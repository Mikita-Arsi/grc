from aiogram import Router
from aiogram.enums import ChatMemberStatus
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from asyncpg import UniqueViolationError

from db import GRCEvent, GRCProtocol, GRCUser, GRCVisitor, GRCEventCreator
from .keyboards import archive_keyboard, event_keyboard, back_to_event_keyboard, visitor_keyboard
from ..event_creator.keyboards import save_keyboard
from ...const import admin_chat_id
from ...texts import event_constructor, new_event_texts
from ...states import ProtocolEditorState, EventEditorState
from ...filters import (
    PrivateMessageFilter,
    ChatMemberFilter,
    ViewFilter,
    ArchiveCallbackFilter,
    StepArchiveFilter,
    ProtocolFilter,
    AddFilter,
    EditFilter,
    AdminFilter,
    MarkFilter,
    ArchiveMarkFilter
)

archive_router = Router(name="archive")


@archive_router.message(PrivateMessageFilter(), ChatMemberFilter(), Command(commands=['archive']))
async def show_archive(message: Message):
    events = await GRCEvent.objects.all()
    sort_events = sorted(events, key=lambda event: event.datetime)
    await message.answer(
        'Выберите собрание',
        reply_markup=archive_keyboard(sort_events),
        parse_mode='HTML'
    )


@archive_router.callback_query(ArchiveCallbackFilter(), ViewFilter())
async def view_event(call: CallbackQuery):
    event = await GRCEvent.objects.get(id=int(call.data.split(':')[1]))
    chat_member = await call.bot.get_chat_member(admin_chat_id, call.message.from_user.id)
    is_admin = chat_member.status != ChatMemberStatus.LEFT
    if call.data.split(':')[2] == "edit_message":
        await call.message.edit_text(
            event_constructor(**event.__dict__),
            parse_mode='HTML',
            reply_markup=event_keyboard(call.data.split(':')[1], is_admin)
        )
    else:
        await call.message.answer(
            event_constructor(**event.__dict__),
            parse_mode='HTML',
            reply_markup=event_keyboard(call.data.split(':')[1], is_admin)
        )


@archive_router.callback_query(ArchiveCallbackFilter(), StepArchiveFilter())
async def step_event(call: CallbackQuery):
    events = await GRCEvent.objects.all()
    sort_events = sorted(events, key=lambda event: event.datetime)
    current_point = int(call.data.split(":")[1])
    await call.message.edit_reply_markup(
        reply_markup=archive_keyboard(sort_events, current_point)
    )


@archive_router.callback_query(ProtocolFilter(), ViewFilter())
async def view_protocol(call: CallbackQuery):
    event_id = int(call.data.split(":")[1])
    protocol = await GRCProtocol.objects.get_or_none(event_id=event_id)
    if protocol:
        await call.message.edit_text(
            protocol.text,
            reply_markup=back_to_event_keyboard(event_id)
        )
    else:
        await call.answer(
            "Протокол ещё не создан",
            show_alert=True
        )


@archive_router.callback_query(ProtocolFilter(), AddFilter())
async def add_protocol(call: CallbackQuery, state: FSMContext):
    event_id = int(call.data.split(":")[1])
    try:
        await GRCProtocol.objects.create(tg_id=call.from_user.id, event_id=event_id, text="")
    except UniqueViolationError:
        await call.answer("Протокол уже существует", show_alert=True)
        return
    await state.set_state(ProtocolEditorState)
    await call.message.answer(
        "Введите протокол"
    )


@archive_router.callback_query(ProtocolFilter(), EditFilter())
async def edit_protocol(call: CallbackQuery, state: FSMContext):
    await state.set_state(ProtocolEditorState)
    event_id = int(call.data.split(":")[1])
    protocol: GRCProtocol = await GRCProtocol.objects.get(event_id=event_id)
    await protocol.upsert(tg_id=call.from_user.id)
    await call.message.answer(
        "Введите протокол"
    )


@archive_router.message(PrivateMessageFilter(), AdminFilter(), ProtocolEditorState)
async def write_protocol(message: Message, state: FSMContext):
    await state.clear()
    protocol = (await GRCProtocol.objects.filter(tg_id=message.from_user.id).all())[0]
    await protocol.upsert(tg_id=1, text=message.text)
    await message.answer(
        "Протокол записан"
    )
    event = await GRCEvent.objects.get(id=protocol.event_id)
    chat_member = await message.bot.get_chat_member(admin_chat_id, message.from_user.id)
    is_admin = chat_member.status != ChatMemberStatus.LEFT
    await message.answer(
        event_constructor(**event.__dict__),
        parse_mode='HTML',
        reply_markup=event_keyboard(str(protocol.event_id), is_admin)
    )


@archive_router.callback_query(ArchiveCallbackFilter(), ArchiveMarkFilter())
async def show_visitors(call: CallbackQuery):
    visitors = await GRCVisitor.objects.filter(event_id=int(call.data.split(":")[1])).all()
    if len(visitors) == 0:
        await call.answer("Никто не отметился", show_alert=True)
        return
    for i in visitors:
        user = await GRCUser.objects.get(tg_id=i.tg_id)
        await call.message.answer(
            f'<a href="tg://user?id={user.tg_id}">{user.first_name}{" " + user.last_name if user.last_name else ""}</a>\nУказано: {"онлайн" if i.is_online else "оффлайн"}',
            parse_mode="HTML",
            reply_markup=visitor_keyboard(user.tg_id, i.event_id)
        )


@archive_router.callback_query(ArchiveCallbackFilter(), EditFilter())
async def edit_event(call: CallbackQuery, state: FSMContext):
    event_id = int(call.data.split(":")[1])
    event = await GRCEvent.objects.get(id=event_id)
    await GRCEvent.objects.delete(id=event_id)
    del event['id']
    await GRCEventCreator.objects.filter(id=1).update(**event)
    await state.set_state(EventEditorState.title)
    await call.message.answer(
        event_constructor(**event.__dict__),
        parse_mode='HTML',
        disable_web_page_preview=True
    )
    await call.message.answer(
        f"<i>{new_event_texts['title']}</i>", parse_mode='HTML',
        reply_markup=save_keyboard(back=None, edit='title', next='description', is_save=None)
    )


@archive_router.callback_query(MarkFilter())
async def mark_visitor(call: CallbackQuery):
    event_id = int(call.data.split(":")[1])
    user_id = int(call.data.split(":")[2])
    action = call.data.split(":")[3]
    user = await GRCUser.objects.get(tg_id=user_id)
    text = f'<a href="tg://user?id={user.tg_id}">{user.first_name}{" " + user.last_name if user.last_name else ""}</a>\n'
    await GRCVisitor.objects.delete(event_id=event_id, tg_id=user_id)
    if action == "delete":
        await call.message.edit_text(
            f'{text}Удалён',
            parse_mode="HTML",
            reply_markup=visitor_keyboard(user.tg_id, event_id)
        )
    elif action == "True":
        await GRCVisitor.objects.create(event_id=event_id, tg_id=user_id, is_online=True)
        await call.message.edit_text(
            f'{text}Указано: онлайн',
            parse_mode="HTML",
            reply_markup=visitor_keyboard(user.tg_id, event_id)
        )
    else:
        await GRCVisitor.objects.create(event_id=event_id, tg_id=user_id, is_online=False)
        await call.message.edit_text(
            f'{text}Указано: оффлайн',
            parse_mode="HTML",
            reply_markup=visitor_keyboard(user.tg_id, event_id)
        )
