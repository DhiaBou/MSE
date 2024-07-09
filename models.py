from typing import List, Tuple

class Scenario:
    def __init__(self, prestate: str, sender: str, operation: str, receiver: str, return_v: str, post_state: str):
        self.prestate = prestate
        self.sender = sender
        self.operation = operation
        self.receiver = receiver
        self.return_v = return_v
        self.post_state = post_state

    def __repr__(self):
        return f"Scenario({self.prestate}, {self.sender}, {self.operation}, {self.receiver}, {self.return_v}, {self.post_state})"


class BehaviorBlock:
    def __init__(self, prestate: str, messagee_in: str, messageout: List[Tuple[str]], return_v: str, poststate: str):
        self.prestate = prestate
        self.messagee_in = messagee_in
        self.messageout = messageout
        self.return_v = return_v
        self.poststate = poststate

    def __repr__(self):
        return f"BehaviorBlock({self.prestate}, {self.messagee_in}, {self.messageout}, {self.return_v}, {self.poststate})"


class Behavior:
    def __init__(self, scenario_name: str, object: str, behavior: List[BehaviorBlock]):
        self.scenario_name = scenario_name
        self.object = object
        self.behavior = behavior

    def __repr__(self):
        return f"Behavior({self.scenario_name}, {self.object}, {self.behavior})"


class Transition:
    def __init__(self, from_transition: str, to_transition: str, message_in: str, message_out: List[Tuple[str]], return_v: str):
        self.from_transition = from_transition
        self.to_transition = to_transition
        self.message_in = message_in
        self.message_out = message_out
        self.return_v = return_v

    def __repr__(self):
        return f"Transition({self.from_transition}, {self.to_transition}, {self.message_in}, {self.message_out}, {self.return_v})"


class IOAutomaton:
    def __init__(self, states: List[str], transitions: List[Transition]):
        self.states = states
        self.transitions = transitions

    def __repr__(self):
        return f"IOAutomaton({self.states}, {self.transitions})"