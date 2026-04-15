"""Appraisal agent implementation."""

from ...agents.client import create_gemini_client
from .appraiser import Appraiser
from .base_info_extractor import BaseInfoExtractor


class AppraisalAgent:
    """画像査定フローを実行し、進捗状態を管理するエージェント。"""

    def __init__(self, find_similar_items, list_categories, state_manager):
        self.find_similar_items = find_similar_items
        self.list_categories = list_categories
        self.state_manager = state_manager
        self.gemini_client = create_gemini_client()
        self.base_info_extractor = BaseInfoExtractor(self.gemini_client)
        self.appraiser = Appraiser(self.gemini_client)

    def _resolve_resume_state(
        self, appraisal_id: str
    ) -> tuple[dict | None, str | None, dict | None, list | None, bool]:
        """再開可否や再開地点を判定し、必要な状態を返す。

        Args:
            appraisal_id: 査定ID。

        Returns:
            tuple: (existing_state, resume_from, base_info_result, similar_items, should_return)
                existing_state: Redisに保存済みの状態。存在しない場合はNone。
                resume_from: 再開地点。存在しない場合はNone。
                base_info_result: base_info工程の結果。必要な場合のみ返す。
                similar_items: 類似商品リスト。必要な場合のみ返す。
                should_return: 既存状態をそのまま返すべきかどうか。
        """
        existing_state = self.state_manager.get(appraisal_id)
        resume_from = None
        base_info_result = None
        similar_items = None
        should_return = False

        if existing_state is not None:
            status = existing_state.get("status")

            # 完了済みはそのまま返して終了
            if status == "done":
                should_return = True
                return existing_state, resume_from, base_info_result, similar_items, should_return

            # 再撮影の場合は、どの工程から再開するかを判定
            if status == "retake_required" and existing_state.get("retake_required_by") in (
                "base_info",
                "appraiser",
            ):
                resume_from = existing_state.get("retake_required_by")
                # appraiser再開なら、必要な中間結果を復元
                if resume_from == "appraiser":
                    restored_base_info = existing_state.get("base_info_result")
                    restored_similar_items = existing_state.get("similar_items")
                    # 中間状態が欠落している場合は再開せず、既存状態を返す。
                    if restored_base_info is None or restored_similar_items is None:
                        should_return = True
                        return (
                            existing_state,
                            resume_from,
                            base_info_result,
                            similar_items,
                            should_return,
                        )
                    base_info_result = restored_base_info
                    similar_items = restored_similar_items

            # それ以外の途中状態は、再開ではなくそのまま返す
            else:
                should_return = True
                return existing_state, resume_from, base_info_result, similar_items, should_return

        return existing_state, resume_from, base_info_result, similar_items, should_return

    def run(self, appraisal_id: str, image_bytes: bytes) -> dict:
        """画像を元に査定を行い、状態をRedisで管理する。

        Args:
            appraisal_id: 査定の一意なID
            image_bytes: 査定対象の画像のバイト列

        Returns:
            以下いずれかの辞書を返す。

            - status == "done" の場合:
              {
                "status": "done",
                "appraisal_id": str,
                "result": {
                  "brand": str,
                  "category": str,
                  "appraisal_price": int,   # 類似商品が無い場合は -1
                  "appraisal_reason": str
                }
              }

            - status == "retake_required" の場合:
              {
                "status": "retake_required",
                "appraisal_id": str,
                "retake_message": str,
                "retake_required_by": "base_info" | "appraiser"
              }

            - 途中状態のまま返す場合（再開不可・処理中など）:
              Redis に保存済みの状態辞書（status が "processing" など）。
        """
        (
            existing_state,
            resume_from,
            base_info_result,
            similar_items,
            should_return,
        ) = self._resolve_resume_state(appraisal_id)
        if should_return and existing_state is not None:
            return existing_state

        # ポリシー:
        # - 処理中/再撮影要求/完了の各状態をRedisへ保存する
        # - done時にも削除せず、TTL内は同一appraisal_idで同結果を返す
        self.state_manager.set(appraisal_id, {"status": "processing", "appraisal_id": appraisal_id})

        # 画像からブランド・カテゴリを抽出（必要な場合のみ）
        if resume_from != "appraiser":
            categories = self.list_categories()
            base_info_result = self.base_info_extractor.run(image_bytes, categories)

            if base_info_result["retake_required"]:
                result = {
                    "status": "retake_required",
                    "appraisal_id": appraisal_id,
                    "retake_message": base_info_result["retake_instructions"],
                    "retake_required_by": "base_info",
                }
                self.state_manager.set(appraisal_id, result)
                return result

        # 再撮影が必要な場合を除いて、類似商品情報を取得
        if similar_items is None:
            similar_items = self.find_similar_items(
                brand=base_info_result["brand"],
                category=base_info_result["category"],
            )

        # 査定の参考になる類似商品情報がない場合は、査定が不可能なことを返す
        if len(similar_items) == 0:
            result = {
                "status": "done",
                "appraisal_id": appraisal_id,
                "result": {
                    "brand": base_info_result["brand"],
                    "category": base_info_result["category"],
                    "appraisal_price": -1,
                    "appraisal_reason": "査定の参考になる類似商品が見つからなかったため、査定ができませんでした。",
                },
            }
            self.state_manager.set(appraisal_id, result)
            return result

        self.state_manager.set(
            appraisal_id,
            {
                "status": "processing",
                "appraisal_id": appraisal_id,
                "base_info_result": base_info_result,
                "similar_items": similar_items,
            },
        )

        # 画像と類似商品情報から査定を実行
        appraisal_result = self.appraiser.run(
            similar_item_descriptions=similar_items,
            image_bytes=image_bytes,
        )

        price = int(appraisal_result.get("appraisal_price", -1))

        result = {
            "status": "done",
            "appraisal_id": appraisal_id,
            "result": {
                "brand": base_info_result["brand"],
                "category": base_info_result["category"],
                "appraisal_price": price,
                "appraisal_reason": appraisal_result.get("appraisal_reason", ""),
            },
        }
        self.state_manager.set(appraisal_id, result)
        return result
