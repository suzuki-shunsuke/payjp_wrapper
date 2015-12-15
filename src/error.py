"""
"""


class PayJPError(Exception):
    """Pay.JPのAPIをコールした際に起こる全てのエラーの基底クラス

    Attrs:
      params: APIコール時に渡したパラメータ(dict)
      error: エラー時のレスポンスのキー "error" の値
    """
    def __init__(self, error, params):
        self.params = params
        self.error = error
        self.message = error["message"]
        self.status = error["status"]
        self.type = error["type"]


class CustomerError(PayJPError):
    """顧客関連のAPIコール時のエラーの基底クラス
    """
    pass


class ChargeError(PayJPError):
    """支払い関連のAPIコール時のエラーの基底クラス
    """
    pass


class TokenError(PayJPError):
    """トークン関連のAPIコール時のエラーの基底クラス
    http://docs.pay.jp/docs/token
    """
    pass


class CustomerCreateError(CustomerError):
    """顧客を作成時のエラー
    """
    pass


class CustomerRetrieveError(CustomerError):
    """顧客情報を取得時のエラー
    """
    pass


class CustomerUpdateError(CustomerError):
    """顧客情報を更新時のエラー
    """
    pass


class CustomerCardCreateError(CustomerError):
    """顧客のカードを作成時のエラー
    """
    pass


class CustomerCardRetrieveError(CustomerError):
    """顧客のカード情報を取得時のエラー
    """
    pass


class CustomerCardUpdateError(CustomerError):
    """顧客のカードを更新時のエラー
    """
    pass


class CustomerCardDeleteError(CustomerError):
    """顧客のカードを削除時のエラー
    """
    pass


class CustomerCardListError(CustomerError):
    """顧客のカードリストを取得時のエラー
    """
    pass


class ChargeCreateError(ChargeError):
    """支払いを作成時のエラー
    """
    pass


class TokenCreateError(TokenError):
    """トークンを作成時のエラー
    http://docs.pay.jp/docs/token-create
    """
    pass
