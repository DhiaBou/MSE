import os

from MSE.io_automaton_to_composite import get_composite_states
from MSE.io_automaton_to_state_machine import get_state_machine
from MSE.visualizer import visualize_composite_state, visualize_state_machine
from models import *
from typing import Dict, List

from step1 import generate_table_from_model
from step2 import get_behaviors
from step3 import get_io_from_behavior, visualizer
from step4 import IO2UML

artefacts_folder = "Artefacts"
uml_artefacts_folder = f"{artefacts_folder}/Uml"
io_automata_artefacts_folder = f"{artefacts_folder}/IOAutomata"

scenarios = generate_table_from_model("MSE/inputs/MDD_Model.uml")
behaviors = get_behaviors(scenarios)
io_automata = get_io_from_behavior(behaviors)
visualizer(io_automata, io_automata_artefacts_folder)


for obj, automat in io_automata.items():
    composite_states = get_composite_states(automat)
    state_machine = get_state_machine(automat)
    for composite_state in composite_states:
        visualize_composite_state(composite_state, f"{artefacts_folder}/{obj}/Uml")
        visualize_state_machine(state_machine, f"{artefacts_folder}/{obj}/Uml")
    