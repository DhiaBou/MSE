class Scenario:
    prestate: str
    sender: str
    operation: str
    receiver: str
    return_v: str
    post_state: str


class BehaviorBlock:
    prestate: str
    messagee_in: str
    messageout: list[tuple[str]]
    return_v: str
    poststate: str


class Behavior:
    scenario_name: str
    object: str
    behavior: list[BehaviorBlock]


class Transition:
    from_transition: str
    to_transition: str
    message_in: str
    message_out: list[tuple[str]]
    return_v: str


class IOAutomaton:
    states: list[str]
    transitions: list[Transition]


class Transition:
    from_transition: str
    to_transition: str
    message_in: str
    message_out: list[tuple[str]]
    return_v: str
