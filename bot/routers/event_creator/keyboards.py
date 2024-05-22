from aiogram.utils.keyboard import InlineKeyboardBuilder


def save_keyboard(edit: str, next: str = None, back: str = None, is_save: bool = None):
    builder = InlineKeyboardBuilder()
    sizes = [1]
    if back:
        sizes[0] += 1
        builder.button(text='Назад', callback_data=f'event_creator:{back}:back')
    builder.button(text='Изменить', callback_data=f'event_creator:{edit}:edit')
    if next:
        sizes[0] += 1
        builder.button(text='Продолжить', callback_data=f'event_creator:{next}:next')
    if is_save:
        sizes.append(1)
        builder.button(text='Сохранить', callback_data='event_creator:save')
    sizes.append(1)
    builder.button(text='Удалить черновик', callback_data=f'event_creator:{edit}:next')
    builder.adjust(*sizes)
    return builder.as_markup()


def cancel_keyboard(cancel: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Отмена', callback_data=f'event_creator:{cancel}:back')
    builder.adjust(2, 1)
    return builder.as_markup()
