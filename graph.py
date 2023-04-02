import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from numpy import inf

path = []
G = nx.MultiDiGraph()

G.add_nodes_from([
    ("1", {"heuristics": 0}),
    ("2", {"heuristics": 0}),
    ("3", {"heuristics": 0}),
    ("4", {"heuristics": 0}),
    ("5", {"heuristics": 0}),
    ("6", {"heuristics": 0}),
    ("7", {"heuristics": 0}),
    ("8", {"heuristics": 0}),
    ("9", {"heuristics": 0}),
    ("10", {"heuristics": 0}),
    ("11", {"heuristics": 0}),
    ("12", {"heuristics": 0}),
    ("13", {"heuristics": 0}),
    ("14", {"heuristics": 0}),
    ("15", {"heuristics": 0}),
])

G.add_edges_from([
    ("1", "2", {"weight": 10}),
    ("1", "3", {"weight": 12}),
    ("1", "5", {"weight": 23}),
    ("2", "4", {"weight": 14}),
    ("2", "5", {"weight": 6}),
    ("2", "6", {"weight": 18}),
    ("3", "4", {"weight": 4}),
    ("3", "5", {"weight": 20}),
    ("3", "7", {"weight": 34}),
    ("4", "6", {"weight": 26}),
    ("4", "7", {"weight": 7}),
    ("4", "9", {"weight": 40}),
    ("5", "6", {"weight": 7}),
    ("5", "7", {"weight": 10}),
    ("5", "8", {"weight": 23}),
    ("6", "8", {"weight": 3}),
    ("6", "12", {"weight": 14}),
    ("7", "10", {"weight": 6}),
    ("8", "10", {"weight": 1}),
    ("8", "12", {"weight": 8}),
    ("9", "10", {"weight": 5}),
    ("9", "13", {"weight": 8}),
    ("10", "11", {"weight": 1}),
    ("10", "13", {"weight": 4}),
    ("11", "12", {"weight": 4}),
    ("11", "15", {"weight": 9}),
    ("12", "14", {"weight": 6}),
    ("12", "15", {"weight": 4}),
    ("13", "14", {"weight": 3}),
    ("14", "15", {"weight": 6}),
])


def draw_path():
    tmp_paar_path = []
    for i in range(len(path) - 1):
        tmp_paar_path.append(path[i])
        tmp_paar_path.append(path[i + 1])
    tmp_paar_path = np.array(tmp_paar_path).reshape(-1, 2)
    # print(tmp_paar_path)

    tmp_edge_array = []
    for u, v, d in G.edges:
        tmp_edge_array.append(u)
        tmp_edge_array.append(v)
    tmp_edge_array = np.array(tmp_edge_array).reshape(-1, 2)
    # print(tmp_edge_array)

    if len(path) > 0:
        edge_colors = []
        for u1, v1 in tmp_edge_array:
            flag = 0
            for u2, v2 in tmp_paar_path:
                if u1 == u2 and v1 == v2:
                    flag = 1
                else:
                    pass
            edge_colors.append(flag)
        return np.array(edge_colors)
    else:
        return np.full(len(G.edges), 0)


def draw_graph():
    pos = nx.shell_layout(G)

    node_labels = {n: (d["heuristics"]) for n, d in G.nodes(data=True)}
    edge_labels = {(u, v): (d["weight"]) for u, v, d in G.edges(data=True)}

    edge_colors = draw_path()

    nx.draw(G, pos, with_labels=True, node_size=200, node_color="pink", font_size=10, width=1, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="maroon", font_size=6)
    # for i in pos:
    #     pos[i] -= 0.002
    # nx.draw_networkx_labels(G, pos, font_color="green", font_size=20)
    # for i in pos:
    #     pos[i] += 0.005
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_color="maroon", font_size=20)
    # plt.legend(path)
    # plt.show()


