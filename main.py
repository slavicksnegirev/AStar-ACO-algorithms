import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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

    tmp_edge_array = []
    for u, v, d in G.edges:
        tmp_edge_array.append(u)
        tmp_edge_array.append(v)
    tmp_edge_array = np.array(tmp_edge_array).reshape(-1, 2)

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
    plt.show()


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


def menu(case_number):
    if case_number == '1':
        case_number_1()

    elif case_number == '2':
        case_number_2()

    elif case_number == '3':
        case_number_3()

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
        print(f"|3.| Алгоритм А*                    |\n"
              f"+-----------------------------------+")
        print("Введите номер меню: ")
        number = input()
        menu(number)


if __name__ == "__main__":
    main()
