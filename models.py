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
        return f"Communication({self.prestate}, {self.sender}, {self.operation}, {self.receiver}, {self.return_v}, {self.post_state})"


class Scenario:
    def __init__(self, name: str, communications: list[Communication]):
        self.name = name
        self.communications = communications

    def __repr__(self):
        return f"Scenario({self.name}, {self.communications})"


class BehaviorBlock:
    def __init__(self, prestate: str, messagee_in: str, messageout: list[Tuple[str, str, str]], return_v: str,
                 poststate: str):
        self.prestate = prestate
        self.messagee_in = messagee_in
        self.messageout = messageout
        self.return_v = return_v
        self.poststate = poststate

    def __repr__(self):
        return f"BehaviorBlock({self.prestate}, {self.messagee_in}, {self.messageout}, {self.return_v}, {self.poststate})"


class Behavior:
    def __init__(self,scenario_name:str,   object: str, behavior: list[BehaviorBlock]):
        self.scenario_name = scenario_name
        self.object = object
        self.behavior = behavior

    def __repr__(self):
        return f"Behavior({self.scenario_name}, {self.object}, {self.behavior})"


class Transition:
    def __init__(self, from_transition: str, to_transition: str, message_in: str, message_out: list[Tuple[str, str, str]],
                 return_v: str):
        self.from_transition = from_transition
        self.to_transition = to_transition
        self.message_in = message_in
        self.message_out = message_out
        self.return_v = return_v

    def __repr__(self):
        return f"Transition({self.from_transition}, {self.to_transition}, {self.message_in}, {self.message_out}, {self.return_v})"

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
        return f"IOAutomaton({self.states}, {self.transitions})"
    
class CompositeState:
    name: str # same as message_in

    # if empty do one node: so actions is len 1. if not empty, write the check in the first box
    # then come a list of actions
    check: dict[str, list[str]]
    actions: list[str]

    # example enterpassword:
    # check = {"consortium.verifyaccount" : [Ok, badPassword, badAccount]}
    # actions  = ["", "user.requestPassword", "user.BadAccountMessage \n user.printReceipt \n user.ejectCard"]

    # example cancel:
    # check = {}
    # actions = ["user.canceledMessage, user.ejectCard, user.requestTakeCard"]

    def __init__(self, name: str, check: dict[str, list[str]], actions: list[str]):
        self.name = name
        self.check = check
        self.actions = actions

    def __repr__(self) -> str:
        return f"CompositeState(name='{self.name}', check={self.check}, actions={self.actions})"

class StateMachine:
    states: list[str] # mouraba3
    actions: list[str] # mou3ayan
    transitions: list[Transition]

    def __init__(self,  states: list[str], actions: list[str], transitions: list[Transition]):

        self.states = states
        self.actions = actions
        self.transitions = transitions

    def __repr__(self) -> str:
        return f"StateMachine( states={self.states}, actions={self.actions}, transitions={self.transitions})"