START_COMMANDS = ['/start']

GREETING_ANSWER = 'Здравствуйте, я бот по заказу еды.'

DEFAULT_ANSWER = 'Нажмите /start для начала'

REGISTRATION_NEEDED = 'Для пользования ботом, надо зарегестрироваться'

INTENTS = [
    {
        'name': 'Сделать заказ',
        'command': ['/order', '🛍Сделать заказ'],
        'scenario': 'order',
    },
    {
        'name': 'Регистрация',
        'command': ['/reg', 'Зарегестрироваться'],
        'scenario': 'registration',
    },
    {
        'name': 'Написать отзыв',
        'command': ['/feedback', '📝Написать отзыв'],
        'scenario': 'feedback',
    },
    {
        'name': 'О проекте',
        'command': ['/about', '❓О боте'],
        'message': 'Тестовый бот по заказу еды\n'
                   'Разработчик: @timurmalik17\n'
                   'Github: https://github.com/timur-cyber/',
    }
]

SCENARIOS = {
    'order': {
        'first_step': 'step1',
        'cart_step': 'step4',
        'steps': {
            'step1': {
                'text': 'Выберите категорию',
                'failure_text': 'Неверное значение',
                'handler': 'handler_category_choice',
                'next_step': 'step2',
                'prev_step': None,
                'options': 'make_categories_keyboard',
                'result': None
            },
            'step2': {
                'text': 'Выберите товар',
                'failure_text': 'Надо выбрать товар',
                'handler': 'handler_product_choice',
                'next_step': 'step3',
                'prev_step': 'step1',
                'options': 'make_products_keyboard',
                'result': None
            },
            'step3': {
                'text': 'Товар: {product_name}\n'
                        'Описание: {description}\n'
                        'Цена: {price}',
                'second_text': 'Выберите кол-во',
                'failure_text': 'Выберите кол-во',
                'handler': 'handler_empty',
                'next_step': 'step4',
                'prev_step': 'step2',
                'options': 'make_product_inline',
                'result': True
            },
            'step4': {
                'text': '🛒Корзина',
                'failure_text': 'Неверное значение',
                'handler': 'handler_empty',
                'next_step': 'step5',
                'prev_step': 'step1',
                'options': 'make_cart_keyboard',
                'result': None
            },
            'step5': {
                'text': 'Введите свой адрес',
                'failure_text': 'Неверное значение',
                'handler': 'handler_address',
                'next_step': 'step6',
                'prev_step': 'step1',
                'options': None,
                'result': None
            },
            'step6': {
                'text': 'Ваш заказ принят!',
                'failure_text': None,
                'handler': None,
                'next_step': None,
                'prev_step': 'step5',
                'options': None,
                'result': None,
                'action': 'make_order'
            },
        }
    },
    'registration': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите своё имя:',
                'failure_text': 'Что-то явно пошло не так, введи правильное значение',
                'handler': 'handler_user_name',
                'next_step': 'step2',
                'prev_step': None,
                'options': None,
                'action': None,
                'result': None,
            },
            'step2': {
                'text': 'Введите свой номер:',
                'failure_text': 'Что-то явно пошло не так, введи правильное значение',
                'handler': 'handler_phone',
                'next_step': 'step3',
                'prev_step': 'step1',
                'options': None,
                'action': None,
                'result': None,
            },
            'step3': {
                'text': 'Регистрация прошла успешно',
                'failure_text': None,
                'handler': None,
                'next_step': None,
                'prev_step': 'step3',
                'options': 'make_start_keyboard',
                'action': 'register_user',
                'result': None,
            },
        }
    },
    'feedback': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Напишите отзыв о боте',
                'failure_text': 'Что-то явно пошло не так, введи правильное значение',
                'handler': 'handler_feedback',
                'next_step': 'step2',
                'prev_step': None,
                'options': None,
                'action': None,
                'result': None,
            },
            'step2': {
                'text': 'Спасибо за ваш отзыв!',
                'failure_text': None,
                'handler': None,
                'next_step': None,
                'prev_step': 'step1',
                'options': 'make_start_keyboard',
                'action': 'register_feedback',
                'result': None,
            },
        }
    }
}
