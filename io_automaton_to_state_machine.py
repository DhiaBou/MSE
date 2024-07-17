# STEP 4.2
from models import *


def _io_in_messages(state: str, automat: IOAutomaton):
    return [
        transition.message_in
        for transition in automat.transitions
        if transition.from_transition == state
    ]


def get_state_machine(automat: IOAutomaton) -> StateMachine:
    states_from_io = automat.states
    actions = []
    transitions_from_io = automat.transitions
    transition_state_machine = []
    iotransitions_sorted = transitions_from_io.copy()
    iotransitions_sorted.sort(key=lambda x: x.to_transition)
    for state in states_from_io:
        incoming_messages = _io_in_messages(state=state, automat=automat)
        for message_in in incoming_messages:
            exit_nr = 1
            for transition in iotransitions_sorted:
                if transition.from_transition != state or transition.message_in != message_in:
                    continue
                label = transition.message_in
                if label not in actions:
                    actions.append(label)
                transition_temp_from = (
                    Transition(
                        from_transition=transition.from_transition,
                        to_transition=label,
                        message_in=label,
                        message_out=[],
                        return_v=""
                    ))
                if transition_temp_from not in transition_state_machine:
                    transition_state_machine.append(transition_temp_from)
                transition_temp_to = (Transition
                        (
                        from_transition=label,
                        to_transition=transition.to_transition,
                        message_in=f"exit{exit_nr}",
                        message_out=[],
                        return_v=transition.return_v
                    ))
                if transition_temp_to not in transition_state_machine:
                    transition_state_machine.append(transition_temp_to)


                exit_nr += 1

    return StateMachine(
        states=states_from_io,
        actions=actions,
        transitions=transition_state_machine

    )


def get_state_machines(io_automata: dict[str, IOAutomaton]) -> dict[str, StateMachine]:
    state_machines = {}
    for obj, io_auomtaton in io_automata.items():
        state_machines[obj] = get_state_machine(io_auomtaton)
    return state_machines
