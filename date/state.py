from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class UsersState(StatesGroup):
    day = State()

class AdminState(StatesGroup):
    school = State()
    clas = State()
    day = State()
    modified_timetable = State()
