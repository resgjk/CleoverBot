from aiogram.fsm.state import StatesGroup, State


class NewsForm(StatesGroup):
    GET_TITLE = State()
    GET_DESCRIPTION = State()
    GET_MEDIA_FILES = State()
    SEND_NEWS_TO_USERS = State()
