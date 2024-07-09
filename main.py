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


xml_file = "hi.xml"


def xml_to_table(xml_file: str) -> list[Scenario]:
    pass


table = xml_to_table(xml_file)


# key is object, value is list of scenarios
def table_to_projections(table: list[Scenario]) -> dict[str : list[Scenario]]:
    pass


projections = table_to_projections(table)


def projections_to_behavior(projections: dict[str : list[Scenario]]) -> list[Behavior]:
    pass


behavior = projections_to_behavior(projections)


def get_io_from_behavior(behavior: list[Behavior]) -> dict[str:IOAutomaton]:
    pass


io_automaton = get_io_from_behavior(behavior)


def write_to_uml(io_automaton: dict[str:IOAutomaton]) -> None:
    res: str = ""
    destination: str = "result.uml"
    print("I am writing res to destination")
    pass
