from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    full_name = State()
    age = State()
    city = State()
    target_weight_loss = State()
    phone = State()
