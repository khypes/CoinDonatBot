from aiogram.fsm.state import State, StatesGroup


class Checkout(StatesGroup):
    payment_method = State()
    receipt_upload = State()
