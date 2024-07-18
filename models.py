from typing import Tuple


class Communication:
    def __init__(self, prestate: str, sender: str, operation: str, receiver: str, return_v: str, post_state: str):
        self.prestate = prestate
        self.sender = sender
        self.operation = operation
        self.receiver = receiver
        self.return_v = return_v
        self.post_state = post_state

    def __repr__(self):
        return (
            "Communication(\n"
            f"    Prestate: {self.prestate}\n"
            f"    Sender: {self.sender}\n"
            f"    Operation: {self.operation}\n"
            f"    Receiver: {self.receiver}\n"
            f"    Return Value: {self.return_v}\n"
            f"    Post State: {self.post_state}\n"
            ")"
        )


class Scenario:
    def __init__(self, name: str, communications: list[Communication]):
        self.name = name
        self.communications = communications

    def __repr__(self):
        communications_repr = "\n    ".join(repr(c) for c in self.communications)
        return (
            "Scenario(\n"
            f"    Name: {self.name}\n"
            f"    Communications: [\n        {communications_repr}\n    ]\n"
            ")"
        )


class BehaviorBlock:
    def __init__(self, prestate: str, messagee_in: str, messageout: list[Tuple[str, str, str]], return_v: str,
                 poststate: str):
        self.prestate = prestate
        self.messagee_in = messagee_in
        self.messageout = messageout
        self.return_v = return_v
        self.poststate = poststate

    def __repr__(self):
        messageout_repr = "\n        ".join(f"{m}" for m in self.messageout)
        return (
            "BehaviorBlock(\n"
            f"    Prestate: {self.prestate}\n"
            f"    Message In: {self.messagee_in}\n"
            f"    Message Out: [\n        {messageout_repr}\n    ]\n"
            f"    Return Value: {self.return_v}\n"
            f"    Poststate: {self.poststate}\n"
            ")"
        )


class Behavior:
    def __init__(self, scenario_name: str, object: str, behavior: list[BehaviorBlock]):
        self.scenario_name = scenario_name
        self.object = object
        self.behavior = behavior

    def __repr__(self):
        behavior_repr = "\n    ".join(repr(b) for b in self.behavior)
        return (
            "Behavior(\n"
            f"    Scenario Name: {self.scenario_name}\n"
            f"    Object: {self.object}\n"
            f"    Behavior: [\n        {behavior_repr}\n    ]\n"
            ")"
        )


class Transition:
    def __init__(self, from_transition: str, to_transition: str, message_in: str, message_out: list[Tuple[str, str, str]],
                 return_v: str):
        self.from_transition = from_transition
        self.to_transition = to_transition
        self.message_in = message_in
        self.message_out = message_out
        self.return_v = return_v

    def __repr__(self):
        message_out_repr = "\n        ".join(f"{m}" for m in self.message_out)
        return (
            "Transition(\n"
            f"    From Transition: {self.from_transition}\n"
            f"    To Transition: {self.to_transition}\n"
            f"    Message In: {self.message_in}\n"
            f"    Message Out: [\n        {message_out_repr}\n    ]\n"
            f"    Return Value: {self.return_v}\n"
            ")"
        )

    def __eq__(self, other):
        if not isinstance(other, Transition):
            return False

        return (self.from_transition == other.from_transition and
                self.to_transition == other.to_transition and
                self.message_in == other.message_in and
                self.message_out == other.message_out and
                self.return_v == other.return_v)


class IOAutomaton:
    def __init__(self, states: list[str], transitions: list[Transition]):
        self.states = states
        self.transitions = transitions

    def __repr__(self):
        transitions_repr = "\n    ".join(repr(t) for t in self.transitions)
        return (
            "IOAutomaton(\n"
            f"    States: {self.states}\n"
            f"    Transitions: [\n        {transitions_repr}\n    ]\n"
            ")"
        )


class CompositeState:
    def __init__(self, name: str, check: dict[str, list[str]], actions: list[str]):
        self.name = name
        self.check = check
        self.actions = actions

    def __repr__(self):
        check_repr = "\n        ".join(f"{k}: {v}" for k, v in self.check.items())
        return (
            "CompositeState(\n"
            f"    Name: {self.name}\n"
            f"    Check: {{\n        {check_repr}\n    }}\n"
            f"    Actions: {self.actions}\n"
            ")"
        )


class StateMachine:
    def __init__(self, states: list[str], actions: list[str], transitions: list[Transition]):
        self.states = states
        self.actions = actions
        self.transitions = transitions

    def __repr__(self):
        transitions_repr = "\n    ".join(repr(t) for t in self.transitions)
        return (
            "StateMachine(\n"
            f"    States: {self.states}\n"
            f"    Actions: {self.actions}\n"
            f"    Transitions: [\n        {transitions_repr}\n    ]\n"
            ")"
        )
