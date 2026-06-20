# -*- coding: utf-8 -*-
"""
algo6_lattice_traversal_from_dot.py

Input :
    lattice.dot généré par l'algorithme 5

Output :
    L_scenarios.json
"""

from collections import deque
import json
import re
import ast


def load_lattice_from_dot(filename):
    """
    Lit un fichier DOT et extrait :
    - les noeuds avec leurs labels
    - les arcs source -> target
    """

    node_labels = {}
    edges = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        # Exemple :
        # N1 [label="((1, 'send_a', 2), 1, 0)"];
        node_match = re.match(r'(N\d+)\s+\[label="(.+)"\];', line)

        if node_match:
            node_id = node_match.group(1)
            label = node_match.group(2)

            if label == "racine":
                node_labels[node_id] = "racine"
            else:
                try:
                    node_labels[node_id] = ast.literal_eval(label)
                except Exception:
                    node_labels[node_id] = label

        # Exemple :
        # N0 -> N1 [label="p1"];
        edge_match = re.match(r'(N\d+)\s+->\s+(N\d+)\s+\[label="(.+)"\];', line)

        if edge_match:
            source = edge_match.group(1)
            target = edge_match.group(2)
            edge_label = edge_match.group(3)
            edges.append((source, target, edge_label))

    return node_labels, edges


def build_adjacency(edges):
    adj = {}

    for source, target, label in edges:
        if source not in adj:
            adj[source] = []
        adj[source].append(target)

    return adj


def find_root_node(node_labels):
    for node_id, label in node_labels.items():
        if label == "racine":
            return node_id

    raise ValueError("Racine non trouvée dans le fichier DOT.")


def generate_fault_injection_scenarios_from_dot(dot_file):
    node_labels, edges = load_lattice_from_dot(dot_file)

    adj = build_adjacency(edges)
    root_id = find_root_node(node_labels)

    L_scenarios = []
    L_explore = deque()
    visited = set()

    # Initialisation avec les fils de la racine
    for neighbor in adj.get(root_id, []):
        L_explore.append(neighbor)
        visited.add(neighbor)

    # BFS
    while len(L_explore) != 0:
        x = L_explore.popleft()

        event = node_labels[x]

        if event != "racine":
            L_scenarios.append(event)

        for v in adj.get(x, []):
            if v not in visited:
                L_explore.append(v)
                visited.add(v)

    return L_scenarios


def save_scenarios(L_scenarios, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            L_scenarios,
            file,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":

    dot_file = input("Chemin du fichier lattice.dot : ")

    L_scenarios = generate_fault_injection_scenarios_from_dot(dot_file)

    print("\n===== L_scenarios =====")
    for event in L_scenarios:
        print(event)

    output_file = input(
        "\nNom du fichier JSON de sortie "
        "(ex: L_scenarios.json) : "
    )

    if output_file.strip() == "":
        output_file = "L_scenarios.json"

    save_scenarios(L_scenarios, output_file)

    print(f"\nFichier généré : {output_file}")
