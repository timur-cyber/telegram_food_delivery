"""
Вспомогательный модуль для обработки входящих сообщений, валидации данных и проходу по сценарию
"""
from app_products.models import Category, Product


def handler_user_name(text, context):
    """
    Валидация имени пользователя
    :param text: str
    :param context: dict
    :return: bool
    """
    if text.isalpha():
        context['first_name'] = text
        return True
    else:
        return False


def handler_phone(text, context):
    """
    Валидауия номера телефона
    :param text: str
    :param context: dict
    :return: bool
    """
    if '+' in text and text[1:].isdigit():
        context['phone'] = text
        return True
    else:
        return False


def handler_category_choice(text, context):
    """
    Проверка верности введённой категории
    :param text: str
    :param context: dict
    :return: bool
    """
    if Category.objects.filter(category_name=text).exists():
        context['category'] = text
        return True
    else:
        return False


def handler_product_choice(text, context):
    """
    Проверка верности введённого товара
    :param text: str
    :param context: dict
    :return: bool
    """
    if Product.objects.filter(name=text).exists():
        product = Product.objects.get(name=text)
        context['product_name'] = text
        context['image'] = str(product.image)
        context['description'] = product.description
        context['price'] = product.price
        return True
    else:
        return False


def handler_empty(text, context):
    """
    Пустая проверка. Т.е. продвижение по сценарию путём сообщения невозможно
    :param text: str
    :param context: dict
    :return: False
    """
    return False


def handler_feedback(text, context):
    """
    Валидация оставленного пользователем отзыва
    :param text: str
    :param context: dict
    :return: bool
    """
    if 3 < len(text) < 150:
        context['feedback'] = text
        return True


def handler_address(text, context):
    """
    Валидация адреса
    :param text: str
    :param context: dict
    :return: bool
    """
    if 3 < len(text) < 150:
        context['address'] = text
        return True
