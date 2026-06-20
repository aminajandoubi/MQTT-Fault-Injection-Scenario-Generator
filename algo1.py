# -*- coding: utf-8 -*-
"""
algo1_from_txt.py

Chaque ligne du fichier graph.txt doit avoir le format :
source transition type destination

Exemple :
1 send_a send 2
2 receive_c receive 4

Sortie :
un dossier contenant :
Scenario_1.json
Scenario_2.json
Scenario_3.json
...
"""

import json
import os


class Transition:
    def __init__(self, name, event_type, target):
        self.name = name
        self.event_type = event_type
        self.target = target


class CFG:
    def __init__(self):
        self.graph = {}

    def add_transition(self, source, name, event_type, target):
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append(Transition(name, event_type, target))

    def get_transitions(self, node):
        return self.graph.get(node, [])


def convert_node(value):
    try:
        return int(value)
    except ValueError:
        return value


def load_cfg_from_txt(filename):
    cfg = CFG()

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) != 4:
                raise ValueError(
                    f"Erreur ligne {line_number}: format invalide. "
                    "Format attendu : source transition type destination"
                )

            source, name, event_type, target = parts

            source = convert_node(source)
            target = convert_node(target)

            if event_type not in ["send", "receive", "internal"]:
                raise ValueError(
                    f"Erreur ligne {line_number}: type invalide '{event_type}'. "
                    "Types acceptes : send, receive, internal"
                )

            cfg.add_transition(source, name, event_type, target)

    return cfg


def generate_scenarios(cfg, node, visited=None):
    if visited is None:
        visited = set()

    if node in visited:
        return [[]]

    visited.add(node)

    transitions = cfg.get_transitions(node)

    if not transitions:
        return [[]]

    all_scenarios = []

    for t in transitions:
        triplet = (node, t.name, t.target)

        sub_scenarios = generate_scenarios(
            cfg,
            t.target,
            visited.copy()
        )

        for sub in sub_scenarios:
            if t.event_type in ["send", "receive"]:
                all_scenarios.append([triplet] + sub)
            else:
                all_scenarios.append(sub)

    return all_scenarios


def save_each_scenario(scenarios, folder_name):
    """
    Sauvegarde chaque scénario dans un fichier JSON séparé.
    """

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i, scenario in enumerate(scenarios, start=1):
        filename = os.path.join(folder_name, f"Scenario_{i}.json")

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                scenario,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(f"Scénario {i} sauvegardé dans : {filename}")


if __name__ == "__main__":
    graph_file = "graph.txt"

    print("Lecture du graphe depuis :", graph_file)

    cfg = load_cfg_from_txt(graph_file)

    start_node = input("Donner le noeud de depart : ")
    start_node = convert_node(start_node)

    scenarios = generate_scenarios(cfg, start_node)

    print("\n===== Scenarios generes =====")

    for i, scenario in enumerate(scenarios, start=1):
        print(f"\nScenario {i}:")
        for event in scenario:
            print(event)

    folder_name = input(
        "\nNom du dossier pour sauvegarder les scénarios "
        "(ex: Scenarios_G1) : "
    )

    if folder_name.strip() == "":
        folder_name = "Scenarios"

    save_each_scenario(scenarios, folder_name)

    print(f"\nTous les scénarios sont sauvegardés dans le dossier : {folder_name}")
