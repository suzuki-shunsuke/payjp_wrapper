"""トークン関連のAPI
"""


import payjp

from .error import *


def create_token(**kwargs):
    """トークンを作成
    http://docs.pay.jp/docs/token-create

    Args:
      **kwargs:
        number:
        exp_month: str
        exp_year: str
        cvc:
        name:
      Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      TokenCreateError
    """
    token = payjp.Token.create(card=kwargs)
    if "error" in token:
        error = token["error"]
        raise TokenCreateError(error, kwargs)
    else:
        return token
