from aiogram import types, Router
from aiogram.filters.command import Command
from filters.filter_registr import RegFilter, NumStep
from date.bd import BD

router = Router()

def prov_reg_2(lis, dic):
    if(len(lis) == 2 and lis[0].isdigit()):
        return lis[1] in dic.get(int(lis[0]), [])
    return False

@router.message(Command(commands='start'))
async def start(message: types.Message):
    await message.answer('Начало регестрации')
    if(BD().check_user(message.from_user.id)):
        BD().data_reset(message.from_user.id)
    else:
        BD().add_user(message.from_user.id)
    await message.answer('Выберите свою школу')
    await message.answer(BD().print_all_school()[0])

@router.message(RegFilter())
async def prov_reg(message: types.Message):
    await message.answer("Вы еще не прошли регестрацию.\nПожалуйста, введите комманду '/start' и зарегестрируйтесь")


@router.message(NumStep(0))
async def reg_1(message: types.Message):
    school_name = message.text
    if(school_name in BD().print_all_school()[1]):
        BD().update_user_school(message.from_user.id, school_name)
        await message.answer('А теперь выберите свой класс запросом типа: "10 А"')
        await message.answer(BD().print_all_class(message.from_user.id)[0])
    else:
        await message.answer('В моей базе нет такой школы(')

@router.message(NumStep(1))
async def reg_2(message: types.Message):
    lis_class = message.text.split()
    if(prov_reg_2(lis_class, BD().print_all_class(message.from_user.id)[1])):
        BD().update_user_class(message.from_user.id, lis_class[0], lis_class[1])
        await message.answer('Регистрация завершена, поздравляю!')
    else:
        await message.answer('Такого класса не существует')

