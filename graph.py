import sys
import numpy as np
import networkx as nx
from numpy import inf
from matplotlib import pyplot as plt

path = []
text_output = []
G = nx.MultiDiGraph()

G.add_nodes_from([
    ("1", {"heuristics": 14}),
    ("2", {"heuristics": 13}),
    ("3", {"heuristics": 12}),
    ("4", {"heuristics": 11}),
    ("5", {"heuristics": 10}),
    ("6", {"heuristics": 9}),
    ("7", {"heuristics": 8}),
    ("8", {"heuristics": 7}),
    ("9", {"heuristics": 6}),
    ("10", {"heuristics": 5}),
    ("11", {"heuristics": 4}),
    ("12", {"heuristics": 3}),
    ("13", {"heuristics": 2}),
    ("14", {"heuristics": 1}),
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


def a_star(start, goal):
    iteration = 0
    text_output.append("Вывод протокола:\n")

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
        iteration += 1
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
            text_output.append('Путь не существует.' + "\n")
            return None

        if current == goal:
            path.clear()

            while parents[current] != current:
                path.append(current)
                current = parents[current]

            path.append(start)
            path.reverse()

            text_output.append("Путь найден: " + str(path)  + "\n")

            cost = 0
            for i in range(len(path)-1):
                for u, v, data in G.edges(data=True):
                    if str(path[i]) == u and str(path[i+1]) == v:
                        cost += d[u, v]

            text_output.append("Стоимость пути: " + str(cost)  + "\n")
            return text_output

        Q.remove(current)
        U.append(current)

        text_output.append("Итерация " + str(iteration) + "\n")
        text_output.append("Множество вершин, которое требуется рассмотреть: " + str(Q)  + "\n")
        text_output.append("Множество рассмотренных вершин: " + str(U) + "\n\n")

    text_output.append('Путь не существует.\n')


def aco(start, goal, size):
    e = .5  # коэффициент испраения
    alpha = 1  # коэффициент феромона
    beta = 4  # коэффициент видимости

    n_iterations = 100 # количество итераций
    n_ants = int(size) # размер колонии
    n_nodes = len(G.nodes) # количество вершин

    start_node = list(G.nodes).index(start)
    goal_node = list(G.nodes).index(goal)

    text_output.append("Вывод протокола:\n")
    D = np.array(nx.adjacency_matrix(G).todense()) # матрица расстояний

    # подсчет видимости следующего узла: visibility(i,j)=1/d(i,j)
    visibility = 1 / D
    visibility[visibility == inf] = 0

    # инициирующий феромон, присутствующий на дорогах, ведущих в узлы
    pheromne = visibility
    pheromne[pheromne > 0] = 0.1


    # инициализация лучшего пути
    best_rute = inf * np.ones((1, n_nodes))

    # стоимость минимального пути
    best_dist_min_cost = None

    # инициализация маршрута муравьев с размером rute(n_ants,n_citys)
    rute = -1 * np.ones((n_ants, n_nodes))

    # начальное положение каждого муравья
    rute[:, 0] = start_node

    for iteration in range(n_iterations):
        for i in range(n_ants):
            temp_visibility = np.array(visibility)

            for j in range(n_nodes - 1):
                cur_loc = int(rute[i, j])
                temp_visibility[:, cur_loc] = 0  # видимость текущего узла равна нулю
                p_feature = np.power(pheromne[cur_loc, :], alpha)  # вычисление коэффициента феромона
                v_feature = np.power(temp_visibility[cur_loc, :], beta)  # вычисление коэффициента видимости
                p_feature = p_feature[:, np.newaxis]  # добавление оси для создания size[n_nodes,1]
                v_feature = v_feature[:, np.newaxis]  # добавление оси для создания size[n_nodes,1]
                combine_feature = np.multiply(p_feature, v_feature)  # вычисление функции объединения
                total = np.sum(combine_feature)  # сумма всех характеристик
                probs = combine_feature / total  # нахождение вероятности элемента probs(i) = comine_feature(i)/total
                cum_prob = np.cumsum(probs)  # вычисление совокупной суммы
                r = np.random.random_sample()  # рандомное число в диапазоне [0.0, 1.0)
                node = np.nonzero(cum_prob > r)[0][0]  # поиск следующего узла с вероятностью выше random(r)
                rute[i, j + 1] = node  # добавление узла в путь

                if node == n_nodes-1 or node == list(G.nodes).index(goal):
                    break

        rute_opt = np.array(rute)  # инициализация оптимального пути
        dist_cost = np.zeros((n_ants, 1))  # инициализация стоимости пути

        for i in range(n_ants):
            s = 0
            for j in range(n_nodes-1):
                s = s + D[int(rute_opt[i, j]), int(rute_opt[i, j + 1])]  # расчет общего расстояния

            dist_cost[i] = s  # сохранение расстояния 'i'-го муравья в положении 'i'

        dist_min_loc = np.argmin(dist_cost)  # нахождение местоположения минимума dist_cost
        dist_min_cost = dist_cost[dist_min_loc]  # нахождение минимума dist_cost

        # инициализация текущего пройденного маршрута как наилучшего маршрута
        if goal_node in rute[dist_min_loc, :]:
            if inf in best_rute and goal_node:
                best_rute = rute[dist_min_loc, :]
                best_dist_min_cost = dist_min_cost
            elif best_dist_min_cost > dist_min_cost:
                best_rute = rute[dist_min_loc, :]
                best_dist_min_cost = dist_min_cost

        text_output.append("\nИтерация " + str(iteration) + "\n")
        text_output.append("Ферменты на ребрах:\n")
        for i in range(n_nodes):
            text_output.append("[")
            for j in range(n_nodes):
                text_output.append(str(round(pheromne[i][j], 3)) + "  ")
            text_output.append("]\n")

        text_output.append("\nПройденные маршруты муравьями:\n")
        for i in range(n_ants):
            text_output.append("[")
            for j in range(n_nodes-1):
                if rute[i][j] != -1:
                    text_output.append("'" + str(list(G.nodes)[int(rute[i][j])]) + "',  ")
            text_output.append("]\n")

        pheromne = (1 - e) * pheromne  # испарение феромона с помощью (1-e)

        for i in range(n_ants):
            for j in range(n_nodes - 1):

                if goal_node in rute[i]:
                    dt = 1 / dist_cost[i]
                else:
                    dt = 0
                # обновление феромона с помощью delta_distance delta_distance будет больше с min_dist, т.е. добавит больше веса этому маршруту на единицу площади
                pheromne[int(rute_opt[i, j]), int(rute_opt[i, j + 1])] = pheromne[int(rute_opt[i, j]), int(rute_opt[i, j + 1])] + dt

    best_rute = best_rute[best_rute != -1]

    if goal_node in best_rute:
        path.clear()

        for i in range(len(best_rute)):
            if best_rute[i] != -1:
                path.append(str(list(G.nodes)[int(best_rute[i])]))

        text_output.append("\nКратчайший путь: " + str(path))
        text_output.append("\nСтоимость кратчайшего пути: " + str(int(best_dist_min_cost) + D[int(best_rute[-2]) - 1, 0]))
    else:
        text_output.append("\nПуть не найден.")