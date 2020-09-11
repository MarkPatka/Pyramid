import requests
import telebot
import datetime
import operator
import collections


from bs4 import BeautifulSoup
from typing import Optional, Tuple, List

telebot.apihelper.proxy = {'https': 'https://185.80.130.50:80'}
days = {'monday' : 1, 'tuesday' : 2, 'wednesday' : 3,
            'thursday' : 4, 'friday' : 5, 'saturday' : 6, 'sunday' : 7}

#API - токен.
bot = telebot.TeleBot("921333701:AAEOeeMvCb73EAWScXLj7Cvq4YWfMY1E0TE")


def get_page(group: str, week: str='') -> str:
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain="http://www.ifmo.ru/ru/schedule/0/",
        week=week,
        group=group)
    response = requests.get(url) #Библиотека выполн. rest-запросов (get, post, put, delete... запросы web-у)
    web_page = response.text
    return web_page


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']) # В телеботе имеется ф. хендлер, при вводе соотв. комманд выполн. след. указ. функцию get_day
def get_day(message: str) -> None:
    try:
        group = message.text.split()[1]
        day = message.text.split()[0][1:]
        week = message.text.split()[2]
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(web_page, str(days[day]))
        if days[day] == 7:
            bot.send_message(message.chat.id, 'Это выходной так-то')
            return None
    except IndexError:
        bot.send_message(message.chat.id, 'Не хватает параметров, вводите все как надо')
    

    resp = ''
    for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
        resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


def get_schedule(web_page: str, day: str) -> Tuple[List[str], List[str], List[str], List[str]]:
    
    soup = BeautifulSoup(web_page, "html5lib")
    schedule_table = soup.find("table", attrs={"id": day + "day"})
    
    try:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]
        
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]
        
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.replace('\t','').replace('нечетная неделя', '').replace('четная неделя', '').split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
        
        aud_list = schedule_table.find_all("td", attrs={"class": "room"})
        aud_list = [aud.dd.text for aud in aud_list]
    except:
        times_list = ['']
        locations_list = ['']
        lessons_list = ['']
        aud_list = ['']
    finally:
        return times_list, locations_list, lessons_list, aud_list


# функция для получения следующей пары
@bot.message_handler(commands=['near'])
def get_near_lesson(message: str) -> None:
    """ Получить ближайшее занятие """
    try:
# получим из сообщения номер группы
        group = message.text.split()[1]
# узнаем, какой у этой недели номер в году
        week = datetime.datetime.today().strftime("%V")
        now = datetime.datetime.now()
# посмотрим, какая она по счету в учебном году (просто узнаем, сколько недель прошло с первого сентября)
        week = int(week) - int(datetime.date(2019, 9, 1).strftime("%V"))
# получим расписание на нужную нам неделю (четную/нечетную)
        times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(get_page(group, str(week % 2 + 1)), str(datetime.datetime.today().weekday() + 1))
# узнаем, сколько сейчас времени
        curr_time = now.strftime("%H:%M")
# пройдемся по списку из времени начала пар и посмотрим, какая пара будет следующей
        for iterator in range(len(times_lst)):
            time = times_lst[iterator]
# следующая пара начинается во время, которое больше (наступит позже), чем сейчас
            if curr_time < time.split('-')[0]:
                response = '<b>{}</b>, {}, {}, {}\n'.format(times_lst[iterator],
                                                        locations_lst[iterator],
                                                        lessons_lst[iterator],
                                                        aud_lst[iterator])
                bot.send_message(message.chat.id, response, parse_mode='HTML')
                return None
        bot.send_message(message.chat.id, 'Сегодня больше нет пар')
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка')


# функция, чтобы получить пары на завтра
@bot.message_handler(commands=['tommorow'])
def get_tommorow(message: str) -> None:
    try:
        tommorow = datetime.date.today() + datetime.timedelta(days=1)
        group = message.text.split()[1]
        week = int(tommorow.strftime("%V")) - int(datetime.date(2019, 9, 1).strftime("%V"))
        times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(get_page(group, str(week % 2 + 1)),
                                                                str(tommorow.weekday() + 1 if tommorow.weekday() < 6 else 0))
        resp = ''
        for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка')

# функция для получения расписания на всю неделю
@bot.message_handler(commands=['all'])
def get_all_schedule(message: str) -> None:
    try:
        group = message.text.split()[1]
        week = datetime.datetime.today().strftime("%V")
        week = int(week) - int(datetime.date(2019, 9, 1).strftime("%V"))
        page = get_page(group, week)
        soup = BeautifulSoup(page, "html5lib")
        resp = ''
        for name, order in collections.OrderedDict(sorted(days.items(), key=lambda kv: kv[1])).items(): # Сортируем дни(+номер дня) по возрастанию
             if order == 7:
                 break
             times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(page, str(order))
             for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
                resp += '<b>'+name.upper() + '</b>:\n<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)
        
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except IndexError:
        bot.send_message(message.chat.id, 'Не хватает параметров, сверьтесь с мануалом')


if __name__ == '__main__':
    bot.polling()