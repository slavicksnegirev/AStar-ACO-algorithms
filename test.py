import numpy as np
import networkx as nx
from numpy import inf



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


d = np.array(nx.adjacency_matrix(G).todense())

start = 1
goal = 5

n_iterations = 100
n_ants = 15
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
            pheromne[int(rute_opt[i, j]) - 1, int(rute_opt[i, j + 1]) - 1] = pheromne[int(rute_opt[i, j]) - 1, int(rute_opt[i, j + 1]) - 1] + dt
            # обновление феромона с помощью delta_distance
            # delta_distance будет больше с min_dist, т.е.
            # добавит больше веса этому маршруту на единицу площади

print('Конечные маршруты всех муравьев:')
print(rute_opt)
print('Кратчайший путь:', best_route)
print('Стоимость кратчайшего пути: ', int(dist_min_cost[0]) + d[int(best_route[-2]) - 1, 0])



