import requests
# сначала надо установить эту либу через pip. "python -m pip install telebot" -> напиши в консольке
import telebot
import datetime
import operator
import collections
# потом надо установить эту либу через pip. "python -m pip install bs4" -> напиши в консольке

from bs4 import BeautifulSoup
from typing import Optional, Tuple, List
# то, что идет в скобочках надо постоянно менять, поищи на hidemyname новые прокси, если эти не работают. Во время теста эти работали
telebot.apihelper.proxy = {'https': 'https://191.238.217.84:80'}
# это коды для каждого дня. Просто человеку удобно писать название дня, а на сайте они через циферки идут
days = {'monday' : 1, 'tuesday' : 2, 'wednesday' : 3,
            'thursday' : 4, 'friday' : 5, 'saturday' : 6, 'sunday' : 7}
# Тут твой API-токен для бота в телеге. Это - ключ к управлению ботом
bot = telebot.TeleBot("921333701:AAEOeeMvCb73EAWScXLj7Cvq4YWfMY1E0TE")

# функция для того, чтобы получить с сайта итмо страницу с расписанием нужной группы для нужной недели
def get_page(group: str, week: str='') -> str:
#  если указали неделю, значит добавим в url номер недели 0 - четная, 1 - нечетная
    if week:
        week = str(week) + '/'
# тут создаем url, по которому будем отправлять запрос для получения страницы
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain="http://www.ifmo.ru/ru/schedule/0/",
        week=week,
        group=group)
# отправляем запрос
    response = requests.get(url)
# берем html - код ответа от сервара
    web_page = response.text
    return web_page

# эта функция создает взаимодействие между пользователем и ботом. commands - все, что может ввести Юзер. Он это вводит в формате /monday и тд
@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_day(message: str) -> None:
# чтобы бот не вылетал при ошибках, заюзаем try/except
    try:
# вытащим из сообщения номер группы (в каком формате идет обращение к боту - написано в мануале
        group = message.text.split()[1]
# вытащим из сообщения день, в который нас интересует расписание
        day = message.text.split()[0][1:]
# вытащим из сообщения то, какая у нас неделя. Четная/нечетная
        week = message.text.split()[2]
# получим код web-страницы, используя функцию, которую описали выше
        web_page = get_page(group, week)
# получим списки с расписанием, корпусами, названиями пар и номерами аудиторий. Это все нам вернет функция, которую мы чуть дальше распишем
        times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(web_page, str(days[day]))
# В воскресение люди отдыхают, поэтому если пользователю нужны пары на воскресенье, скажем об этом
        if days[day] == 7:
            bot.send_message(message.chat.id, 'Это выходной так-то')
            return None
# Если юзер не ввел какие-то данные, то скажем, что он ошибся, но не выключим бота
    except IndexError:
        bot.send_message(message.chat.id, 'Не хватает параметров, вводите все как надо')

# сформируем красивый ответ на запрос пользователя
    resp = ''
    for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
        resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)
# отправим этот ответ и даже поиграем с тегами, которые в него включили
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


# функция для того, чтобы спарсить (вытащить) с html-страницы нужные нам данные
def get_schedule(web_page: str, day: str) -> Tuple[List[str], List[str], List[str], List[str]]:
# создадим парсер
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на нужный нам день
    schedule_table = soup.find("table", attrs={"id": day + "day"})

    # Время проведения занятий
    try:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.replace('\t','').replace('нечетная неделя', '').replace('четная неделя', '').split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        # Номера аудиторий
        aud_list = schedule_table.find_all("td", attrs={"class": "room"})
        aud_list = [aud.dd.text for aud in aud_list]
   # Если нет никаких записей про этот день / какая-то ошибка при попытке найти занятия нужной группы, положим в списки пустые строки
    except:
        times_list = ['']
        locations_list = ['']
        lessons_list = ['']
        aud_list = ['']
# что бы не произошло, мы все равно вернем полученные списки из времени начала/конца пары, корпуса и тд
    finally:
        return times_list, locations_list, lessons_list, aud_list


# функция для получения следующей пары
@bot.message_handler(commands=['near'])
def get_near_lesson(message: str) -> None:
    """ Получить ближайшее занятие """
# Опять же попробуем не ломать бота при ошибках
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
# красиво напишем, где эта пара и какая она
                bot.send_message(message.chat.id, response, parse_mode='HTML')
                return None
# если не нашли сегодня никаких пар, которые должны начаться - говорим, что пар нет
        bot.send_message(message.chat.id, 'Сегодня больше нет пар')
# Если что-то не заработало из-за юзера, сообщим об ошибке
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка')

# функция, чтобы получить пары на завтра
@bot.message_handler(commands=['tommorow'])
def get_tommorow(message: str) -> None:
# юзаем трай
    try:
        """ Получить расписание на следующий день """
# получим информацию о завтрашнем дне
        tommorow = datetime.date.today() + datetime.timedelta(days=1)
# получим номер группы
        group = message.text.split()[1]
# узнаем, четная/нечетная неделя завтра
        week = int(tommorow.strftime("%V")) - int(datetime.date(2019, 9, 1).strftime("%V"))
# получим расписание на завтра
        times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(get_page(group, str(week % 2 + 1)),
                                                                str(tommorow.weekday() + 1 if tommorow.weekday() < 6 else 0))
        resp = ''
# подготовим красивый ответ на запрос пользователя
        for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
            resp += '<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)
# ответим пользователю
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
# Если что-то упало, сообщим об ошибке
    except IndexError:
        bot.send_message(message.chat.id, 'Ошибка')

# функция для получения расписания на всю неделю
@bot.message_handler(commands=['all'])
def get_all_schedule(message: str) -> None:
    try:
        """ Получить расписание на всю неделю для указанной группы """
# получим номер группы из сообщения
        group = message.text.split()[1]
# узнаем четная/нечетная неделя сейчас
        week = datetime.datetime.today().strftime("%V")
        week = int(week) - int(datetime.date(2019, 9, 1).strftime("%V"))
# получим страничку с расписанием этой недели
        page = get_page(group, week)
# создадим парсер для того, чтобы работать с html-страницей
        soup = BeautifulSoup(page, "html5lib")
        resp = ''
# красивенько заюзаем уже готовую функцию для получения расписания на 1 день 6 раз, чтобы получить расписание на неделю
        for name, order in collections.OrderedDict(sorted(days.items(), key=lambda kv: kv[1])).items():
             if order == 7:
                 break
             times_lst, locations_lst, lessons_lst, aud_lst = get_schedule(page, str(order))
             for time, location, lession, aud in zip(times_lst, locations_lst, lessons_lst, aud_lst):
                resp += '<b>'+name.upper() + '</b>:\n<b>{}</b>, {}, {}, {}\n'.format(time, location, lession, aud)
# отправим красиво оформленный ответ пользователю
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except IndexError:
        bot.send_message(message.chat.id, 'Не хватает параметров, сверьтесь с мануалом')

if __name__ == '__main__':
    bot.polling()