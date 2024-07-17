# STEP 4.2.2
import os
from typing import Dict
import pydot
from models import StateMachine


def visualize_state_machine(state_machines: Dict[str, StateMachine], path):
    if not os.path.exists(path):
        os.makedirs(path)
    for obj, state_machine in state_machines.items():
        start_state = state_machine.transitions[0].from_transition

        uml_filename = os.path.join(path, f"{obj}.uml")
        jpg_filename = os.path.join(path, f"{obj}.jpg")

        with open(uml_filename, 'w') as uml_file:
            uml_file.write(f"@startuml\n")
            uml_file.write(f"[*] --> {start_state}\n")

            for state in state_machine.states:
                uml_file.write(f"state {state}\n")

            for state in state_machine.actions:
                uml_file.write(f"state {state}\n")

            for transition in state_machine.transitions:
                from_state = transition.from_transition
                to_state = transition.to_transition
                message = transition.message_in
                return_value = transition.return_v

                uml_file.write(f"{from_state} --> {to_state} : {message}  / {return_value} \n")

            uml_file.write(f"@enduml\n")

        # Create a graph using pydot
        graph = pydot.Dot(graph_type='digraph')

        # Add the start state and initial transition dynamically
        start_node = pydot.Node("[*]", shape="point")
        graph.add_node(start_node)

        initial_node = pydot.Node(start_state, shape="rectangle")
        graph.add_node(initial_node)

        start_edge = pydot.Edge("[*]", start_state)
        graph.add_edge(start_edge)

        for state in state_machine.states:
            node = pydot.Node(state, shape="rectangle")
            graph.add_node(node)

        for state in state_machine.actions:
            node = pydot.Node(state, shape="diamond")
            graph.add_node(node)

        for transition in state_machine.transitions:
            from_state = transition.from_transition
            to_state = transition.to_transition
            arrowhead = "normal" if from_state in state_machine.states else "onormal"
            arrowtail = "dot" if from_state  in state_machine.actions else ""
            dir = "both"  if from_state  in state_machine.actions else ""
            label = f"{transition.message_in}" + "/" + f"{transition.return_v}"

            graph.add_edge(pydot.Edge(from_state, to_state, label = label, arrowhead = arrowhead, arrowtail = arrowtail, dir = dir))

        # Save the graph as a jpg file
        graph.write_jpg(jpg_filename)
        pass