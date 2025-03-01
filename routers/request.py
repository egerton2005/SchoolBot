from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from date.bd import BD
from date.state import UsersState


router = Router()

lis_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']


@router.message(Command('timetable'))
async def timetable(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=i)] for i in lis_day])

    await message.answer('Выберите день в котором хотели бы посмотреть рассписание', reply_markup=keyboard)

    await state.set_state(UsersState.day)

@router.message(UsersState.day)
async def choice_day(message: types.Message, state: FSMContext):
    day = message.text
    if(day in lis_day):
        await message.answer(f'Вот ваше расписание на {day}', reply_markup=ReplyKeyboardRemove())
        await message.answer(f'{BD().get_timetable(message.from_user.id, day)}')
        await state.clear()
    else:
        await message.answer(f'Такого дня не существует')