def a_star(start, goal):
    h = {n: (d["heuristics"]) for n, d in G.nodes(data=True)}  # cловарь эвристики; ключ - название вершины
    d = {(u, v): (d["weight"]) for u, v, d in G.edges(data=True)}  # словарь весов; ключ - название двух вершин

    Q = list()  # множество вершин, которые требуется рассмотреть
    U = list()  # множество рассмотренных вершин
    f = h  # значение эвристической функции "расстояние + стоимость" для вершины x
    g = h  # стоимость пути от начальной вершины до x
    parents = {}

    # обнуляю значения в словарях
    for k, v in g.items():
        f[k] = 0
        g[k] = 0

    Q.append(str(start))
    g[str(start)] = 0
    parents[str(start)] = start

    while len(Q) > 0:
        current = None

        for v in Q:
            if (current == None) or (g[v] + h[v] < g[current] + h[current]):
                current = v

        if (current == goal) or (G[current] == None):
            pass
        else:
            for v in list(G.neighbors(current)):
                if v not in Q and v not in U:
                    Q.append(v)
                    parents[v] = current
                    g[v] = g[current] + d[current, v]
                else:
                    if g[v] > g[current] + d[current, v]:
                        g[v] = g[current] + d[current, v]
                        parents[v] = current

                        if v in U:
                            U.remove(v)
                            Q.append(v)

        if current == None:
            print('Путь не существует.')
            return None

        if current == goal:
            path.clear()

            while parents[current] != current:
                path.append(current)
                current = parents[current]

            path.append(start)
            path.reverse()

            print('Путь найден: {}'.format(path))
            return path

        Q.remove(current)
        U.append(current)
    print('Путь не существует.')


def aco(start, goal, size):
    d = np.array(nx.adjacency_matrix(G).todense())

    start = int(start)
    goal = int(goal)

    n_iterations = 300
    n_ants = int(size)
    n_nodes = len(G.nodes)

    e = .5  # коэффициент испраения
    alpha = 1  # коэффициент феромона
    beta = 2  # коэффициент видимости

    # подсчет видимости следующего узла: visibility(i,j)=1/d(i,j)
    visibility = 1 / d
    visibility[visibility == inf] = 0

    # инициирующий феромон, присутствующий на дорогах, ведущих в узлы
    pheromne = .1 * np.ones((n_ants, n_nodes))

    # инициализация маршрута муравьев с размером rute(n_ants,n_citys)
    rute = 0 * np.ones((n_ants, n_nodes))

    for iteration in range(n_iterations):
        rute[:, 0] = start  # начальное положение каждого муравья '1', то есть узла '1'

        for i in range(n_ants):

            temp_visibility = np.array(visibility)

            for j in range(n_nodes - 1):
                # combine_feature = np.zeros(n_nodes)
                # cum_prob = np.zeros(n_nodes)
                cur_loc = int(rute[i, j] - 1)
                temp_visibility[:, cur_loc] = 0  # видимость текущего узла равна нулю
                p_feature = np.power(pheromne[cur_loc, :], beta)  # вычисление коэффициента феромона
                v_feature = np.power(temp_visibility[cur_loc, :], alpha)  # вычисление коэффициента видимости
                p_feature = p_feature[:, np.newaxis]  # добавление оси для создания size[n_nodes,1]
                v_feature = v_feature[:, np.newaxis]  # добавление оси для создания size[n_nodes,1]
                combine_feature = np.multiply(p_feature, v_feature)  # вычисление функции объединения
                total = np.sum(combine_feature)  # сумма всех характеристик
                probs = combine_feature / total  # нахождение вероятности элемента probs(i) = comine_feature(i)/total
                cum_prob = np.cumsum(probs)  # вычисление совокупной суммы
                r = np.random.random_sample()  # рандомно число в диапазоне [0.0, 1.0)
                node = np.nonzero(cum_prob > r)[0][0] + 1  # поиск следующего узла с вероятностью выше random(r)
                rute[i, j + 1] = node  # добавление узла в путь

                if node == n_nodes or node == goal:
                    break
            # left = list(set([i for i in range(1, n_nodes + 1)]) - set(rute[i, :-2]))[0] # поиск последнего неизведанного города для маршрута
            # rute[i, -2] = left  # adding untraversed city to route
        rute_opt = np.array(rute)  # инициализация оптимального пути
        dist_cost = np.zeros((n_ants, 1))  # инициализация стоимости пути

        for i in range(n_ants):
            s = 0
            for j in range(n_nodes - 1):
                s = s + d[int(rute_opt[i, j]) - 1, int(rute_opt[i, j + 1]) - 1]  # расчет общего расстояния

            dist_cost[i] = s  # сохранение расстояния 'i'-го муравья в положении 'i'

        dist_min_loc = np.argmin(dist_cost)  # нахождение местоположения минимума dist_cost
        dist_min_cost = dist_cost[dist_min_loc]  # нахождение минимума dist_cost
        best_route = rute[dist_min_loc, :]  # инициализация текущего пройденного маршрута как наилучшего маршрута
        pheromne = (1 - e) * pheromne  # испарение феромона с помощью (1-e)

        for i in range(n_ants):
            for j in range(n_nodes - 1):
                dt = 1 / dist_cost[i]
                # обновление феромона с помощью delta_distance
                # delta_distance будет больше с min_dist, т.е.
                # добавит больше веса этому маршруту на единицу площади
                pheromne[int(rute_opt[i, j]) - 1, int(rute_opt[i, j + 1]) - 1] = pheromne[int(rute_opt[i, j]) - 1, int(
                    rute_opt[i, j + 1]) - 1] + dt

    best_route = best_route[best_route != 0]
    best_route = [str(int(item)) for item in best_route]

    print('Конечные маршруты всех муравьев:')
    print(rute_opt)

    if best_route[len(best_route)-1] == str(goal):
        print('Кратчайший путь:', best_route)
        print('Стоимость кратчайшего пути: ', int(dist_min_cost[0]) + d[int(best_route[-2]) - 1, 0])
        path.clear()
        for i in range(len(best_route)):
            path.append(best_route[i])
    else:
        print('Путь не существует.')



