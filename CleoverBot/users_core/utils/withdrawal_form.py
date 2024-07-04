from aiogram.fsm.state import StatesGroup, State


class WithdrawalForm(StatesGroup):
    GET_WALLET_ADDRESS = State()
