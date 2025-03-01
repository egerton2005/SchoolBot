from aiogram.filters import BaseFilter
from aiogram import types
from date.bd import BD
from date.state import AdminState

class AdminFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message):
        return message.from_user.id in BD().get_admin()



def ClassFilter(school, lis):
    dic = BD().print_all_class_for_school(school)[1]
    if (len(lis) == 2 and lis[0].isdigit()):
        return lis[1] in dic.get(int(lis[0]), [])
    return False

# class AdminClassFilter(BaseFilter):
#     def __init__(self):
#         pass
#
#     async def prov(self, lis, dic):
#             if (len(lis) == 2 and lis[0].isdigit()):
#                 return lis[1] in dic.get(int(lis[0]), [])
#             return False
#
#     async def __call__(self, message: types.Message):
#         return message.text in BD().print_all_class_for_school(AdminState.get_data(''))


