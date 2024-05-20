from aiogram.utils.keyboard import InlineKeyboardBuilder


def save_keyboard(edit: str, next: str = None, back: str = None, is_save: bool = None):
    builder = InlineKeyboardBuilder()
    if back:
        builder.button(text='Назад', callback_data=f'event_creator:{back}:back')
    builder.button(text='Изменить', callback_data=f'event_creator:{edit}:edit')
    if next:
        builder.button(text='Продолжить', callback_data=f'event_creator:{next}:next')
    if is_save:
        builder.button(text='Сохранить', callback_data='event_creator:save')
    builder.adjust(2, 1)
    return builder.as_markup()


def cancel_keyboard(cancel: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Отмена', callback_data=f'event_creator:{cancel}:back')
    builder.adjust(2, 1)
    return builder.as_markup()
