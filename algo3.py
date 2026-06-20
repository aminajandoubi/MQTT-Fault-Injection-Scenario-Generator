# -*- coding: utf-8 -*-
"""
algo3_date_events_from_json.py

Input :
- Scenario_G1.json
- Scenario_G2.json
- couples_EG1_RG2.json
- couples_EG2_RG1.json

Output :
- L_G1_date.json
- L_G2_date.json
"""

import json


def load_scenario(filename):
    with open(filename, "r", encoding="utf-8") as file:
        scenario = json.load(file)

    return [tuple(event) for event in scenario]


def load_couples(filename):
    with open(filename, "r", encoding="utf-8") as file:
        couples = json.load(file)

    return [
        (tuple(pair[0]), tuple(pair[1]))
        for pair in couples
    ]


def save_date_events(L_date, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(L_date, file, indent=4, ensure_ascii=False)


def date_events(
    scenario_G1,
    scenario_G2,
    couples_EG1_RG2,
    couples_EG2_RG1
):
    L_G1_date = []
    L_G2_date = []

    for i, event in enumerate(scenario_G1, start=1):
        L_G1_date.append([event, i, 0])

    for j, event in enumerate(scenario_G2, start=1):
        L_G2_date.append([event, 0, j])

    date_G1 = {item[0]: item for item in L_G1_date}
    date_G2 = {item[0]: item for item in L_G2_date}

    receive_G1_from_G2 = {
        receive: send
        for send, receive in couples_EG2_RG1
    }

    for k in range(len(L_G1_date)):
        event = L_G1_date[k][0]

        if event in receive_G1_from_G2:
            send_event = receive_G1_from_G2[event]
            L_G1_date[k][2] = max(
                L_G1_date[k][2],
                date_G2[send_event][2]
            )
        elif k != 0:
            L_G1_date[k][2] = max(
                L_G1_date[k][2],
                L_G1_date[k - 1][2]
            )

    receive_G2_from_G1 = {
        receive: send
        for send, receive in couples_EG1_RG2
    }

    for l in range(len(L_G2_date)):
        event = L_G2_date[l][0]

        if event in receive_G2_from_G1:
            send_event = receive_G2_from_G1[event]
            L_G2_date[l][1] = max(
                L_G2_date[l][1],
                date_G1[send_event][1]
            )
        elif l != 0:
            L_G2_date[l][1] = max(
                L_G2_date[l][1],
                L_G2_date[l - 1][1]
            )

    return L_G1_date, L_G2_date


if __name__ == "__main__":

    file_scenario_G1 = input(
        "Chemin du scénario G1 "
        "(ex: Scenarios_G1/Scenario_1.json) : "
    )

    file_scenario_G2 = input(
        "Chemin du scénario G2 "
        "(ex: Scenarios_G2/Scenario_1.json) : "
    )

    file_couples_EG1_RG2 = input(
        "Chemin couples_EG1_RG2.json : "
    )

    file_couples_EG2_RG1 = input(
        "Chemin couples_EG2_RG1.json : "
    )

    scenario_G1 = load_scenario(file_scenario_G1)
    scenario_G2 = load_scenario(file_scenario_G2)

    couples_EG1_RG2 = load_couples(file_couples_EG1_RG2)
    couples_EG2_RG1 = load_couples(file_couples_EG2_RG1)

    L_G1_date, L_G2_date = date_events(
        scenario_G1,
        scenario_G2,
        couples_EG1_RG2,
        couples_EG2_RG1
    )

    print("\nL_G1_date:")
    for item in L_G1_date:
        print(item)

    print("\nL_G2_date:")
    for item in L_G2_date:
        print(item)

    save_date_events(L_G1_date, "L_G1_date.json")
    save_date_events(L_G2_date, "L_G2_date.json")

    print("\nFichiers générés :")
    print("- L_G1_date.json")
    print("- L_G2_date.json")
