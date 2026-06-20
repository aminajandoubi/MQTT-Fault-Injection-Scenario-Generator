# MQTT Fault Injection Scenario Generator

## Overview

This repository contains the Python implementation of the methodology proposed in the thesis for the automatic generation of fault injection scenarios from MQTT protocol specifications.

The framework transforms MQTT Control Flow Graphs (CFGs) into fault injection scenarios through six successive processing stages:

1. Event Extraction
2. Event Synchronization
3. Vector Clock Timestamping
4. Event Filtering
5. Lattice Construction
6. Lattice Exploration

# Repository Structure

project/
│
├── algo1.py
├── algo2.py
├── algo3.py
├── algo4.py
├── algo5.py
├── algo6.py
├── inputs/
│   ├── graph_G1.txt
│   ├── graph_G2.txt
│   ├── graph_G3.txt
│   └── graph_G4.txt
├── outputs/
└── README.md

# Requirements

The implementation requires:

* Python 3.9 or higher
* Graphviz

## Python packages
pip install graphviz

# Input Format

The CFG is described using a text file.

Example:
1 send_a send 2
2 receive_c receive 4
2 receive_b receive 3
4 send_d send 5
5 receive_e receive 6
6 send_f send 4
Format:
source_node transition_name event_type target_node
where:
* source_node : source state
* transition_name : transition label
* event_type : send | receive | internal
* target_node : destination state

# Execution Workflow
The algorithms must be executed in the following order.

## Step 1 – Event Extraction
python algo1.py
Input:
graph_G1.txt
graph_G2.txt
Outputs:
Scenario_G1.json
Scenario_G2.json

## Step 2 – Event Synchronization
python algo2.py
Inputs:
Scenario_G1.json
Scenario_G2.json
Outputs:
couples_EG1_RG2.json
couples_EG2_RG1.json

## Step 3 – Vector Clock Timestamping
python algo3.py
Inputs:
Scenario_G1.json
Scenario_G2.json

couples_EG1_RG2.json
couples_EG2_RG1.json
Outputs:
L_G1_date.json
L_G2_date.json

## Step 4 – Event Filtering
python algo4.py
Inputs:
L_G1_date.json
L_G2_date.json
Outputs:
L_G1_send_date.json
L_G2_send_date.json

## Step 5 – Lattice Construction
python algo5.py
Inputs:
L_G1_send_date.json
L_G2_send_date.json
Outputs:
lattice.dot

Optional visualization:
dot -Tpng lattice.dot -o lattice.png

## Step 6 – Fault Injection Scenario Generation
python algo6.py
Input:
lattice.dot
Output:
L_scenarios.json

# Complete Processing Pipeline
CFG Graphs
    │
    ▼
Algorithm 1
(Event Extraction)
    │
    ▼
Algorithm 2
(Event Synchronization)
    │
    ▼
Algorithm 3
(Vector Clock Timestamping)
    │
    ▼
Algorithm 4
(Event Filtering)
    │
    ▼
Algorithm 5
(Lattice Construction)
    │
    ▼
Algorithm 6
(Lattice Exploration)
    │
    ▼
Fault Injection Scenarios

# Reproducibility

The repository contains:
* Source code
* Example CFGs
* Generated lattices
* Fault injection scenarios

# Citation
If you use this software in your research, please cite the associated publications.
* Faultload time model of the MQTT protocol publish service. COMPSAC 2022: 1468-1473
*Faultload sequences for the MQTT protocol services. Int. J. Internet Protoc. Technol. 19(1): 9-24 (2026)
