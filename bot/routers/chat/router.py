from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery, ChatPermissions, ChatMember
from asyncpg import UniqueViolationError

from db import GRCEvent, GRCVisitor, GRCUser
from .keyboards import visit_keyboard, new_member_keyboard, rules_keyboard
from ...texts import event_constructor
from ...const import forum_id, main_chat_id
from ...filters import VisitorFilter, AdminFilter, ChatMessageFilter, RulesFilter, ChatMemberFilter

chat_router = Router(name="chat")


@chat_router.message(AdminFilter(), Command("publish_event"))
async def publish_event(message: Message):
    now = datetime.now()
    events = await GRCEvent.objects.all()
    try:
        current_timedelta = min(
            ev.datetime - now for ev in events if ev.datetime - now > timedelta(0, 0, 0, 0, 0, 0, 0)
        )
    except ValueError:
        await message.answer(
            "Будущих собраний пока не запланировано"
        )
        return
    current_event = await GRCEvent.objects.get(datetime=(now + current_timedelta))
    msg = await message.bot.send_photo(
        caption=event_constructor(**current_event.__dict__),
        photo=FSInputFile("img.png", "img.png"),
        chat_id=main_chat_id,
        message_thread_id=forum_id,
        parse_mode="HTML",
        reply_markup=visit_keyboard(current_event.id)
    )
    await message.bot.pin_chat_message(
        chat_id=main_chat_id,
        message_id=msg.message_id
    )


@chat_router.message(ChatMemberFilter(), Command(commands=['rules', 'правила']))
async def show_rules(message: Message):
    await message.reply(
        "Правила great.russian.club",
        reply_markup=rules_keyboard()
    )


@chat_router.message(F.new_chat_members, ChatMessageFilter())
async def repost_event(message: Message):
    await message.bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        ChatPermissions(can_send_messages=False)
    )

    await message.answer(
        f"""<a href="tg://user?id={
            message.from_user.id
            }">{
                message.from_user.full_name
            }</a>, для получения возможности писать сообщения в чате ознакомьтесь с нашими правилами""",
        parse_mode="HTML",
        reply_markup=new_member_keyboard(message.from_user.id)
    )

    now = datetime.now()
    events = await GRCEvent.objects.all()
    try:
        current_timedelta = min(
            ev.datetime - now for ev in events if ev.datetime - now > timedelta(0, 0, 0, 0, 0, 0, 0)
        )
    except ValueError:
        return
    current_event = await GRCEvent.objects.get(datetime=(now + current_timedelta))

    msg = await message.bot.send_photo(
        caption=event_constructor(**current_event.__dict__),
        photo=FSInputFile("img.png", "img.png"),
        chat_id=message.chat.id,
        message_thread_id=forum_id,
        parse_mode="HTML",
        reply_markup=visit_keyboard(current_event.id)
    )
    await message.bot.pin_chat_message(
        chat_id=msg.chat.id,
        message_id=msg.message_id
    )


@chat_router.callback_query(RulesFilter())
async def read_rules(call: CallbackQuery):
    if call.from_user.id == int(call.data.split(":")[-1]):
        await call.message.bot.restrict_chat_member(
            call.message.chat.id,
            call.from_user.id,
            ChatPermissions(can_send_messages=True)
        )
        await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await call.answer("Эта кнопка не для тебя")


@chat_router.callback_query(VisitorFilter())
async def write_visitor(call: CallbackQuery):
    try:
        await GRCUser.objects.create(
            tg_id=call.from_user.id,
            username=call.from_user.username,
            first_name=call.from_user.first_name,
            last_name=call.from_user.last_name,
            join_date=datetime.now()
        )
    except UniqueViolationError:
        pass
    event_id = int(call.data.split(":")[1])
    is_online = call.data.split(":")[-1] == 'online'
    visitor = await GRCVisitor.objects.get_or_none(
        tg_id=call.from_user.id,
        event_id=event_id
    )
    if visitor:
        if visitor.is_online != is_online:
            await visitor.upsert(is_online=is_online)
            await call.answer(
                "Вы изменили формат посещения",
                show_alert=True
            )
        else:
            await call.answer(
                "Вы уже указали этот формат посещения",
                show_alert=True
            )
    else:
        await GRCVisitor.objects.create(
            tg_id=call.from_user.id,
            event_id=event_id,
            is_online=is_online
        )
        await call.answer(
            "Вы успешно записаны",
            show_alert=True
        )
