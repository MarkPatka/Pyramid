import pandas as pd
import requests
import textwrap
from config import *
from pandas.io.json import json_normalize
from string import Template



def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=100,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get 
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """    
    code = """return API.wall.get({
        "owner_id": '%s',
        "domain": '%s',
        "offset": %s,
        "count": %s,
        "filter": '%s',
        "extended": %s,
        "fields": '%s',
        "v": "%s"
    });""" % (owner_id, domain, offset, count, filter, extended, fields, v) # форматирование строки

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": access_token,
                "v": "5.103"
            }
    )
    posts = response.json()['response']['items'] # получили посты
    listofposts = [post["text"] for post in posts] # взяли текст постов
    data = pd.DataFrame(listofposts) 
    return data


if __name__ == "__main__":
    data = get_wall(domain="pn6")
    data.to_csv("data.csv")
