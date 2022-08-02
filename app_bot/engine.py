import logging

import telebot

from app_bot import settings, handlers, keyboard
from app_bot.models import TelegramUser, TelegramState, Feedback
from app_cart.models import Cart, CartItem
from app_orders.models import Order, OrderItem
from app_products.models import Product

logger = logging.getLogger("bot")


class BotEngine:
    """
    Класс для обработки сообщений посредством Telegram WebHook
    """

    def __init__(self, TOKEN):
        self.bot = telebot.TeleBot(TOKEN)

    def send_message(self, user_id, text, reply_markup=None, parse=None, image=None, second_text=None):
        """
        Доработанный метод отправки сообщений
        :param user_id: int
        :param text: str
        :param reply_markup: ReplyKeyboard or InlineKeyboard class
        :param parse: str
        :param image: str
        :param second_text: str
        :return: API reply
        """
        text_to_send = text
        if second_text:
            self.bot.send_message(user_id, second_text,
                                  reply_markup=keyboard.make_keyboard(None, back=True))
        if not reply_markup:
            reply_markup = telebot.types.ReplyKeyboardRemove(selective=False)
        elif isinstance(reply_markup, str):
            get_keyboard = getattr(keyboard, reply_markup)
            user = TelegramState.objects.get(user_id=user_id)
            reply_markup = get_keyboard(**user.context)
        if image:
            image_to_send = open(f'media/{image}', 'rb')
            return self.bot.send_photo(user_id, image_to_send, caption=text_to_send, parse_mode=parse,
                                       reply_markup=reply_markup)
        else:
            return self.bot.send_message(user_id, text_to_send, reply_markup=reply_markup, parse_mode=parse)

    @staticmethod
    def user_is_registered(user_id: int):
        """
        Метод проверки регистрации пользователей
        :param user_id: int
        :return: bool
        """
        if TelegramUser.objects.filter(user_id=user_id).exists():
            return True
        else:
            return False

    @staticmethod
    def register_user(user_id: int, username, first_name, phone):
        """
        Метод регистрации новых пользователей
        :param user_id: int
        :param username: str
        :param first_name: str
        :param phone: str
        :return: None
        """
        TelegramUser.objects.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            phone_num=phone
        )
        logger.info(f"User {user_id} registered as {first_name}")

    def make_order(self, user_id, address, *args, **kwargs):
        """
        Метод переноса данных с корзины в модель заказа
        :param user_id: int
        :param address: str
        :return: None
        """
        user = TelegramUser.objects.get(user_id=user_id)
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        order = Order.objects.create(
            user=user,
            address=address
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        self.empty_cart(user)
        self.send_message(user_id, f'Номер вашего заказа #{order.id}', reply_markup=keyboard.make_start_keyboard())
        logger.info(f"User {user_id} has made order #{order.id}")

    @staticmethod
    def register_feedback(user_id, feedback, *args, **kwargs):
        """
        Метод добавление отзыва в БД
        :param user_id: int
        :param feedback: str
        :return: None
        """
        user = TelegramUser.objects.get(user_id=user_id)
        Feedback.objects.create(
            user=user,
            feedback=feedback
        )
        logger.info(f"User {user_id} left feedback")

    @staticmethod
    def user_in_scenario(user_id):
        """
        Метод проверки пользователей в сценарии
        :param user_id: int
        :return: bool
        """
        if TelegramState.objects.filter(user_id=user_id).exists():
            return True
        else:
            return False

    def perform_rollback(self, user_id, steps, step, user):
        """
        Метод реализации перехода на предыдущий шаг сценария или отмены вовсе
        :param user_id: int
        :param steps: str
        :param step: str
        :param user: TelegramState
        :return: None
        """
        prev_step = step['prev_step']
        if prev_step:
            step = steps[prev_step]
            user.step = prev_step
            user.context['image'] = None
            user.save()
            self.send_message(user_id, step['text'].format(**user.context), reply_markup=step['options'])
            logger.debug(f"User {user_id} performed rollback from to {prev_step}")
        else:
            self.empty_cart(user)
            user.delete()
            self.send_message(user_id, settings.GREETING_ANSWER, reply_markup=keyboard.make_start_keyboard())
            logger.debug(f"User {user_id} quit scenario - {user.scenario}")

    def start_scenario(self, user_id, scenario):
        """
        Метод реализации начала сценария
        :param user_id: str
        :param scenario: str
        :return:
        """
        step_name = settings.SCENARIOS[scenario]['first_step']
        new_state = TelegramState.objects.create(
            user_id=user_id,
            scenario=scenario,
            step=step_name,
            context=dict()
        )
        new_state.save()
        text = settings.SCENARIOS[scenario]['steps'][step_name]['text']
        self.send_message(user_id, text, reply_markup=settings.SCENARIOS[scenario]['steps'][step_name]['options'])
        logger.debug(f"User {user_id} started scenario - {scenario}")

    def continue_scenario(self, user, next_step, data, force_transit=None):
        """
        Метод реализации продолжения сценария
        :param user: TelegramState
        :param next_step: str
        :param data: dict
        :param force_transit: str
        :return: None
        """
        user_id = user.user_id
        steps = settings.SCENARIOS[user.scenario]['steps']
        step_name = user.step
        step = steps[user.step]
        next_message = next_step['text'].format(**user.context)
        reply_markup = getattr(keyboard, next_step['options'])(**user.context) if next_step[
            'options'] else None
        image = user.context.get('image') or None
        second_text = next_step.get('second_text') or None
        msg = self.send_message(user_id, next_message, reply_markup=reply_markup, image=image,
                                second_text=second_text)
        if reply_markup and isinstance(reply_markup, telebot.types.InlineKeyboardMarkup):
            user.context['inline_id'] = msg.message_id
        if next_step['next_step']:
            user.step = step['next_step'] if not force_transit else force_transit
            user.save()
        else:
            user.delete()
        if next_step.get('result'):
            pass
        if next_step.get('action'):
            action = getattr(self, next_step['action'])
            action(**user.context, user_id=user_id, username=data['message']['from'].get('username'))
        logger.debug(f"User {user_id} gets {user.scenario} - {step_name}")

    def add_to_cart(self, user, context):
        """
        Метод добавления товаров в корзину
        :param user: TelegramState
        :param context: dict
        :return: None
        """
        user_account = TelegramUser.objects.get(user_id=user.user_id)
        if not Cart.objects.filter(user=user_account).exists():
            Cart.objects.create(
                user=user_account
            )
        cart = Cart.objects.get(user=user_account)
        product = Product.objects.get(name=context['product_name'])
        if CartItem.objects.filter(product=product).exists():
            item = CartItem.objects.get(product=product)
            item.quantity += context['product_quantity']
            item.save()
        else:
            CartItem.objects.create(
                product=product,
                quantity=context['product_quantity'],
                cart=cart
            )
        user.step = settings.SCENARIOS[user.scenario]['first_step']
        user.context = {}
        user.save()
        self.send_message(user.user_id, 'Товар успещно добавлен в корзину')
        logger.debug(f"User {user.user_id} added item {product.name} x{context['product_quantity']} to cart")

    def empty_cart(self, user):
        """
        Метод опустошения корзины
        :param user: TelegramState
        :return: None
        """
        user_account = TelegramUser.objects.get(user_id=user.user_id)
        if Cart.objects.filter(user=user_account).exists():
            Cart.objects.get(user=user_account).delete()
        logger.debug(f"User {user.user_id} emptied cart")

    def cart_is_not_empty(self, user):
        """
        Метод проверки полности корзины
        :param user: TelegramState
        :return: bool
        """
        user_account = TelegramUser.objects.get(user_id=user.user_id)
        if Cart.objects.filter(user=user_account).exists():
            cart = Cart.objects.get(user=user_account)
            if CartItem.objects.filter(cart=cart).exists():
                return True
            else:
                return False
        else:
            return False

    def get_cart_text(self, user_account):
        """
        Метод отображения корзины 
        :param user_account: TelegramUser
        :return: str
        """
        cart = Cart.objects.get(user=user_account)
        cart_items = sorted([item for item in CartItem.objects.filter(cart=cart)], key=lambda x: x.id)
        cart_text = ''
        total_pirce = 0
        if not cart_items:
            return 'Корзина пуста'
        for i, cart_item in enumerate(cart_items, start=1):
            text = f'<b>{i}. {cart_item.product.name}</b>\n' \
                   f'{cart_item.quantity} x {cart_item.product.price} = {cart_item.price_w_quantity}\n\n'
            cart_text += text
            total_pirce += cart_item.price_w_quantity
        cart_text += f'\n<b>Итого: {total_pirce}</b>\n'
        return cart_text

    def show_cart(self, user):
        """
        Метод отправки корзины текстом с клавиатурой
        :param user: TelegramState
        :return: None
        """
        user_id = user.user_id
        user_account = TelegramUser.objects.get(user_id=user_id)
        cart_text = self.get_cart_text(user_account)
        cart_inline = keyboard.make_cart_inline(user_account)
        msg = self.send_message(user_id, cart_text, reply_markup=cart_inline, parse='HTML')
        user.context['inline_id'] = msg.message_id
        user.save()

    def handler_callback_query(self, user_id, callback_data):
        """
        Метод обработки вызовов InlineMarkup
        :param user_id: int
        :param callback_data: dict
        :return: None
        """
        user = TelegramState.objects.get(user_id=user_id)
        response = callback_data['data']
        context = user.context
        step_text = settings.SCENARIOS[user.scenario]['steps'][user.step]['text'].format(**context)
        if '&' in response:
            user_account = TelegramUser.objects.get(user_id=user_id)
            values = response.split('&')
            item_id = int(values[0])
            action = values[1]
            item = CartItem.objects.get(id=item_id)
            if action == 'plus':
                item.quantity += 1
                item.save()
                self.bot.edit_message_text(text=self.get_cart_text(user_account=user_account),
                                           chat_id=callback_data['message']['chat']['id'],
                                           message_id=callback_data['message']['message_id'],
                                           reply_markup=keyboard.make_cart_inline(user_account), parse_mode='HTML')
            elif action == 'minus':
                if item.quantity <= 1:
                    return
                item.quantity -= 1
                item.save()
                self.bot.edit_message_text(text=self.get_cart_text(user_account=user_account),
                                           chat_id=callback_data['message']['chat']['id'],
                                           message_id=callback_data['message']['message_id'],
                                           reply_markup=keyboard.make_cart_inline(user_account), parse_mode='HTML')
            elif action == 'cancel':
                item.delete()
                self.bot.edit_message_text(text=self.get_cart_text(user_account=user_account),
                                           chat_id=callback_data['message']['chat']['id'],
                                           message_id=callback_data['message']['message_id'],
                                           reply_markup=keyboard.make_cart_inline(user_account), parse_mode='HTML')
        if not context.get('product_quantity'):
            context['product_quantity'] = 1
        if response == 'plus':
            context['product_quantity'] += 1
            user.save()
            self.bot.edit_message_caption(caption=step_text, chat_id=callback_data['message']['chat']['id'],
                                          message_id=callback_data['message']['message_id'],
                                          reply_markup=keyboard.make_product_inline(
                                              quantity=context['product_quantity']))
        elif response == 'minus':
            context['product_quantity'] -= 1
            if context['product_quantity'] <= 0:
                return
            user.save()
            self.bot.edit_message_caption(caption=step_text, chat_id=callback_data['message']['chat']['id'],
                                          message_id=callback_data['message']['message_id'],
                                          reply_markup=keyboard.make_product_inline(
                                              quantity=context['product_quantity']))
        elif response == 'done':
            self.add_to_cart(user, context)
            self.bot.delete_message(chat_id=callback_data['message']['chat']['id'],
                                    message_id=callback_data['message']['message_id'])
            text = settings.SCENARIOS[user.scenario]['steps'][user.step]['text']
            self.send_message(user_id, text,
                              reply_markup=settings.SCENARIOS[user.scenario]['steps'][user.step]['options'])

    def handle_message(self, data: dict):
        """
        Метод обработки сообщений отправленных пользователем
        :param data: dict
        :return: None
        """
        if data.get('message'):
            user_id = data['message']['from']['id']
            text = data['message']['text']
            if self.user_in_scenario(user_id):
                user = TelegramState.objects.get(user_id=user_id)
                if text and any(item == text for item in settings.START_COMMANDS):
                    self.empty_cart(user)
                    user.delete()
                    if self.user_is_registered(user_id):
                        self.send_message(user_id, settings.GREETING_ANSWER,
                                          reply_markup=keyboard.make_start_keyboard())
                    else:
                        self.send_message(user_id, settings.REGISTRATION_NEEDED,
                                          reply_markup=keyboard.make_keyboard(['Зарегестрироваться']))
                    return
                steps = settings.SCENARIOS[user.scenario]['steps']
                step = steps[user.step]
                handler = getattr(handlers, step['handler'])
                next_step = steps[step['next_step']]
                if text and text == '🔙Назад':
                    if user.context.get('inline_id'):
                        inline_id = user.context.get('inline_id')
                        self.bot.delete_message(message_id=inline_id, chat_id=user_id)
                        user.context['inline_id'] = None
                    self.perform_rollback(user_id, steps, step, user)
                    return
                if text == '🛒Корзина' and user.scenario == 'order':
                    if self.cart_is_not_empty(user):
                        step = settings.SCENARIOS[user.scenario]['cart_step']
                        self.continue_scenario(user, settings.SCENARIOS[user.scenario]['steps'][step], data,
                                               force_transit=step)
                        self.show_cart(user)
                    else:
                        self.bot.send_message(user_id, 'Корзина пуста')
                    return
                if text == '🔁Очистить корзину' and user.scenario == 'order':
                    if self.cart_is_not_empty(user):
                        self.empty_cart(user)
                    self.bot.send_message(user_id, 'Корзина очищена')
                    self.perform_rollback(user_id, steps, step, user)
                    return
                if text == '✅Подтвердить' and user.scenario == 'order':
                    if self.cart_is_not_empty(user):
                        self.continue_scenario(user, next_step, data)
                    else:
                        self.bot.send_message(user_id, 'Корзина пуста')
                    return
                response = handler(text=text, context=user.context)
                if response:
                    self.continue_scenario(user, next_step, data)
                else:
                    self.bot.send_message(user_id, step['failure_text'])
            else:
                if self.user_is_registered(user_id):
                    if any(item == text for item in settings.START_COMMANDS):
                        self.send_message(user_id, settings.GREETING_ANSWER,
                                          reply_markup=keyboard.make_start_keyboard())
                    else:
                        for intent in settings.INTENTS:
                            if any(command in text for command in intent['command']):
                                message = intent.get('message')
                                self.send_message(user_id, message,
                                                  reply_markup=keyboard.make_start_keyboard()) if message else None
                                scenario = intent.get('scenario')
                                self.start_scenario(user_id, scenario) if scenario else None
                                break
                        else:
                            self.send_message(user_id, settings.DEFAULT_ANSWER)
                else:
                    if text == 'Зарегестрироваться':
                        scenario = 'registration'
                        self.start_scenario(user_id, scenario)
                        return
                    self.send_message(user_id, settings.REGISTRATION_NEEDED,
                                      reply_markup=keyboard.make_keyboard(['Зарегестрироваться']))
        elif data.get('callback_query'):
            user_id = data['callback_query']['from']['id']
            if self.user_in_scenario(user_id):
                callback_data = data.get('callback_query')
                self.handler_callback_query(user_id, callback_data)

    def get_id(self, data: dict):
        """
        Метод получения id из JSON response
        :param data: dict
        :return: int
        """
        if data.get('message'):
            return data['message']['from']['id']
        elif data.get('callback_query'):
            return data['callback_query']['from']['id']
        else:
            return None

    def work(self, data: dict):
        """
        Метод для полноценной работы в View классе
        :param data: dict
        :return: None
        """
        try:
            self.handle_message(data)
        except Exception as exc:
            user_id = self.get_id(data)
            logger.error(f"User {user_id} got exception - {exc}")
