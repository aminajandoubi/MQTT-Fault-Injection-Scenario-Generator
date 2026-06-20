# -*- coding: utf-8 -*-
"""
algo5_generate_lattice.py
"""

import json


def load_send_date(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        (tuple(item[0]), item[1], item[2])
        for item in data
    ]


def vector_time(event_date):
    return event_date[1], event_date[2]


def vector_greater(e1, e2):
    a, b = vector_time(e1)
    c, d = vector_time(e2)
    return a >= c and b >= d and (a, b) != (c, d)


class Lattice:
    def __init__(self):
        self.root = "racine"
        self.edges = []

    def add_edge(self, source, target, label):
        edge = (source, target, label)
        if edge not in self.edges:
            self.edges.append(edge)

    def print_edges(self):
        print("\n===== RELATIONS DU LATTICE =====")
        for source, target, label in self.edges:
            print(f"{source} --{label}--> {target}")


def initialization_list(L_send_date):
    return [{"event": item, "visited": False} for item in L_send_date]


def search_parent(current_item, L_explore_other):
    current_event = current_item["event"]
    candidates = []

    for other_item in L_explore_other:
        other_event = other_item["event"]

        if other_item["visited"] is False and vector_greater(current_event, other_event):
            candidates.append(other_item)

    if not candidates:
        return None

    best_parent = max(
        candidates,
        key=lambda x: (x["event"][1], x["event"][2])
    )

    best_parent["visited"] = True
    return best_parent["event"]


def synchronisation(T, L_explore_current, L_explore_other, pivot):
    for i in range(len(L_explore_current)):
        current_item = L_explore_current[i]
        current_event = current_item["event"]

        if i != 0:
            previous_event = L_explore_current[i - 1]["event"]

            if pivot == 0:
                T.add_edge(previous_event, current_event, "p1")
            else:
                T.add_edge(previous_event, current_event, "p2")

        parent = search_parent(current_item, L_explore_other)

        if parent is not None:
            if pivot == 0:
                T.add_edge(parent, current_event, "p1")
            else:
                T.add_edge(parent, current_event, "p2")

    return T


def generate_a_lattice(L_G1_send_date, L_G2_send_date):
    T = Lattice()

    L_explore_G1 = initialization_list(L_G1_send_date)
    L_explore_G2 = initialization_list(L_G2_send_date)

    if len(L_explore_G1) > 0:
        T.add_edge(T.root, L_explore_G1[0]["event"], "p1")

    if len(L_explore_G2) > 0:
        T.add_edge(T.root, L_explore_G2[0]["event"], "p2")

    T = synchronisation(T, L_explore_G1, L_explore_G2, pivot=0)
    T = synchronisation(T, L_explore_G2, L_explore_G1, pivot=1)

    return T, L_explore_G1, L_explore_G2


def export_lattice_dot(T, filename="lattice.dot"):
    nodes = []

    for source, target, _ in T.edges:
        if source not in nodes:
            nodes.append(source)
        if target not in nodes:
            nodes.append(target)

    node_ids = {}

    for i, node in enumerate(nodes):
        node_ids[node] = f"N{i}"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("digraph Lattice {\n")
        f.write("  rankdir=TB;\n")
        f.write("  node [shape=ellipse, fontsize=10];\n\n")

        for node in nodes:
            label = str(node).replace('"', '\\"')
            f.write(f'  {node_ids[node]} [label="{label}"];\n')

        f.write("\n")

        for source, target, label in T.edges:
            f.write(
                f"  {node_ids[source]} -> {node_ids[target]} "
                f'[label="{label}"];\n'
            )

        f.write("}\n")


if __name__ == "__main__":

    file_G1 = input("Chemin de L_G1_send_date.json : ")
    file_G2 = input("Chemin de L_G2_send_date.json : ")

    L_G1_send_date = load_send_date(file_G1)
    L_G2_send_date = load_send_date(file_G2)

    output_dot = input("Nom du fichier DOT de sortie : ")

    if output_dot.strip() == "":
        output_dot = "lattice.dot"

    T, L_explore_G1, L_explore_G2 = generate_a_lattice(
        L_G1_send_date,
        L_G2_send_date
    )

    print("===== L_explore_G1 =====")
    for item in L_explore_G1:
        print((item["event"], item["visited"]))

    print("\n===== L_explore_G2 =====")
    for item in L_explore_G2:
        print((item["event"], item["visited"]))

    T.print_edges()

    export_lattice_dot(T, output_dot)

    print(f"\nFichier généré : {output_dot}")
    print(f"Commande : dot -Tpng {output_dot} -o lattice.png")
