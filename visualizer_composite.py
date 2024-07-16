import pydot
import os
from typing import Dict, List

class CompositeState:
    def __init__(self, name: str, check: Dict[str, List[str]], actions: List[str]):
        self.name = name
        self.check = check
        self.actions = actions

    def __repr__(self) -> str:
        return f"CompositeState(name='{self.name}', check={self.check}, actions={self.actions})"

class UMLGenerator:
    def generate_composite_uml_string(self, machine: CompositeState):
        uml_string = "@startuml\n"
        uml_string += f'state "{machine.name}" as {machine.name} {{\n'
        uml_string += f'  state "entry" as {machine.name}_entry\n'

        if not machine.check:
            # If check is empty, create a single state with the actions
            actions = "do / \\n" + "\\n".join(machine.actions)
            uml_string += f'  state "{actions}" as state_1\n'
            uml_string += f'  {machine.name}_entry --> state_1\n'
            uml_string += f'  state_1 --> exit1\n'
            uml_string += f'  state "X exit1" as exit1\n'
        else:
            # If there are checks, create the necessary states and transitions
            check_name, outcomes = next(iter(machine.check.items()))
            check_action = "do / \\ncheck := " + check_name
            uml_string += f'  state "{check_action}" as state_1\n'
            uml_string += f'  {machine.name}_entry --> state_1\n'
            for idx, outcome in enumerate(outcomes):
                outcome = outcome.strip()
                actions = "do / \\n" + machine.actions[idx].replace(" \n ", "\\n")
                uml_string += f'  state "{actions}" as state_{idx + 2}\n'
                uml_string += f'  state "X exit{idx + 1}" as exit_{idx + 1}\n'
                uml_string += f'  state_{idx + 2} --> exit_{idx + 1}\n'
                uml_string += f'  state_1 --> state_{idx + 2} : [check = {outcome}]\n'

        uml_string += "}\n@enduml\n"
        return uml_string

    def generate_composite_pydot_graph(self, machine: CompositeState):
        graph = pydot.Dot(graph_type="digraph")

        # Add composite state as a cluster
        subgraph = pydot.Cluster(machine.name, label=machine.name, style="rounded")

        # Add entry node to the subgraph
        subgraph.add_node(pydot.Node(f"{machine.name}_entry", shape="circle", label="", fixedsize="true", width=0.2, height=0.2))

        if not machine.check:
            # If check is empty, create a single state with the actions
            label = f"do / \\n" + "\\n".join(machine.actions)
            state_id = f"state_1"
            subgraph.add_node(pydot.Node(state_id, label=label, shape="box", labelloc="t"))
            subgraph.add_edge(pydot.Edge(f"{machine.name}_entry", state_id))
            exit_id = f"exit1"
            subgraph.add_node(pydot.Node(exit_id, shape="circle", label="X", fixedsize="true", width=0.2, height=0.2))
            subgraph.add_edge(pydot.Edge(state_id, exit_id))
        else:
            # If there are checks, create the necessary states and transitions
            check_name, outcomes = next(iter(machine.check.items()))
            check_action = "do / \\ncheck := " + check_name
            check_state_id = f"state_1"
            subgraph.add_node(pydot.Node(check_state_id, label=check_action, shape="box", labelloc="t"))
            subgraph.add_edge(pydot.Edge(f"{machine.name}_entry", check_state_id))

            for idx, outcome in enumerate(outcomes):
                outcome = outcome.strip()
                actions = "do / \\n" + machine.actions[idx].replace(" \n ", "\\n")
                state_id = f"state_{idx + 2}"
                exit_id = f"exit{idx + 1}"

                subgraph.add_node(pydot.Node(state_id, label=actions, shape="box", labelloc="t"))
                subgraph.add_node(pydot.Node(exit_id, shape="circle", label="X", fixedsize="true", width=0.2, height=0.2))
                subgraph.add_edge(pydot.Edge(state_id, exit_id))
                subgraph.add_edge(pydot.Edge(check_state_id, state_id, label=f"[check = {outcome}]"))

        graph.add_subgraph(subgraph)
        return graph

    def visualize_composite_state_state_machines(self, filepath, composite_states: List[CompositeState]):
        # Ensure the directory exists
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        for machine in composite_states:
            graph = self.generate_composite_pydot_graph(machine)
            folder_name = os.path.basename(filepath)
            output_path_png = f"{filepath}/composite_state_{folder_name}_{machine.name}.png"
            output_path_uml = f"{filepath}/composite_state_{folder_name}_{machine.name}.uml"
            graph.write_png(output_path_png)

            uml_string = self.generate_composite_uml_string(machine)
            with open(output_path_uml, 'w') as f:
                f.write(uml_string)

# Example usage with new input format
composite_state_groups = [
    [
        CompositeState(name='insertCard', check={}, actions=['user.requestPassword']),
        CompositeState(name='enterPassword', check={'consortium.verifyAccount': ['badAccount', 'badPassword', 'OK']}, actions=['user.badAccountMessage \n user.printReceipt \n user.ejectCard \n user.requestTakeCard', 'user.requestPassword', '']),
        CompositeState(name='takeCard', check={}, actions=['user.displayMainScreen']),
        CompositeState(name='cancel', check={}, actions=['user.canceledMessage \n user.ejectCard \n user.requestTakeCard'])
    ],
    [
        CompositeState(name='verifyAccount', check={'bank.verifyCardWithBank': ['badBankAccount', 'badBankPassword', 'OK']}, actions=['', '', ''])
    ],
    [
        CompositeState(name='verifyCardWithBank', check={'verifyCardWithBank': ['badBankAccount', 'badBankPassword', 'OK']}, actions=['', '', ''])
    ]
]

uml_generator = UMLGenerator()

for group in composite_state_groups:
    for state in group:
        uml_string = uml_generator.generate_composite_uml_string(state)
        print(f"UML for {state.name}:\n{uml_string}\n")

    # Visualize the group of composite states
    uml_generator.visualize_composite_state_state_machines("./test", group)

