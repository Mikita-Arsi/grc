import logging
import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from config import token, webhook_url
from init_db import ormar_base_config
from bot.routers import register_base_handlers


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

WEBHOOK_PATH = "/bot"
WEBHOOK_URL = webhook_url + WEBHOOK_PATH

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    register_base_handlers(dp)
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    logger.info("App started")
    yield
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
    await bot.session.close()
    logger.info("App stopped")

app = FastAPI(lifespan=lifespan)
ormar_base_config.metadata.create_all(ormar_base_config.engine)
app.state.database = ormar_base_config.database


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    telegram_update = types.Update(**update)
    try:
        await dp.feed_update(bot=bot, update=telegram_update)
    except Exception as e:
        logging.error(e, exc_info=e)


def main():
    while True:
        try:
            uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
