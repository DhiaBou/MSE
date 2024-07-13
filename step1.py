from xml.dom.minidom import parse
from models import Communication, Scenario

def get_elements_by_tag_name(element, tag_name):
    return [child for child in element.childNodes if child.nodeType == child.ELEMENT_NODE and child.tagName == tag_name]

def extract_lifelines(interaction):
    lifelines = get_elements_by_tag_name(interaction, "lifeline")
    return {lifeline.getAttribute("xmi:id"): lifeline.getAttribute("name") for lifeline in lifelines}

def extract_messages(interaction, lifeline_objects):
    scenario = Scenario("", [])
    fragments = get_elements_by_tag_name(interaction, "fragment")
    messages = get_elements_by_tag_name(interaction, "message")
    replies = {}

    for message in messages:
        message_name = message.getAttribute("name")
        receive_fragment = [fragment for fragment in fragments if fragment.getAttribute("xmi:id") == message.getAttribute("receiveEvent")][0]
        send_fragment = [fragment for fragment in fragments if fragment.getAttribute("xmi:id") == message.getAttribute("sendEvent")][0]
        
        receiver_id = receive_fragment.getAttribute("covered")
        sender_id = send_fragment.getAttribute("covered")

        prestate_fragment = receive_fragment.previousSibling
        poststate_fragment = receive_fragment.nextSibling
        prestate = "-"
        poststate = "-"

        while prestate_fragment is not None:
            if prestate_fragment.nodeType == receive_fragment.ELEMENT_NODE and prestate_fragment.tagName == receive_fragment.tagName and prestate_fragment.getAttribute("xmi:type") == "uml:StateInvariant" and prestate_fragment.getAttribute("covered") == receiver_id:
                prestate = prestate_fragment.getAttribute("name")
                break
            prestate_fragment = prestate_fragment.previousSibling

        while poststate_fragment is not None:
            if poststate_fragment.nodeType == poststate_fragment.ELEMENT_NODE and poststate_fragment.tagName == receive_fragment.tagName and poststate_fragment.getAttribute("xmi:type") == "uml:StateInvariant" and poststate_fragment.getAttribute("covered") == receiver_id:
                poststate = poststate_fragment.getAttribute("name")
                break
            poststate_fragment = poststate_fragment.nextSibling

        if message.getAttribute("messageSort") == "reply":
            original_message_name = receive_fragment.getAttribute("name").split("_Message")[0]
            replies[original_message_name] = message_name
            continue

        scenario.communications.append(Communication(
            prestate, 
            lifeline_objects[sender_id], 
            message_name, 
            lifeline_objects[receiver_id], 
            "void", 
            poststate
        ))

    for communication in scenario.communications:
        if communication.operation in replies.keys():
            communication.return_v = replies[communication.operation]

    return scenario

def generate_table_from_model(file_path):
    dom = parse(file_path)
    interactions = get_elements_by_tag_name(dom.firstChild, "packagedElement")
    scenarios = []

    for interaction in interactions:
        if interaction.getAttribute("xmi:type") == "uml:Interaction":
            scenario_name = interaction.getAttribute("name")
            lifelines = extract_lifelines(interaction)
            scenario = extract_messages(interaction, lifelines)
            scenario.name = scenario_name
            scenarios.append(scenario)

    return scenarios
scenarios = generate_table_from_model("MDD_Model.uml")
print(scenarios)