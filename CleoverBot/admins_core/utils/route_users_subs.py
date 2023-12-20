from aiogram.fsm.state import StatesGroup, State


class UserSubscribeRoute(StatesGroup):
    GET_ID_FOR_ADD_SUB = State()
    GET_END_DATE_FOR_SUB = State()
    GET_ID_FOR_DELETE_SUB = State()
