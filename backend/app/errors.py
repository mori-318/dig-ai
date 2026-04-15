"""外部AI連携で利用する独自例外定義。"""

class ExternalAIError(Exception):
    """外部AIサービス起因の例外。"""


class ExternalAIUnavailableError(ExternalAIError):
    """外部AIが一時的に利用不可のときの例外。"""


class ExternalAIResponseError(ExternalAIError):
    """外部AIの応答が契約と不一致のときの例外。"""
