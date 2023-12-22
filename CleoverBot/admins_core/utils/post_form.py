from aiogram.fsm.state import StatesGroup, State


class PostForm(StatesGroup):
    GET_TITLE = State()
    GET_CATEGORY = State()
    GET_BANK = State()
    GET_START_DATE = State()
    GET_START_TIME = State()
    GET_END_DATE = State()
    GET_END_TIME = State()
    GET_SHORT_DESCRIPTION = State()
    GET_FULL_DESCRIPTION = State()
    GET_MEDIA_FILES = State()
    SEND_POST_TO_USERS = State()
