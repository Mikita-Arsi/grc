from aiogram.fsm.state import State, StatesGroup


class EventEditorState(StatesGroup):
    title = State()
    description = State()
    themes = State()
    datetime = State()
    location = State()
    location_url = State()
    img = State()


ProtocolEditorState = State()