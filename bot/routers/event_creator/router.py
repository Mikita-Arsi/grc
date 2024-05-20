import os

from datetime import datetime

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from bot.filters import (
    AdminFilter,
    PrivateMessageFilter,
    EventCreatorCallbackFilter,
    EventCreatorStateFilter,
    SaveEventFilter
)
from bot.states import EventEditorState
from db import GRCEventCreator, GRCEvent
from bot.texts import new_event_title_text, new_event_texts, event_constructor, steps
from .keyboards import save_keyboard, cancel_keyboard


event_creator_router = Router(name="event_creator")


@event_creator_router.callback_query(EventCreatorCallbackFilter())
async def step_manage(call: CallbackQuery, bot: Bot, state: FSMContext):
    step = call.data.split(':')[1]
    action = call.data.split(':')[2]
    await state.set_state(EventEditorState.__dict__[step])
    event_creator = await GRCEventCreator.objects.first()
    points = event_creator.__dict__
    points["img"] = "img.png" if os.path.exists("img.png") else None

    if not points[step] is None and action != 'edit':
        back_step = steps[steps.index(step) - 1] if steps.index(step) > 0 else None
        next_step = steps[steps.index(step) + 1] if steps.index(step) < 6 else None
        is_save = next_step is None
        await call.message.edit_text(
            f"<i>{new_event_texts[step]}</i>",
            parse_mode='HTML',
            reply_markup=save_keyboard(back=back_step, edit=step, next=next_step, is_save=is_save)
        )
    else:
        if step == 'img':
            await call.message.edit_text(
                f"Отправьте {new_event_texts[step].replace('дата', 'дату').replace('ссылка', 'ссылку')}",
                reply_markup=cancel_keyboard(step)
            )
        else:
            await call.message.edit_text(
                f"Введите {new_event_texts[step].replace('дата', 'дату').replace('ссылка', 'ссылку')}",
                reply_markup=cancel_keyboard(step)
            )


@event_creator_router.callback_query(SaveEventFilter())
async def save_event(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    new_event = (await GRCEventCreator.objects.first()).__dict__
    del new_event['id']
    await GRCEvent.objects.create(**new_event)
    await call.message.answer("Собрание успешно сохранено")
    await GRCEventCreator.objects.delete(id=1)
    await GRCEventCreator.objects.create(id=1)


@event_creator_router.message(AdminFilter(), PrivateMessageFilter(), Command(commands=['new_event']))
async def create_event(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(EventEditorState.title)
    await message.answer(f"Введите {new_event_title_text}")


@event_creator_router.message(AdminFilter(), PrivateMessageFilter(), EventCreatorStateFilter())
async def edit_param(message: Message, bot: Bot, state: FSMContext):
    state = await state.get_state()
    step = state.split(':')[1]
    if step == 'datetime':
        try:
            dt = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
            await GRCEventCreator.objects.filter(id=1).update(datetime=dt)
        except ValueError:
            return await message.answer("Неверный формат даты и времени, повторите попытку")
    elif step == 'img':
        await bot.download(file=message.photo[-1].file_id, destination=f"img.png")
    else:
        await GRCEventCreator.objects.filter(id=1).update(**{step: message.text})
    event_creator = await GRCEventCreator.objects.first()
    if os.path.exists("img.png"):
        await message.answer_photo(
            FSInputFile("img.png", "img.png"),
            caption=event_constructor(**event_creator.__dict__),
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    else:
        await message.answer(
            event_constructor(**event_creator.__dict__),
            parse_mode='HTML',
            disable_web_page_preview=True)
    back_step = steps[steps.index(step) - 1] if steps.index(step) > 0 else None
    next_step = steps[steps.index(step) + 1] if steps.index(step) < 6 else None
    is_save = next_step is None
    await message.answer(
        f"<i>{new_event_texts[step]}</i>", parse_mode='HTML',
        reply_markup=save_keyboard(back=back_step, edit=step, next=next_step, is_save=is_save)
    )
