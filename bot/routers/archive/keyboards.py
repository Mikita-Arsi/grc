from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import GRCEvent


def archive_keyboard(sort_events: list[GRCEvent], current_point: int = 0):
    block_len = 8
    builder = InlineKeyboardBuilder()
    sizes = []
    for i in range(current_point, len(sort_events)):
        if i == len(sort_events): break
        builder.button(
            text=f'{i + 1}. {sort_events[i].datetime.strftime("%d.%m.%Y")} - {sort_events[i].title}',
            callback_data=f'archive:{sort_events[i].id}:view')
        sizes.append(1)
        if ((i + 1) % block_len) == 0.0 or (i + 1 == len(sort_events)):
            last_button_size = 1
            if current_point > 0:
                builder.button(text='◀️', callback_data=f'archive:{current_point - block_len}:step')
                last_button_size += 1
            builder.button(
                text=f'{current_point//block_len + 1}/{len(sort_events)//block_len+(len(sort_events)%block_len!=0)}',
                callback_data=f'archive:{i}:list'
            )
            if i < len(sort_events) - 1:
                builder.button(text='▶️', callback_data=f'archive:{i + 1}:step')
                last_button_size += 1
            sizes.append(last_button_size)
            break

    builder.adjust(*sizes)
    return builder.as_markup()


def back_to_event_keyboard(ev_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data=f'archive:{ev_id}:edit_message:view')
    builder.adjust(1)
    return builder.as_markup()


def event_keyboard(ev_id: str, is_admin: bool = False):
    builder = InlineKeyboardBuilder()
    builder.button(text='Протокол', callback_data=f'protocol:{ev_id}:view')
    if is_admin:
        builder.button(text='Добавить протокол', callback_data=f'protocol:{ev_id}:add')
        builder.button(text='Изменить протокол', callback_data=f'protocol:{ev_id}:edit')
        builder.button(text='Изменить протокол', callback_data=f'archive:{ev_id}:edit')
        builder.button(text='Отметка присутствующих', callback_data=f'archive:{ev_id}:mark')

    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def visitor_keyboard(user_id: int, event_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Был онлайн', callback_data=f'mark:{event_id}:{user_id}:True')
    builder.button(text='Был оффлайн', callback_data=f'mark:{event_id}:{user_id}:False')
    builder.button(text='Не был', callback_data=f'mark:{event_id}:{user_id}:delete')
    builder.adjust(2, 1)
    return builder.as_markup()
