import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from date.bd import BD
from time import time

logging.basicConfig(level=logging.INFO)
bot = Bot(token='')

import routers.registr
import routers.request
import routers.admin_action

dp = Dispatcher()

dp.include_router(routers.admin_action.router)
dp.include_router(routers.registr.router)
dp.include_router(routers.request.router)

async def distributor():
    while(True):
        await asyncio.sleep(2)
        dic = BD().get_all_users_change_timetable()
        for i in dic:
            txt = BD().get_timetable(i, dic[i])
            await bot.send_message(i, txt)
        BD().set_change_day([i for i in dic])

async def bot_on():
    await dp.start_polling(bot)


async def main():
    distr = asyncio.create_task(distributor())
    bots = asyncio.create_task(bot_on())

    await distr
    await bots


if __name__ == '__main__':
    asyncio.run(main())
