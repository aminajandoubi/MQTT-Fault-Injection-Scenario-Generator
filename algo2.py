# -*- coding: utf-8 -*-
"""
algo2_generate_pairs_from_json.py

Input :
    Deux fichiers JSON générés par l'algorithme 1 :
    - Scenario_G1.json
    - Scenario_G2.json

Output :
    - couples_EG1_RG2.json
    - couples_EG2_RG1.json
"""

import json


def event_type(event):
    name = event[1]

    if name.startswith("send"):
        return "send"
    elif name.startswith("receive"):
        return "receive"

    return "other"


def message_name(event):
    """
    Exemple :
        send_a -> a
        receive_a -> a
    """
    return event[1].split("_")[1]


def load_scenario(filename):
    """
    Charge un scénario depuis un fichier JSON.
    """

    with open(filename, "r", encoding="utf-8") as file:
        scenario = json.load(file)

    return [tuple(event) for event in scenario]


def save_pairs(couples, filename):
    """
    Sauvegarde les couples dans un fichier JSON.
    """

    data = []

    for send_event, receive_event in couples:
        data.append([
            list(send_event),
            list(receive_event)
        ])

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def generate_pairs(scenario_send, scenario_receive):
    couples = []

    for send_event in reversed(scenario_send):

        if event_type(send_event) == "send":

            msg_send = message_name(send_event)

            for receive_event in reversed(scenario_receive):

                if event_type(receive_event) == "receive":

                    msg_receive = message_name(receive_event)

                    if msg_send == msg_receive:
                        couples.append((send_event, receive_event))
                        break

    return couples


if __name__ == "__main__":

    file_G1 = input(
        "Donner le chemin du scénario G1 "
        "(ex: Scenarios_G1/Scenario_1.json) : "
    )

    file_G2 = input(
        "Donner le chemin du scénario G2 "
        "(ex: Scenarios_G2/Scenario_1.json) : "
    )

    scenario_G1 = load_scenario(file_G1)
    scenario_G2 = load_scenario(file_G2)

    couples_EG1_RG2 = generate_pairs(
        scenario_G1,
        scenario_G2
    )

    couples_EG2_RG1 = generate_pairs(
        scenario_G2,
        scenario_G1
    )

    print("\nCouples_EG1_RG2 :")
    for c in couples_EG1_RG2:
        print(c)

    print("\nCouples_EG2_RG1 :")
    for c in couples_EG2_RG1:
        print(c)

    save_pairs(
        couples_EG1_RG2,
        "couples_EG1_RG2.json"
    )

    save_pairs(
        couples_EG2_RG1,
        "couples_EG2_RG1.json"
    )

    print("\nFichiers générés :")
    print("- couples_EG1_RG2.json")
    print("- couples_EG2_RG1.json")
