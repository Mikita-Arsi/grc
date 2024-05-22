from abc import ABC

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .const import main_chat_id, admin_chat_id
from .states import EventEditorStates


class AdminFilter(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        chat_member = await bot.get_chat_member(admin_chat_id, message.from_user.id)
        return chat_member.status != ChatMemberStatus.LEFT


class PrivateMessageFilter(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.chat.id == message.from_user.id


class ChatMessageFilter(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.chat.id == main_chat_id


class ChatMemberFilter(Filter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        chat_member = await bot. get_chat_member(main_chat_id, message.from_user.id)
        return chat_member.status != ChatMemberStatus.LEFT


class EventCreatorStateFilter(Filter):
    async def __call__(self, message: Message, bot: Bot, state: FSMContext) -> bool:
        return (await state.get_state()) in EventEditorStates.__all_states__


class EventCreatorCallbackFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'event_creator' and 'save' not in call.data


class SaveEventFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data == 'event_creator:save'


class ArchiveCallbackFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'archive'


class CreatorFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'creator'


class ViewFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'view'


class StepArchiveFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'step'


class ProtocolFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'protocol'


class AddFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'add'


class EditFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'edit'


class DeleteFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'delete'


class VisitorFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'visitor'


class RulesFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'rules'


class ArchiveMarkFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[-1] == 'mark'


class MarkFilter(Filter):
    async def __call__(self, call: CallbackQuery, bot: Bot) -> bool:
        return call.data.split(':')[0] == 'mark'

