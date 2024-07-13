import os

from models import *
from typing import Dict, List

from step1 import generate_table_from_model
from step2 import get_behaviors
from step3 import get_io_from_behavior, visualizer
from step4 import IO2UML

def get_initial_states(behaviors: List[Behavior]) -> Dict[str, List[str]]:
    initial_states: Dict[str, List[str]] = {}

    for behavior in behaviors:
        init = []
        for behaviorBlockObject in behavior.behavior:
            init.append(behaviorBlockObject.prestate)
            break  # very hacky work around, the assumption is wrong
        initial_states.update({behavior.object: list(set(init))})

    return initial_states

artefacts_folder = "Artefacts"
uml_artefacts_folder = f"{artefacts_folder}/Uml"
io_automata_artefacts_folder = f"{artefacts_folder}/IOAutomata"

scenarios = generate_table_from_model("inputs/MDD_Model.uml")
behaviors = get_behaviors(scenarios)
io_automata = get_io_from_behavior(behaviors)
visualizer(io_automata, io_automata_artefacts_folder)

initial_states = get_initial_states(behaviors)

for obj, automat in io_automata.items():
    uml = IO2UML(io_automata[obj], initial_states[obj])
    os.makedirs(f"{uml_artefacts_folder}/{obj}", exist_ok=True)
    uml.visualize_uml(f"{uml_artefacts_folder}/{obj}")
    uml.visualize_composite_state_state_machines(f"{uml_artefacts_folder}/{obj}")