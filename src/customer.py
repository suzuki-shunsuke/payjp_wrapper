"""顧客関連のAPI
"""


import payjp

from .error import *


def create_customer(**kwargs):
    """顧客を作成して返す
    http://docs.pay.jp/docs/customer-create

    Args:
      Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCreateError
    """
    customer = payjp.Customer.create(**kwargs)
    if "error" in customer:
        error = customer["error"]
        raise CustomerCreateError(error, kwargs)
    else:
        return customer


def retrieve_customer(customer_id):
    """顧客情報を取得(顧客は作成済みとする)
    http://docs.pay.jp/docs/customer-retrieve

    Args:
      customer_id: 顧客ID(str)

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerRetrieveError
    """
    customer = payjp.Customer.retrieve(customer_id)
    if "error" in customer:
        error = customer["error"]
        raise CustomerRetrieveError(error, {"customer_id": customer_id})
    else:
        return customer


def update_customer(customer, **kwargs):
    """顧客情報を更新
    http://docs.pay.jp/docs/customer-update

    Args:
      customer: 顧客ID(str) or 顧客オブジェクト
      **kwargs: Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerUpdateError
    """
    if isinstance(customer, str):
        customer = retrieve_customer(customer)
    for key, val in kwargs.items():
        setattr(customer, key, val)
    result = customer.save()
    if "error" in result:
        error = result["error"]
        kwargs["customer"] = customer
        raise CustomerUpdateError(error, kwargs)
    else:
        return result


def create_customer_card(customer, **kwargs):
    """顧客のカードを作成して返す(顧客は作成済みとする)
    http://docs.pay.jp/docs/customer-card-create

    Args:
      customer: 顧客ID(str) or 顧客オブジェクト
      **kwargs: Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCardCreateError
    """
    if isinstance(customer, str):
        customer = retrieve_customer(customer)
    card = customer.cards.create(**kwargs)
    if "error" in card:
        error = card["error"]
        raise CustomerCardCreateError(error, kwargs)
    else:
        return card


def retrieve_customer_card(card_id, customer):
    """顧客のカード情報を取得
    http://docs.pay.jp/docs/customer-card-retrieve

    Args:
      card: カードID(str)
      **kwargs:
        customer: 顧客ID(str) or 顧客オブジェクト
        card: カードID(str) or カードオブジェクト

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCardRetrieveError
    """
    if isinstance(customer, str):
        customer = retrieve_customer(customer)
    card = customer.cards.retrieve(card_id)
    if "error" in card:
        raise CustomerCardRetrieveError(card["error"], card_id=card_id, customer=customer)
    else:
        return card


def update_customer_card(card, **kwargs):
    """顧客のカードを更新
    http://docs.pay.jp/docs/customer-card-update

    Args:
      card: カードID(str) or カードオブジェクト
      **kwargs:
        customer: 顧客ID(str) or 顧客オブジェクト
        Pay.JPのドキュメントを参照

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCardUpdateError
    """
    if isinstance(card, str):
        customer = kwargs.pop("customer")
        if isinstance(customer, str):
            customer = retrieve_customer(customer)
        card = retrieve_customer_card(card, customer)
    for key, val in kwargs.items():
        setattr(card, key, val)
    result = card.save()
    if "error" in result:
        error = result["error"]
        kwargs["customer"] = customer
        kwargs["card"] = card
        raise CustomerCardUpdateError(error, kwargs)
    else:
        return result


def delete_customer_card(card, **kwargs):
    """顧客のカードを削除
    http://docs.pay.jp/docs/customer-card-delete

    Args:
      card: カードID(str) or カードオブジェクト
      **kwargs:
        customer: 顧客ID(str) or 顧客オブジェクト

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCardDeleteError
    """
    if isinstance(card, str):
        customer = kwargs["customer"]
        if isinstance(customer, str):
            kwargs["customer"] = customer = retrieve_customer(customer)
        card = retrieve_customer_card(card, customer)
    result = card.delete()
    if "error" in result:
        error = result["error"]
        kwargs["card"] = card
        raise CustomerCardDeleteError(error, kwargs)
    else:
        return result


def get_cards(customer, **kwargs):
    """顧客のカードリストを返す
    http://docs.pay.jp/docs/顧客のカードリストを取得

    Args:
      customer: 顧客ID(str) or 顧客オブジェクト
      kwargs:
        offset: int or None
        limit: 1〜1000 int or None

    Return:
      Pay.JPのドキュメントを参照

    Raises:
      CustomerCardListError
    """
    if isinstance(customer, str):
        customer = retrieve_customer(customer)
    cards = customer.cards.all(**kwargs)
    if "error" in cards:
        error = cards["error"]
        raise CustomerCardListError(error, kwargs)
    else:
        return cards
