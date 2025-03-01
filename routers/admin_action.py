from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from filters.filter_admin import AdminFilter, ClassFilter

from date.bd import BD
from date.state import AdminState


router = Router()

lis_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

def check_string(lis):
    if(len(lis) == 3):
        if(lis[0] in ['1', '2', '3', '4', '5', '6', '7'] and lis[2].isdigit()):
            return True
    return False

@router.message(Command('change_timetable'), AdminFilter())
async def choise_action(message: types.Message, state: FSMContext):
    await message.answer('Выберите школу')
    await message.answer(BD().print_all_school()[0])
    await state.set_state(AdminState.school)

@router.message(Command('change_timetable'))
async def choise_action(message: types.Message):
    await message.answer('У вас нет прав, для использования данной комманды')

@router.message(AdminState.school)
async def action(message: types.Message, state: FSMContext):
    schools = message.text
    if(schools in BD().print_all_school()[1]):
        await state.update_data(school=schools)
        await message.answer('Хорошо. Теперь выберите класс запросом типа: "10 А"')
        await message.answer(BD().print_all_class(message.from_user.id)[0])
        await state.set_state(AdminState.clas)
    else:
        await message.answer('В моей базе нет такой школы(')

@router.message(AdminState.clas)
async def action(message: types.Message, state: FSMContext):
    clas = message.text.split()
    res = await state.get_data()
    ans = res.get('school')
    if(ClassFilter(ans, clas)):
        await state.update_data(clas = [clas[0], clas[1]])
        keyboard = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=i)] for i in lis_day])

        await message.answer('Отлично. Теперь выберите день', reply_markup=keyboard)
        await state.set_state(AdminState.day)
    else:
        await message.answer('Такого класса не существует')

@router.message(AdminState.day)
async def action(message: types.Message, state: FSMContext):
    days = message.text
    if(days in lis_day):
        await state.update_data(day = days)
        await message.answer("Чтобы изменить расписание напишите номер предмета в расписании + '.' + Название предмета"
        " + '.' + Номер кабинета\nЕсли нужно изменить, предположим, только 2 урок на русский язык, то напишите:"
        "\n2.Русский язык.314\nА если нужно изменить несколько предметов, напишите тоже самое, но только через 'Enter':"
        "\n2.Русский язык.314\n3.Математика.312\n4.Английский язык.304/305")

        await state.set_state(AdminState.modified_timetable)

    else:
        await message.answer('Такого класс не существует')


@router.message(AdminState.modified_timetable)
async def action(message: types.Message, state: FSMContext):
    txt = message.text.split('\n')
    prov = True
    lis_num = []
    lis_name = []
    lis_cab = []
    for i in txt:
        lis = i.split('.')
        if(not(check_string(lis))):
            prov = False
            break
        else:
            lis_num.append(lis[0])
            lis_name.append(lis[1])
            lis_cab.append((lis[2]))
    res = await state.get_data()
    school = res.get('school')
    clas = res.get('clas')
    day = res.get('day')
    if(prov):
        for i in range(len(txt)):
            BD().change_timetable(school, int(clas[0]), clas[1], day, int(lis_num[i]), lis_name[i], lis_cab[i])
        BD().change_day(school, int(clas[0]), clas[1], day)
        await state.clear()
    else:
        await message.answer('Вы ввели запрос неправильно')