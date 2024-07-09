

class Scenario:
    prestate: str
    sender: str
    operatoin: str
    receiver: str
    reurn: str
    post_state: str


class Behaviour:
    scenario_name:str
    object:str
    behaviour: list[BehaviourBlock]

class BehaviourBlock:
    prestate: str
	messagee_in: str
	messageout: list[tuple[str]]
	return_v:str
	poststate:str

xml_file = "hi.xml"

xml_to_table(xml_file: str) -> Scenario:
    pass







