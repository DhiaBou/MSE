import os

from visualizer_statemachine import visualize_state_machine
from io_automaton_to_composite import get_composite_states
from io_automaton_to_state_machine import get_state_machine, get_state_machines
from visualizer_composite import visualize_composite_state_state_machines
from models import *
from typing import Dict, List

from step1 import generate_table_from_model
from step2 import get_behaviors
from step3 import get_io_from_behavior, automaton_visualizer
from step4 import IO2UML

artefacts_folder = "Artefacts"
uml_artefacts_folder = f"{artefacts_folder}/Uml"
io_automata_artefacts_folder = f"{artefacts_folder}/IOAutomata"

scenarios = generate_table_from_model("./inputs/MDD_Model.uml")
behaviors = get_behaviors(scenarios)
io_automata = get_io_from_behavior(behaviors)
automaton_visualizer(io_automata, io_automata_artefacts_folder)



for obj, automat in io_automata.items():
    composite_states = get_composite_states(automat)
    state_machine = get_state_machine(automat)
    print(state_machine)
    for composite_state in composite_states:
        visualize_composite_state_state_machines(f"{uml_artefacts_folder}/{obj}", composite_states)

state_machines = get_state_machines(io_automata)
visualize_state_machine(state_machines, f"{uml_artefacts_folder}")

