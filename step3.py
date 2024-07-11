# KARIM OR MALEK if you are ready, discuss the next steps


from models import *
from typing import Dict, List


import pydot

import os


def get_io_from_behavior(behaviors: List[Behavior]) -> Dict[str, IOAutomaton]:
    automata = {}

    for behavior in behaviors:
        obj = behavior.object
        if obj not in automata:
            automata[obj] = IOAutomaton(states=[], transitions=[])
        io_automaton = automata[obj]

        for block in behavior.behavior:
            if block.prestate not in io_automaton.states:
                io_automaton.states.append(block.prestate)
            if block.poststate not in io_automaton.states:
                io_automaton.states.append(block.poststate)

            transition = Transition(
                from_transition=block.prestate,
                to_transition=block.poststate,
                message_in=block.messagee_in,
                message_out=block.messageout,
                return_v=block.return_v
            )

            duplicate_found = False
            for existing_transition in io_automaton.transitions:
                if (existing_transition.from_transition == transition.from_transition and
                        existing_transition.to_transition == transition.to_transition and
                        existing_transition.message_in == transition.message_in and
                        existing_transition.return_v == transition.return_v):
                    existing_transition.message_out.extend(transition.message_out)
                    duplicate_found = True
                    break

            if not duplicate_found:
                io_automaton.transitions.append(transition)

    for obj, io_automaton in automata.items():
        for transition in io_automaton.transitions:
            transition.message_out = list(dict.fromkeys(transition.message_out))
        io_automaton.states = list(io_automaton.states)
    return automata


def visualizer(io_automata: Dict[str, IOAutomaton]) -> None:
    output_dir = "IOAutomata"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for obj, automaton in io_automata.items():
        if not automaton.transitions:
            continue

        start_state = automaton.transitions[0].from_transition # Change this eventually to the pre state of the first behaviour

        uml_filename = os.path.join(output_dir, f"{obj}.uml")
        jpg_filename = os.path.join(output_dir, f"{obj}.jpg")

        with open(uml_filename, 'w') as uml_file:
            uml_file.write(f"@startuml\n")
            uml_file.write(f"[*] --> {start_state}\n")

            for state in automaton.states:
                uml_file.write(f"state {state}\n")

            for transition in automaton.transitions:
                from_state = transition.from_transition
                to_state = transition.to_transition
                message_in = transition.message_in
                message_out_lines = "\n".join([f"<{msg[0]}, {msg[1]}, {msg[2]}>" for msg in transition.message_out])
                return_v = transition.return_v or "void"

                uml_file.write(f"{from_state} --> {to_state} : {message_in} / \n{message_out_lines}\n{return_v}\n")

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

        for state in automaton.states:
            node = pydot.Node(state, shape="rectangle")
            graph.add_node(node)

        for transition in automaton.transitions:
            from_state = transition.from_transition
            to_state = transition.to_transition
            label = f"{transition.message_in} /\n" + "\n".join([f"<{msg[0]}, {msg[1]}, {msg[2]}>" for msg in transition.message_out]) + f"\n{transition.return_v or 'void'}"
            edge = pydot.Edge(from_state, to_state, label=label)
            graph.add_edge(edge)

        # Save the graph as a jpg file
        graph.write_jpg(jpg_filename)


# Example usage
behaviors = [
    Behavior(scenario_name='Bad account', object='atm', behavior=[
        BehaviorBlock(prestate='WaitCard', messagee_in='insertCard', messageout=[('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'badAccount'), ('badAccountMessage', 'user', 'void'),
                                  ('printReceipt', 'user', 'void'), ('ejectCard', 'user', 'void'),
                                  ('requestTakeCard', 'user', 'void')], return_v='void', poststate='WaitTakeCard'),
        BehaviorBlock(prestate='WaitTakeCard', messagee_in='takeCard',
                      messageout=[('displayMainScreen', 'user', 'void')],
                      return_v='void', poststate='WaitCard')]),
    Behavior(scenario_name='Bad password', object='atm', behavior=[
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'badPassword'), ('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='cancel',
                      messageout=[('canceledMessage', 'user', 'void'), ('ejectCard', 'user', 'void'),
                                  ('requestTakeCard', 'user', 'void')], return_v='void', poststate='WaitTakeCard')]),
    Behavior(scenario_name='GoodAccount', object='atm', behavior=[
        BehaviorBlock(prestate='WaitCard', messagee_in='insertCard', messageout=[('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'OK')], return_v='void', poststate='WaitAmount')]),
    Behavior(scenario_name='Bad account', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[],
                      return_v='badBankAccount', poststate='WaitBankVerify')]),
    Behavior(scenario_name='Bad password', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[],
                      return_v='badBankPassword', poststate='WaitBankVerify')]),
    Behavior(scenario_name='GoodAccount', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[], return_v='OK',
                      poststate='WaitBankVerify')]),
    Behavior(scenario_name='Bad account', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'badBankAccount')], return_v='badAccount',
                      poststate='WaitVerify')]),
    Behavior(scenario_name='Bad password', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'badBankPassword')], return_v='badPassword',
                      poststate='WaitVerify')]),
    Behavior(scenario_name='GoodAccount', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'OK')], return_v='OK', poststate='WaitVerify')])
]

io_automata = get_io_from_behavior(behaviors)
visualizer(io_automata)

for obj, automaton in io_automata.items():
    print(f"Object: {obj}")
    print(f"States: {automaton.states}")
    for transition in automaton.transitions:
        print(
            f"Transition: {transition.from_transition} -> {transition.to_transition}, message_in: {transition.message_in}, message_out: {transition.message_out}, return_v: {transition.return_v}")



#def write_to_uml(io_automaton: dict[str:IOAutomaton]) -> None:
#    res: str = ""
#    destination: str = "result.uml"
#    print("I am writing res to destination")
#    pass