from aiogram.fsm.state import StatesGroup, State


class CategoryForm(StatesGroup):
    GET_TITLE = State()
    GET_DESCRIPTION = State()
    GET_MEDIA = State()
    SAVE_MEDIA_AND_SHOW_CATEGORY = State()
    SAVE_IN_DB = State()


class CategoryDeleteField(StatesGroup):
    GET_TITLE = State()
