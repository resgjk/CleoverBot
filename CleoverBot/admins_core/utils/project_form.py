from aiogram.fsm.state import StatesGroup, State


class ProjectForm(StatesGroup):
    CHOISE_CATEGORY = State()
    GET_TITLE = State()
    GET_DESCRIPTION = State()
    GET_LINKS = State()
    GET_MEDIA = State()
    SAVE_MEDIA_AND_SHOW_PROJECT = State()
    SAVE_AND_SEND_NOTIF = State()
