import os

from models import *
from typing import Dict, List
from step2 import get_behaviors
from step3 import get_io_from_behavior, visualizer
from step4 import IO2UML

# xml_file = "hi.xml"


# table = xml_to_table(xml_file)

# print(table)


input = {'Bad account': [
    Communication(prestate='WaitCard', sender='user', operation='insertCard', receiver='atm', return_v="void",
                  post_state='WaitPassword'),
    Communication(prestate="_", sender='atm', operation='requestPassword', receiver='user', return_v="void",
                  post_state="_"),
    Communication(prestate='WaitPassword', sender='user', operation='enterPassword', receiver='atm', return_v="void",
                  post_state='WaitTakeCard'),
    Communication(prestate='WaitVerify', sender='atm', operation='verifyAccount', receiver='consortium',
                  return_v='badAccount', post_state='WaitVerify'),
    Communication(prestate='WaitBankVerify', sender='consortium', operation='verifyCardWithBank', receiver='bank',
                  return_v='badBankAccount', post_state='WaitBankVerify'),
    Communication(prestate="_", sender='atm', operation='badAccountMessage', receiver='user', return_v="void",
                  post_state="_"),
    Communication(prestate="_", sender='atm', operation='printReceipt', receiver='user', return_v="void",
                  post_state="_"),
    Communication(prestate="_", sender='atm', operation='ejectCard', receiver='user', return_v="void", post_state="_"),
    Communication(prestate="_", sender='atm', operation='requestTakeCard', receiver='user', return_v="void",
                  post_state="_"),
    Communication(prestate='WaitTakeCard', sender='user', operation='takeCard', receiver='atm', return_v="void",
                  post_state='WaitCard'),
    Communication(prestate="_", sender='atm', operation='displayMainScreen', receiver='user', return_v="void",
                  post_state="_")],
    'Bad password': [
        Communication(prestate='WaitPassword', sender='user', operation='enterPassword', receiver='atm',
                      return_v="void", post_state='WaitPassword'),
        Communication(prestate='WaitVerify', sender='atm', operation='verifyAccount', receiver='consortium',
                      return_v='badPassword', post_state='WaitVerify'),
        Communication(prestate='WaitBankVerify', sender='consortium', operation='verifyCardWithBank',
                      receiver='bank', return_v='badBankPassword', post_state='WaitBankVerify'),
        Communication(prestate="_", sender='atm', operation='requestPassword', receiver='user', return_v="void",
                      post_state="_"),
        Communication(prestate='WaitPassword', sender='user', operation='cancel', receiver='atm', return_v="void",
                      post_state='WaitTakeCard'),
        Communication(prestate="_", sender='atm', operation='canceledMessage', receiver='user', return_v="void",
                      post_state="_"),
        Communication(prestate="_", sender='atm', operation='ejectCard', receiver='user', return_v="void",
                      post_state="_"),
        Communication(prestate="_", sender='atm', operation='requestTakeCard', receiver='user', return_v="void",
                      post_state="_")],
    'GoodAccount': [
        Communication(prestate='WaitCard', sender='user', operation='insertCard', receiver='atm', return_v="void",
                      post_state='WaitPassword'),
        Communication(prestate="_", sender='atm', operation='requestPassword', receiver='user', return_v="void",
                      post_state="_"),
        Communication(prestate='WaitPassword', sender='user', operation='enterPassword', receiver='atm',
                      return_v="void", post_state='WaitAmount'),
        Communication(prestate='WaitVerify', sender='atm', operation='verifyAccount', receiver='consortium',
                      return_v='OK', post_state='WaitVerify'),
        Communication(prestate='WaitBankVerify', sender='consortium', operation='verifyCardWithBank',
                      receiver='bank', return_v='OK', post_state='WaitBankVerify')]}

def get_initial_states(behaviors: List[Behavior]) -> Dict[str, List[str]]:
    initial_states: Dict[str, List[str]] = {}

    for behavior in behaviors:
        init = []
        for behaviorBlockObject in behavior.behavior:
            init.append(behaviorBlockObject.prestate)
            break  # very hacky work around, the assumption is wrong
        initial_states.update({behavior.object: list(set(init))})

    return initial_states

artefacts_folder = "Artefacts"
uml_artefacts_folder = f"{artefacts_folder}/Uml"
io_automata_artefacts_folder = f"{artefacts_folder}/IOAutomata"

# Print each behavior on a separate line
scenarios = []
for scenario_name, scenario in input.items():
    # print(scenario_name)
    scenarios.append(Scenario(scenario_name, scenario))

behaviors = get_behaviors(scenarios)

io_automata = get_io_from_behavior(behaviors)
visualizer(io_automata, io_automata_artefacts_folder)

initial_states = get_initial_states(behaviors)

for obj, automat in io_automata.items():
    uml = IO2UML(io_automata[obj], initial_states[obj])
    os.makedirs(f"{uml_artefacts_folder}/{obj}", exist_ok=True)
    uml.visualize_uml(f"{uml_artefacts_folder}/{obj}")
    uml.visualize_composite_state_state_machines(f"{uml_artefacts_folder}/{obj}")

#for obj, automaton in io_automata.items():
#    print(f"Object: {obj}")
#    print(f"States: {automaton.states}")
#    for transition in automaton.transitions:
#        print(
#            f"Transition: {transition.from_transition} -> {transition.to_transition}, message_in: {transition.message_in}, message_out: {transition.message_out}, return_v: {transition.return_v}")



# print(behaviors)

# print(io_automaton)

# write_to_uml(io_automaton)
