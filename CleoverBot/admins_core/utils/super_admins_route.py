from aiogram.fsm.state import StatesGroup, State


class SuperAdminRoute(StatesGroup):
    GET_ID_FOR_ADD_ADMIN = State()
    GET_ID_FOR_DELETE_ADMIN = State()