def case_number_1():
    print("Введите название вершины, которую хотите добавить: ")
    name_of_node = input()
    print("Введите значение эвристики для данной вершины: ")
    heuristics = int(input())
    G.add_node(name_of_node, heuristics=heuristics)


def case_number_2():
    print("Введите название вершины, из которой выходит путь: ")
    name_of_out_node = input()
    print("Введите название вершины, в которую приходит путь: ")
    name_of_in_node = input()
    print("Введите стоимость данного пути: ")
    weight = int(input())
    G.add_edge(name_of_out_node, name_of_in_node, weight=weight)


def case_number_3():
    print("Введите название начальной вершины: ")
    name_of_start_vertex = input()
    print("Введите название целевой вершины: ")
    name_of_goal_vertex = input()
    a_star(name_of_start_vertex, name_of_goal_vertex)


def case_number_4():
    print("Введите название начальной вершины: ")
    name_of_start_vertex = input()
    print("Введите название целевой вершины: ")
    name_of_goal_vertex = input()
    print("Введите размер колонии: ")
    size_of_colony = input()
    aco(name_of_start_vertex, name_of_goal_vertex, size_of_colony)


def menu(case_number):
    if case_number == '1':
        case_number_1()

    elif case_number == '2':
        case_number_2()

    elif case_number == '3':
        case_number_3()

    elif case_number == '4':
        case_number_4()

    else:
        print("Неверный ввод")
        return
    draw_graph()


def main():
    draw_graph()
    while True:
        print(f"+-----------------------------------+\n"
              f"|               М Е Н Ю             |\n"
              f"+-----------------------------------+\n"
              f"|1.| Добавить вершину.              |")
        print(f"|2.| Добавить путь.                 |")
        print(f"|3.| Алгоритм А*                    |")
        print(f"|4.| Муравьиный алгоритм.           |\n"
              f"+-----------------------------------+")
        print("Введите номер меню: ")
        number = input()
        menu(number)





