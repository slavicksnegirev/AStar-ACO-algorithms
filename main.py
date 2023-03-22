import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

G = nx.MultiDiGraph()


#
# G.add_nodes_from([
#     ("A", {"Heuristics": 9}),
#     ("B", {"Heuristics": 6}),
#     ("C", {"Heuristics": 5}),
#     ("D", {"Heuristics": 7}),
#     ("E", {"Heuristics": 8}),
# ])
#
# G.add_edges_from([
#     ("A", "C", {"Weight": 10}),
#     ("B", "C", {"Weight": 15}),
#     ("B", "D", {"Weight": 16}),
#     ("C", "D", {"Weight": 18}),
#     ("D", "E", {"Weight": 7}),
# ])
#

def draw_graph():
    pos = nx.planar_layout(G)
    node_labels = {n: (d["heuristics"]) for n, d in G.nodes(data=True)}
    edge_labels = {(u, v): (d["weight"]) for u, v, d in G.edges(data=True)}

    nx.draw_planar(G, with_labels=True, node_size=2000, node_color="pink", font_size=20, width=3, edge_color="grey")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="maroon", font_size=16)
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


def menu(case_number):
    if case_number == '1':
        case_number_1()

    elif case_number == '2':
        case_number_2()
    else:
        print("Неверный ввод")
        return
    draw_graph()


def main():
    while True:
        print(f"+-----------------------------------+\n"
              f"|               М Е Н Ю             |\n"
              f"+-----------------------------------+\n"
              f"|1.| Добавить вершину.              |")
        print(f"|2.| Добавить путь.                 |\n"
              f"+-----------------------------------+")
        print("Введите номер меню: ")
        number = input()
        menu(number)


if __name__ == "__main__":
    main()
