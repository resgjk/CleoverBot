from aiogram.fsm.state import StatesGroup, State


class FeedbackForm(StatesGroup):
    GET_FEEDBACK = State()
