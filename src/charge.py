"""支払い関連のAPI
"""


import payjp

from .error import ChargeCreateError
from .customer import update_customer, retrieve_customer


def create_charge(**kwargs):
    """支払いを作成
    http://docs.pay.jp/docs/charge-create

    Args:
      **kwargs:
        amount: 支払額(円) int 50~9,999,999の整数
        currency:
          3文字のISOコード(現状 "jpy" のみサポート)
          デフォルトで "jpy"
        card: カードID(str), トークンID, カード情報
        customer: 顧客ID(str)
        description:
        capture:
        expire_days:
      Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      ChargeCreateError

    Examples:
      # デフォルトのカードで支払い
      create_charge(amount, customer=customer_id)
      # 登録済みの他のカードで支払い
      # 顧客のデフォルトのカードを一時的に切り替えて顧客IDで支払う
      create_charge(amount, customer=customer_id, card=card_id)
      # 登録されていないカードで支払う(カードを登録しない)
      # 顧客が登録されている必要がないので顧客情報はいらない
      create_charge(amount, card=card)  # カード情報
      create_charge(amount, card=token_id)
    """

    def _charge_create(**kwargs):
        charge = payjp.Charge.create(**kwargs)
        if "error" in charge:
            error = charge["error"]
            raise ChargeCreateError(error, kwargs)
        else:
            return charge

    kwargs.setdefault("currency", "jpy")
    if "customer" in kwargs:
        customer = kwargs["customer"]
        if "card" in kwargs:
            # 登録済みのカードで支払い
            card = kwargs.pop("card")
            default_card = retrieve_customer(customer)["default_card"]
            update_customer(customer, default_card=card)
            try:
                charge = _charge_create(**kwargs)
            except ChargeCreateError as e:
                kwargs["card"] = card
                update_customer(customer, default_card=defalt_card)
                raise e
            kwargs["card"] = card
            update_customer(customer, default_card=default_card)
            return charge
        else:
            # デフォルトのカードで決済
            return _charge_create(**kwargs)
    else:
        # 登録されていないカードで決済
        return _charge_create(**kwargs)
