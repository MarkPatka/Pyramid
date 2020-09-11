from api import *
import numpy as np
from igraph import Graph, plot
from igraph import Graph, plot
import numpy as np
import igraph

# Получим граф отношений пользователей
def get_network(users_ids, as_edgelist=True):
    vertices = ['me']
    edges = []
    ids = []
    cipher = {}

    for user_id in users_ids['response']['items']:
# получим имя пользователя и фамилию из словаря
        name = user_id['first_name'] + user_id['last_name']
# получим id из словаря
        user_id = user_id['id']
# кинем id в список айдишек
        ids.append(user_id)
# отметим соответствие между айди и именем (чтобы удобней было ориентироваться)
        cipher.update({user_id : len(cipher.keys()) + 1})
# в список вершин добавим имя этого пользователя
        vertices.append(name)
# посмотрим друзей этого пользователя и проверим, нет ли их в уже данном нам списке
    for user_id in users_ids['response']['items']:
        user_id = user_id['id']
        edges.append((0, cipher[user_id]))
        friends = get_friends(user_id, 'sex')
        try:
            for friend in friends['response']['items']:
                lable = friend['id']
# если такой человек есть, значит обозначим связь между двумя людьми. Связь у нас - ребро

                if lable in ids:

                    edges.append((cipher[user_id], cipher[lable]))

        except:
            pass
# если просят вернуть список ребер, то просто его вернем
    if as_edgelist:
        print(edges)
# если нужна матрица смежности, перестроим список ребер в нее
    else:
        n = max(max(i, j) for i, j in edges)
        matrix = np.zeros((n, n))
        for i, j in edges:
            matrix[i-1][j-1] = 1
        for row in matrix:
            print(row)
# создадим граф из библиотеки Igraph
    g = Graph(vertex_attrs={"label":vertices},
            edges=edges, directed=False)
# получим его примерный размер, чтобы знать, как его изобразить
    N = len(vertices)
# подготовимся красиво выводить граф
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
    maxiter=1000,
    area=N**3,
    repulserad=N**3)
# удалим все петли из графа и все циклы
    g.simplify(multiple=True, loops=True)
# нарисуем граф (может занять много минут
    plot_graph(g, visual_style)

# функция для рисования графа
def plot_graph(g, visual_style):
# найдем сообщества в графе
    communities = g.community_edge_betweenness(directed=False)
# кластеризуем граф. То есть, посмотрим, сколько можно кластеров/сообществ найти в графе
    clusters = communities.as_clustering()
#  выведем все кластеры. Обычно это просто, кто с кем связан. Если переводить на язык вк, то кто у кого в друзьях
    print(clusters)
# цветовая гамма для всех кластеров. Пусть новый кластер - новый цвет
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
# нарисуем граф
    plot(g, **visual_style)


if __name__ == '__main__':
    get_network(get_friends(user_id, 'sex'), True)
