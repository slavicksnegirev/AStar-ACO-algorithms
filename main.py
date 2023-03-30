import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from graph import Graph
from queue import PriorityQueue

G = nx.MultiDiGraph()


# G.add_nodes_from([
#     ("A", {"heuristics": 9}),
#     ("B", {"heuristics": 6}),
#     ("C", {"heuristics": 5}),
#     ("D", {"heuristics": 7}),
#     ("E", {"heuristics": 8}),
# ])
#
# G.add_edges_from([
#     ("A", "C", {"weight": 10}),
#     ("B", "C", {"weight": 15}),
#     ("B", "D", {"weight": 16}),
#     ("C", "D", {"weight": 18}),
#     ("D", "E", {"weight": 7}),
# ])

G.add_nodes_from([
    ("1", {"heuristics": 15}),
    ("2", {"heuristics": 13}),
    ("3", {"heuristics": 11}),
    ("4", {"heuristics": 10}),
    ("5", {"heuristics": 8}),
    ("6", {"heuristics": 9}),
    ("7", {"heuristics": 6}),
    ("8", {"heuristics": 5}),
    ("9", {"heuristics": 5}),
    ("10", {"heuristics": 6}),
    ("11", {"heuristics": 3}),
    ("12", {"heuristics": 4}),
    ("13", {"heuristics": 1}),
    ("14", {"heuristics": 2}),
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

# vertex = len(G)
# tmp_graph = Graph(vertex)
# tmp_array = []
# for i in range(vertex):
#         for j in range(vertex):
#
# tmp_graph.graph = [
#
# ]

def draw_graph():
    pos = nx.shell_layout(G)

    node_labels = {n: (d["heuristics"]) for n, d in G.nodes(data=True)}
    edge_labels = {(u, v): (d["weight"]) for u, v, d in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, node_size=200, node_color="pink", font_size=10, width=1, edge_color="grey")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="maroon", font_size=6)
    # for i in pos:
    #     pos[i] -= 0.002
    # nx.draw_networkx_labels(G, pos, font_color="green", font_size=20)
    # for i in pos:
    #     pos[i] += 0.005
    # nx.draw_networkx_labels(G, pos, labels=node_labels, font_color="maroon", font_size=20)
    plt.show()


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
    pass

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
