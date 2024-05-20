from aiogram.utils.keyboard import InlineKeyboardBuilder


def visit_keyboard(ev_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Приду', callback_data=f'visitor:{ev_id}:offline')
    builder.button(text='Буду онлайн', callback_data=f'visitor:{ev_id}:online')
    builder.adjust(2)
    return builder.as_markup()


def rules_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Правила', url="https://telegra.ph/Pravila-05-06-43")
    builder.adjust(1)
    return builder.as_markup()


def new_member_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Правила', url="https://telegra.ph/Pravila-05-06-43")
    builder.button(text='С правилами ознакомлен(а)', callback_data=f'rules:{user_id}')
    builder.adjust(1, 1)
    return builder.as_markup()
