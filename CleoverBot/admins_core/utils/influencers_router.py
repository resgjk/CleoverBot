from aiogram.fsm.state import StatesGroup, State


class InfluencerRouter(StatesGroup):
    GET_ID_FOR_ADD_INFL = State()
    GET_INFL_TYPE = State()
