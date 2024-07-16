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

    for state in states_from_io:
        incoming_messages = _io_in_messages(state=state, automat=automat)
        for message_in in incoming_messages:
            for transition in transitions_from_io:
                if transition.from_transition != state or transition.message_in != message_in:
                    continue
                label = transition.message_in
                if label not in actions:
                    actions.append(label)
                transition_state_machine.append(
                    Transition(
                        from_transition=transition.from_transition,
                        to_transition=label,
                        message_in=label,
                        message_out=[],
                        return_v=""
                    )
                )
                transition_state_machine.append(
                    Transition
                        (
                        from_transition=label,
                        to_transition=transition.to_transition,
                        message_in="exit1",
                        message_out=[],
                        return_v=transition.return_v
                    )

                )

    return StateMachine(
        states=states_from_io,
        actions=actions,
        transitions=transition_state_machine,

    )


def get_state_machines(io_automata: dict[str, IOAutomaton]):
    state_machines = {}
    for obj, io_auomtaton in io_automata.items():
        state_machines[obj] = get_state_machine(io_auomtaton)
    return state_machines
