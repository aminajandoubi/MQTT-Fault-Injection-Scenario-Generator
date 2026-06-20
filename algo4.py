# -*- coding: utf-8 -*-
"""
algo4_retrieve_send_dates.py

Input :
    - L_G1_date.json
    - L_G2_date.json

Output :
    - L_G1_send_date.json
    - L_G2_send_date.json
"""

import json


def load_date_events(filename):
    """
    Charge un fichier produit par l'algorithme 3.
    """

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_send_events(L_send_date, filename):
    """
    Sauvegarde les événements send.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            L_send_date,
            file,
            indent=4,
            ensure_ascii=False
        )


def retrieve_send_dates(L_date):
    """
    Input :
        [
            [event, date1, date2],
            ...
        ]

    Output :
        uniquement les événements send
    """

    result = []

    for item in L_date:

        event = item[0]
        event_name = event[1]

        if event_name.startswith("send"):
            result.append(item)

    return result


if __name__ == "__main__":

    file_G1 = input(
        "Chemin de L_G1_date.json : "
    )

    file_G2 = input(
        "Chemin de L_G2_date.json : "
    )

    L_G1_date = load_date_events(file_G1)
    L_G2_date = load_date_events(file_G2)

    L_G1_send_date = retrieve_send_dates(L_G1_date)
    L_G2_send_date = retrieve_send_dates(L_G2_date)

    print("\n===== L_G1_send_date =====")
    for item in L_G1_send_date:
        print(item)

    print("\n===== L_G2_send_date =====")
    for item in L_G2_send_date:
        print(item)

    save_send_events(
        L_G1_send_date,
        "L_G1_send_date.json"
    )

    save_send_events(
        L_G2_send_date,
        "L_G2_send_date.json"
    )

    print("\nFichiers générés :")
    print("- L_G1_send_date.json")
    print("- L_G2_send_date.json")
