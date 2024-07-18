from model_to_scenarios import generate_table_from_model
from scenarios_to_projections_to_behaviors import get_behaviors
from behaviors_to_io_automata import get_io_from_behavior, automaton_visualizer
from visualizer_statemachine import visualize_state_machine
from io_automaton_to_composite import get_composite_states
from io_automaton_to_state_machine import get_state_machine, get_state_machines
from visualizer_composite import visualize_composite_state_state_machines

artefacts_folder = "Artefacts"
composite_state_state_machine_artefacts_folder = f"{artefacts_folder}/CompositeStates"
state_machine_artefacts_folder = f"{artefacts_folder}/StateMachines"
io_automata_artefacts_folder = f"{artefacts_folder}/IOAutomata"

scenarios = generate_table_from_model("./inputs/MDD_Model.uml")
print('======Scenarios======')
print(scenarios)
behaviors = get_behaviors(scenarios)
print('======behaviors======')
print(behaviors)
io_automata = get_io_from_behavior(behaviors)
print('======IOAutomata======')
print(io_automata)

for obj, automat in io_automata.items():
    composite_states = get_composite_states(automat)
    state_machine = get_state_machine(automat)
    print(state_machine)
    for composite_state in composite_states:
        visualize_composite_state_state_machines(composite_states, f"{composite_state_state_machine_artefacts_folder}/{obj}")

automaton_visualizer(io_automata, io_automata_artefacts_folder)
state_machines = get_state_machines(io_automata)
visualize_state_machine(state_machines, f"{state_machine_artefacts_folder}")

