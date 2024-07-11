import os
from os.path import abspath
from typing import Dict, List, Optional
from models import *
from model4 import *


import pydot

class IO2UML:
    def __init__(self, input: IOAutomaton, initial_states: List[str]):
        self.initial_states = initial_states
        self.io_automat = input
        self.state_machine = self._io_2_state_machine()
        self.composite_state_state_machines = (
            self._io_to_composite_state_state_machines()
        )

    def _io_incoming_messages(self, state):
        return set(
            [
                transition.message_in
                for transition in self.io_automat.transitions
                if transition.from_transition == state
            ]
        )

    def _io_transitions_with_incoming_message(self, state, in_message):
        return [
            transition
            for transition in self.io_automat.transitions
            if transition.message_in == in_message and transition.from_transition == state
        ]

    def _io_to_composite_state_state_machines(self) -> List[CompositeStateStateMachine]:
        io_states = self.io_automat.states
        state_machines = []
        for state in io_states:
            for action in self._io_incoming_messages(state):
                io_similar_transitions = self._io_transitions_with_incoming_message(
                    state, action
                )
                state_machine_label = action
                state_machine_parent = state
                blocks = []
                block_transitions = []
                if len(io_similar_transitions) == 1:
                    transition = io_similar_transitions[0]
                    operations: List[BlockLabelElement] = []
                    for message_out_elem in transition.message_out:
                        operations.append(
                            BlockLabelElement(
                                operation=message_out_elem[0],
                                receiver=message_out_elem[1],
                            )
                        )
                    blocks.append(
                        Block(
                            label=BlockLabel(is_check=False, elems=operations),
                            is_input=True,
                            output_id=1,
                        )
                    )
                else:
                    # We assume that the check only happens (if ever) in the first message-out
                    # We assumed that the first message_outs in "similar" transitions have the same operation and receiver
                    msgs_out = io_similar_transitions[0].message_out
                    if len(msgs_out) == 0:
                        check = BlockLabelElement(
                            operation=io_similar_transitions[0].message_in, receiver=""
                        )
                    else:
                        first_message = io_similar_transitions[0].message_out[0]
                        check = BlockLabelElement(
                            operation=first_message[0],
                            receiver=first_message[1],
                        )
                    initial_block = Block(
                        label=BlockLabel(is_check=True, elems=[check]),
                        is_input=True,
                        output_id=None,
                    )
                    blocks.append(initial_block)

                    output_counter = 1
                    io_similar_transitions_copy = io_similar_transitions.copy()
                    io_similar_transitions_copy.sort(key=lambda x: x.to_transition)
                    for similar_transition in io_similar_transitions_copy:
                        operations: List[BlockLabelElement] = []
                        operations.append(
                            BlockLabelElement(
                                operation="None"
                                if similar_transition.return_v == None
                                else similar_transition.return_v,
                                receiver="",
                            )
                        )
                        for message_out in similar_transition.message_out[1:]:
                            operations.append(
                                BlockLabelElement(
                                    operation=message_out[0],
                                    receiver=message_out[1],
                                )
                            )
                        final_block = Block(
                            label=BlockLabel(is_check=False, elems=operations),
                            is_input=False,
                            output_id=output_counter,
                        )
                        output_counter += 1
                        if len(similar_transition.message_out) == 0:
                            block_transitions.append(
                                BlockTransition(
                                    from_block=initial_block,
                                    to_block=final_block,
                                    check=f"{similar_transition.return_v}",
                                )
                            )
                        else:
                            block_transitions.append(
                                BlockTransition(
                                    from_block=initial_block,
                                    to_block=final_block,
                                    check=f"{similar_transition.message_out[0][2]}",
                                )
                            )
                        blocks.append(final_block)
                state_machines.append(
                    CompositeStateStateMachine(
                        label=state_machine_label,
                        parent=state_machine_parent,
                        blocks=blocks,
                        transitions=block_transitions,
                    )
                )
        return state_machines

    def _io_2_state_machine(self):
        iostates = self.io_automat.states
        iotransitions = self.io_automat.transitions
        states = []
        for state in iostates:
            states.append(SimpleState(label=state))

        transitions = []
        iotransitions_copy = iotransitions.copy()
        iotransitions_copy.sort(key=lambda x: x.to_transition)

        for state in iostates:
            for msg_in in self._io_incoming_messages(state):
                ctr = 1
                for transition in iotransitions_copy:
                    if state != transition.from_transition or transition.message_in != msg_in:
                        continue
                    action = transition.message_in

                    composite_state = CompositeState(
                        label=action, parent=transition.from_transition
                    )

                    states.append(composite_state)

                    transitions.append(
                        Transition(
                            pre_state=transition.from_transition,
                            post_state=action,
                            type=TransitionTypeEnum.action,
                            action=action,
                            return_value=None,
                            exit_id=None,
                        )
                    )

                    transitions.append(
                        Transition(
                            pre_state=action,
                            post_state=transition.to_transition,
                            type=TransitionTypeEnum.ret,
                            action="",
                            return_value=transition.return_v,
                            exit_id=ctr,
                        )
                    )
                    ctr += 1

        return StateMachine(
            states=states,
            transitions=[
                transition
                for idx, transition in enumerate(transitions)
                if transition not in transitions[:idx]
            ],
        )

    def get_state(self, state_label):
        return (
            [state for state in self.state_machine.states if state.label == state_label]
        )[0]

    import os

    def generate_pydot_graph(self):
        graph = pydot.Dot(graph_type="digraph")

        # Add entry node
        graph.add_node(pydot.Node("entry", shape="circle", label="", fixedsize="true", width=0.2, height=0.2))

        # Add states to the graph
        for state in self.state_machine.states:
            node_shape = "box" if state.type == StateTypeEnum.simple else "hexagon"
            graph.add_node(pydot.Node(state.label, shape=node_shape))

        # Add initial states
        for s in self.initial_states:
            graph.add_edge(pydot.Edge("entry", s))

        # Add transitions to the graph
        for transition in self.state_machine.transitions:
            arrowhead = "normal" if self.get_state(transition.pre_state).type == StateTypeEnum.simple else "onormal"
            return_value = (
                transition.return_value
                if transition.return_value is not None
                else "return void"
                if transition.action == ""
                else ""
            )
            exit_id = "" if transition.exit_id is None else f"exit{transition.exit_id}"
            label = f"{exit_id}{transition.action} / {return_value}"

            # Check if the pre_state is a composite state (hexagon)
            if self.get_state(transition.pre_state).type == StateTypeEnum.composite:
                graph.add_edge(pydot.Edge(
                    transition.pre_state,
                    transition.post_state,
                    label=label,
                    arrowhead=arrowhead,
                    headlabel="",
                    labelfontsize=10,
                    fontsize=10,
                    dir="both",
                    arrowtail="dot"
                ))
            else:
                graph.add_edge(pydot.Edge(transition.pre_state, transition.post_state, label=label, arrowhead=arrowhead,
                                          fontsize=10))

        return graph

    def generate_uml_string(self):
        uml_string = "@startuml\n"
        uml_string += 'state "entry" as entry\n'

        for state in self.state_machine.states:
            node_shape = "rectangle" if state.type == StateTypeEnum.simple else "diamond"
            uml_string += f'state "{state.label}" as {state.label} <<{node_shape}>>\n'

        for transition in self.state_machine.transitions:
            return_value = (
                transition.return_value
                if transition.return_value is not None
                else "return void"
                if transition.action == ""
                else ""
            )
            exit_id = "" if transition.exit_id is None else f"exit{transition.exit_id}"
            label = f"{exit_id}{transition.action} / {return_value}"
            uml_string += f"{transition.pre_state} --> {transition.post_state} : {label}\n"

        uml_string += "@enduml\n"
        return uml_string

    def visualize_uml(self, filepath):
        graph = self.generate_pydot_graph()
        folder_name = os.path.basename(filepath)
        output_path_png = f"{filepath}/state_machine_{folder_name}.png"
        output_path_uml = f"{filepath}/state_machine_{folder_name}.uml"
        graph.write_png(output_path_png)

        uml_string = self.generate_uml_string()
        with open(output_path_uml, 'w') as f:
            f.write(uml_string)

    def block_label_to_str(self, blockLabel: BlockLabel):
        elems = blockLabel.elems
        if blockLabel.is_check:
            return f"check := {elems[0].receiver}.{elems[0].operation}"
        else:
            ans = ""
            for e in elems:
                if e.receiver == "":
                    continue
                ans += f"{e.receiver}.{e.operation}\\n"
            return ans

    def generate_composite_pydot_graph(self, machine):
        graph = pydot.Dot(graph_type="digraph")

        aliasDict: Dict[str, str] = {}
        ctr = 1
        for s in machine.blocks:
            aliasDict.update({str(s): f"state_{ctr}"})
            ctr += 1

        def alias(s):
            return aliasDict[str(s)]

        # Add composite state
        subgraph = pydot.Cluster(machine.label, label=machine.label, style="rounded")

        # Add entry node to the subgraph
        subgraph.add_node(
            pydot.Node(f"{machine.label}_entry", shape="circle", label="", fixedsize="true", width=0.2, height=0.2))

        # Add blocks to the subgraph
        for block in machine.blocks:
            label = f"do / \\n{self.block_label_to_str(block.label)}"
            subgraph.add_node(pydot.Node(alias(block), label=label, shape="box", labelloc="t"))
            if block.output_id:
                # Custom exit node with a cross inside and text below
                exit_label = f"<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0' CELLPADDING='0'><TR><TD>           X   exit{block.output_id}</TD></TR></TABLE>>"
                subgraph.add_node(
                    pydot.Node(f"exit{block.output_id}", shape="circle", label=exit_label, fixedsize="true", width=0.2,
                               height=0.2))
                subgraph.add_edge(pydot.Edge(alias(block), f"exit{block.output_id}"))
            if block.is_input:
                subgraph.add_edge(pydot.Edge(f"{machine.label}_entry", alias(block)))

        # Add transitions within the subgraph
        for transition in machine.transitions:
            subgraph.add_edge(pydot.Edge(alias(transition.from_block), alias(transition.to_block),
                                         label=f"[check = {transition.check}]"))

        graph.add_subgraph(subgraph)
        return graph

    def generate_composite_uml_string(self, machine):
        uml_string = "@startuml\n"
        uml_string += f'state "{machine.label}" as {machine.label} {{\n'
        uml_string += f'  state "entry" as {machine.label}_entry\n'

        aliasDict: Dict[str, str] = {}
        ctr = 1
        for s in machine.blocks:
            aliasDict.update({str(s): f"state_{ctr}"})
            ctr += 1

        def alias(s):
            return aliasDict[str(s)]

        for block in machine.blocks:
            label = f"do / \\n{self.block_label_to_str(block.label)}"
            uml_string += f'  state "{label}" as {alias(block)}\n'
            if block.output_id:
                uml_string += f'  state "X exit{block.output_id}" as exit{block.output_id}\n'
                uml_string += f'  {alias(block)} --> exit{block.output_id}\n'
            if block.is_input:
                uml_string += f'  {machine.label}_entry --> {alias(block)}\n'

        for transition in machine.transitions:
            uml_string += f'  {alias(transition.from_block)} --> {alias(transition.to_block)} : [check = {transition.check}]\n'

        uml_string += "}\n@enduml\n"
        return uml_string

    def visualize_composite_state_state_machines(self, filepath):
        state_machines = self.composite_state_state_machines
        for machine in state_machines:
            graph = self.generate_composite_pydot_graph(machine)
            folder_name = os.path.basename(filepath)
            output_path_png = f"{filepath}/composite_state_{folder_name}_{machine.label}.png"
            output_path_uml = f"{filepath}/composite_state_{folder_name}_{machine.label}.uml"
            graph.write_png(output_path_png)

            uml_string = self.generate_composite_uml_string(machine)
            with open(output_path_uml, 'w') as f:
                f.write(uml_string)

