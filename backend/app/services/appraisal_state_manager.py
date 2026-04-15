import json

from redis import Redis


class AppraisalStateManager:
    """査定状態をRedisに保存・取得するための管理クラス。

    appraisalsの状態( processing / retake_required / done )をキーごとに保存し、
    TTLで自動期限切れにする。
    Redisキーは名前空間を付与して衝突を避ける。
    """

    def __init__(self, redis_client: Redis, ttl_seconds: int = 3600) -> None:
        self.redis_client = redis_client
        self.ttl_seconds = ttl_seconds

    def _key(self, appraisal_id: str) -> str:
        """Redisキーを生成する。

        共有されたキー空間で衝突を避けるため、"appraisal:" の名前空間を付与する。
        """
        return f"appraisal:{appraisal_id}"

    def set(self, appraisal_id: str, state: dict) -> None:
        """査定の状態をRedisに保存する。"""
        payload = json.dumps(state, ensure_ascii=False)
        self.redis_client.setex(self._key(appraisal_id), self.ttl_seconds, payload)

    def get(self, appraisal_id: str) -> dict | None:
        """査定の状態をRedisから取得する。"""
        raw = self.redis_client.get(self._key(appraisal_id))
        if raw is None:
            return None
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode("utf-8")
        return json.loads(raw)

    def delete(self, appraisal_id: str) -> bool:
        """査定の状態をRedisから削除する。"""
        return self.redis_client.delete(self._key(appraisal_id)) > 0

    def exists(self, appraisal_id: str) -> bool:
        """査定の状態がRedisに存在するか確認する。"""
        return self.redis_client.exists(self._key(appraisal_id)) > 0
