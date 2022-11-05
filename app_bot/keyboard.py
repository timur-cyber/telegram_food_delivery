"""
Вспомогательный модуль для манипуляций клавиатурой пользователя внутри приложения Telegram
"""
import telebot

from app_cart.models import Cart, CartItem
from app_products.models import Category, Product

START_KEYBOARD_VALUES = ['🛍Сделать заказ', '📝Написать отзыв', '❓О боте']


def make_keyboard(values, width=1, back=False, cart=False):
    """
    Основная функция создания объекта клавиатуры для API
    :param values: list
    :param width: int
    :param back: bool
    :param cart: bool
    :return: ReplyKeyboardMarkup
    """
    # return telebot.types.ReplyKeyboardMarkup(row_width=width).add(*[telebot.types.KeyboardButton(item) for item in values])
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=width)
    markups = list()
    if values:
        for item in values:
            itembtn = telebot.types.KeyboardButton(item)
            markups.append(itembtn)
        keyboard.add(*markups)
    if cart:
        cartbtn = telebot.types.KeyboardButton('🛒Корзина')
        keyboard.add(cartbtn)
    if back:
        backbtn = telebot.types.KeyboardButton('🔙Назад')
        keyboard.add(backbtn)
    return keyboard


def make_start_keyboard(*args, **kwargs):
    """
    Функция создания начальной клавиатуры
    :return: ReplyKeyboardMarkup
    """
    return make_keyboard(START_KEYBOARD_VALUES, 1)


def make_categories_keyboard(*args, **kwargs):
    """
    Функция создания клавиатуры категорий из БД
    :return: ReplyKeyboardMarkup
    """
    category_names = [item.category_name for item in Category.objects.all()]
    return make_keyboard(category_names, width=2, back=True, cart=True)


def make_products_keyboard(*args, **kwargs):
    """
    Функция создания клавиатуры продуктов на основе данной категории из контекста
    :param kwargs: context
    :return: ReplyKeyboardMarkup
    """
    category_name = kwargs['category']
    category = Category.objects.get(category_name=category_name)
    product_names = [item.name for item in Product.objects.filter(category=category)]
    return make_keyboard(product_names, width=2, back=True)


def make_product_inline(quantity=1, *args, **kwargs):
    """
    Функция создания кнопок взаимодействия под сообщением о продукте
    :param quantity: int
    :return: InlineKeyboardMarkup
    """
    inline_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    minus = telebot.types.InlineKeyboardButton(text='➖', callback_data='minus')
    value = telebot.types.InlineKeyboardButton(text='{}'.format(quantity), callback_data=quantity)
    plus = telebot.types.InlineKeyboardButton(text='➕', callback_data='plus')
    inline_markup.add(minus, value, plus)
    done = telebot.types.InlineKeyboardButton(text='Готово', callback_data='done')
    inline_markup.add(done)
    return inline_markup


def make_cart_inline(user_account):
    """
    Функция создания кнопок взаимодействия под отображением корзины для управления товарами внутри корзины
    :param user_account: TelegramUser
    :return: InlineKeyboardMarkup
    """
    x = '\U0000274c'
    cart = Cart.objects.get(user=user_account)
    cart_items = sorted([item for item in CartItem.objects.filter(cart=cart)], key=lambda x: x.id)
    inline_markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    for cart_item in cart_items:
        cancel = telebot.types.InlineKeyboardButton(text=f'{x} {cart_item.product.name}',
                                                    callback_data=f'{cart_item.id}&cancel')
        inline_markup.add(cancel)
        minus = telebot.types.InlineKeyboardButton(text='➖', callback_data=f'{cart_item.id}&minus')
        value = telebot.types.InlineKeyboardButton(text='{}'.format(cart_item.quantity),
                                                   callback_data=cart_item.quantity)
        plus = telebot.types.InlineKeyboardButton(text='➕', callback_data=f'{cart_item.id}&plus')
        inline_markup.add(minus, value, plus)
    return inline_markup


def make_cart_keyboard(*args, **kwargs):
    """
    Функция создания клавиатуры для осуществления действий с корзиной
    :return: ReplyKeyboardMarkup
    """
    buttons = ['✅Подтвердить', '🔁Очистить корзину']
    return make_keyboard(values=buttons, width=1, back=True)


def make_share_contact_button(*args, **kwargs):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact_key = telebot.types.KeyboardButton("☎️ Поделиться контактом", request_contact=True)
    keyboard.add(contact_key)
    backbtn = telebot.types.KeyboardButton('🔙Назад')
    keyboard.add(backbtn)
    return keyboard


def make_share_location_button(*args, **kwargs):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact_key = telebot.types.KeyboardButton("📍️ Отправить локацию", request_location=True)
    keyboard.add(contact_key)
    backbtn = telebot.types.KeyboardButton('🔙Назад')
    keyboard.add(backbtn)
    return keyboard


def make_back_button(*args, **kwargs):
    return make_keyboard(None, back=True)
