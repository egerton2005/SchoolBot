from aiogram.filters import BaseFilter
from aiogram import types
from date.bd import BD

class RegFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message):
        return not(BD().check_user(message.from_user.id))

class NumStep(BaseFilter):
    def __init__(self, step):
        self.step = step

    async def __call__(self, message: types.Message):
        return BD().get_step(message.from_user.id) == self.step

