from aiogram import Dispatcher

from .event_creator import event_creator_router
from .chat import chat_router
from .archive import archive_router


def register_base_handlers(dp: Dispatcher) -> None:
    dp.include_router(event_creator_router)
    dp.include_router(chat_router)
    dp.include_router(archive_router)
