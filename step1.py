from xml.dom.minidom import parse, Element

class Scenario:
    def __init__(self, prestate, sender, operation, receiver, return_v, post_state):
        self.prestate = prestate
        self.sender = sender
        self.operation = operation
        self.receiver = receiver
        self.return_v = return_v
        self.post_state = post_state

def get_text(node):
    return node.firstChild.nodeValue if node.firstChild else ''

def parse_scenario(xml_file):
    dom = parse(xml_file)
    scenarios = []

    # Find all interactions
    interactions = dom.getElementsByTagName('packagedElement')
    for interaction in interactions:
        if interaction.getAttribute('xmi:type') == 'uml:Interaction':
            lifelines = {}
            messages = {}
            state_invariants = {}

            # Parse lifelines
            for lifeline in interaction.getElementsByTagName('lifeline'):
                lifeline_id = lifeline.getAttribute('xmi:id')
                lifelines[lifeline_id] = lifeline.getAttribute('name')

            # Parse messages
            for message in interaction.getElementsByTagName('message'):
                message_id = message.getAttribute('xmi:id')
                sender = message.getAttribute('sendEvent')
                receiver = message.getAttribute('receiveEvent')
                operation = message.getAttribute('name')
                messages[message_id] = (sender, operation, receiver)

            # Parse state invariants
            for invariant in interaction.getElementsByTagName('fragment'):
                if invariant.getAttribute('xmi:type') == 'uml:StateInvariant':
                    state_invariant_id = invariant.getAttribute('xmi:id')
                    state_invariants[state_invariant_id] = invariant.getAttribute('name')

            # Create scenarios
            for message_id, (sender_id, operation, receiver_id) in messages.items():
                prestate = state_invariants.get(sender_id, '')
                post_state = state_invariants.get(receiver_id, '')
                sender = lifelines.get(sender_id, '')
                receiver = lifelines.get(receiver_id, '')

                scenarios.append(Scenario(prestate, sender, operation, receiver, '', post_state))

    return scenarios

# Example usage
xml_file = 'MDD_Model.uml'
scenarios = parse_scenario(xml_file)

for scenario in scenarios:
    print(f"Prestate: {scenario.prestate}, Sender: {scenario.sender}, Operation: {scenario.operation}, Receiver: {scenario.receiver}, Return: {scenario.return_v}, Post-state: {scenario.post_state}")
