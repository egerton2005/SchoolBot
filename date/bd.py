import sqlite3

class BD:
    def __init__(self):
        pass

    def check_user(self, id):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            prov = cur.execute(f"SELECT user_id FROM user").fetchall()
            flag = False
            for i in range(len(prov)):
                if (prov[i][0] == id):
                    flag = True
                    break
            return flag

    def add_user(self, id):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO user (user_id) VALUES({id})")

    def data_reset(self, id):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            cur.execute(f'UPDATE user SET school_id = NULL, class_id = NULL, day_change = NULL WHERE user_id = {id}')

    def update_user_school(self, id, school):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT id FROM school WHERE name_school = '{school}'").fetchone()[0]
            cur.execute(f'UPDATE user SET school_id = {school_id} WHERE user_id = {id}')

    def update_user_class(self, id, clas, lit):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT school_id FROM user WHERE user_id = {id}").fetchone()[0]
            class_id = cur.execute(f"SELECT id FROM list_class WHERE school_id = {school_id} AND number_class = {clas} AND lit_class = '{lit}'").fetchone()[0]
            cur.execute(f'UPDATE user SET class_id = {class_id} WHERE user_id = {id}')

    def get_all_users_change_timetable(self):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            lis_user = cur.execute(f"SELECT user_id, day_change FROM user WHERE day_change <> 'NULL'").fetchall()
            dic_res = {}
            for i in lis_user:
                dic_res[i[0]] = i[1]
            return dic_res


    def get_admin(self):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            all_id = cur.execute(f"SELECT user_id FROM admin").fetchall()
            lis_id = []
            for i in all_id:
                lis_id.append(i[0])
            return lis_id

    def get_timetable(self, id, day):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            class_id = cur.execute(f"SELECT class_id FROM user WHERE user_id = {id}").fetchone()[0]
            school_id = cur.execute(f"SELECT school_id FROM user WHERE user_id = {id}").fetchone()[0]
            res = cur.execute(f"SELECT number_lesson, lesson, cabinet FROM timetable_lesson WHERE day_week = '{day}' AND school_id = {school_id} AND class_id = {class_id}")
            string = ''
            for i in res:
                string += " ".join(map(str, i)) + '\n'
            return string

    def change_day(self, school, clas, lit, day):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT id FROM school WHERE name_school = '{school}'").fetchone()[0]
            class_id = cur.execute(
                    f"SELECT id FROM list_class WHERE school_id = {school_id} AND number_class = {clas} AND lit_class = '{lit}'").fetchone()[0]
            cur.execute(
                    f"UPDATE user SET day_change = '{day}' WHERE school_id = {school_id} AND class_id = {class_id}")

    def set_change_day(self, lis):
        with sqlite3.connect(
                r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            for i in lis:
                cur.execute(f"UPDATE user SET day_change = 'NULL' WHERE user_id = {i}")

    def change_timetable(self, school, clas, lit, day, num, les, cab):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT id FROM school WHERE name_school = '{school}'").fetchone()[0]
            class_id = cur.execute(f"SELECT id FROM list_class WHERE school_id = {school_id} AND number_class = {clas} AND lit_class = '{lit}'").fetchone()[0]
            cur.execute(
                    f"UPDATE timetable_lesson SET lesson = '{les}', cabinet = '{cab}' WHERE day_week = '{day}' AND class_id = {class_id} AND number_lesson = {num}")


    def print_all_school(self):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_lis = cur.execute(f"SELECT name_school FROM school").fetchall()
            string = ''
            lis_school = []
            for i in school_lis:
                lis_school.append(i[0])
                string += " ".join(map(str, i)) + '\n'
            return string, lis_school


    def print_all_class(self, id):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT school_id FROM user WHERE user_id = {id}").fetchone()[0]
            lis_num_class = cur.execute(f"SELECT number_class FROM list_class WHERE school_id = {school_id}").fetchall()
            res_dic = {}
            string = ''
            for i in lis_num_class:
                i = i[0]
                if(not(i in res_dic)):
                    lis_lit_class = cur.execute(
                            f"SELECT lit_class FROM list_class WHERE school_id = {school_id} AND number_class = {i}").fetchall()
                    lis_lit_class = [j[0] for j in lis_lit_class]
                    res_dic[i] = lis_lit_class
                    txt = ''
                    for j in lis_lit_class:
                        txt += j + ' '
                    string += f'{i}: {txt}\n'
            return string, res_dic

    def print_all_class_for_school(self, school):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT id FROM school WHERE name_school = '{school}'").fetchone()[0]
            lis_num_class = cur.execute(f"SELECT number_class FROM list_class WHERE school_id = {school_id}").fetchall()
            res_dic = {}
            string = ''
            for i in lis_num_class:
                i = i[0]
                if(not(i in res_dic)):
                    lis_lit_class = cur.execute(
                            f"SELECT lit_class FROM list_class WHERE school_id = {school_id} AND number_class = {i}").fetchall()
                    lis_lit_class = [j[0] for j in lis_lit_class]
                    res_dic[i] = lis_lit_class
                    txt = ''
                    for j in lis_lit_class:
                        txt += j + ' '
                    string += f'{i}: {txt}\n'
            return string, res_dic

    def get_step(self, id):
        with sqlite3.connect(r'C:\Users\днс\Desktop\program\python\_tg_bots_\проект чат-бот переделка\db_school_bot_2.db') as con:
            cur = con.cursor()
            school_id = cur.execute(f"SELECT school_id FROM user WHERE user_id = {id}").fetchone()[0]
            class_id = cur.execute(f"SELECT class_id FROM user WHERE user_id = {id}").fetchone()[0]

            if(school_id == None):
                return 0
            elif(class_id == None):
                return 1
            else:
                return 2

