# KARIM OR MALEK if you are ready, discuss the next steps


from models import *
from typing import Dict, List


def get_io_from_behavior(behaviors: List[Behavior]) -> Dict[str, IOAutomaton]:
    automata = {}

    for behavior in behaviors:
        obj = behavior.object
        if obj not in automata:
            automata[obj] = IOAutomaton(states=[], transitions=[])

        io_automaton = automata[obj]

        for block in behavior.behavior:
            # Add states if not already present
            if block.prestate not in io_automaton.states:
                io_automaton.states.append(block.prestate)
            if block.poststate not in io_automaton.states:
                io_automaton.states.append(block.poststate)

            # Create transition and add to automaton
            transition = Transition(
                from_transition=block.prestate,
                to_transition=block.poststate,
                message_in=block.messagee_in,
                message_out=block.messageout,
                return_v=block.return_v
            )
            # Check for duplicate transitions
            duplicate_found = False
            for existing_transition in io_automaton.transitions:
                if (existing_transition.from_transition == transition.from_transition and
                        existing_transition.to_transition == transition.to_transition and
                        existing_transition.message_in == transition.message_in and
                        existing_transition.return_v == transition.return_v):
                    existing_transition.message_out.extend(transition.message_out)
                    duplicate_found = True
                    break

            if not duplicate_found:
                io_automaton.transitions.append(transition)

            # Remove duplicate output messages
    for obj, io_automaton in automata.items():
        for transition in io_automaton.transitions:
            transition.message_out = list(dict.fromkeys(transition.message_out))
        io_automaton.states = list(io_automaton.states)

    return automata




# Example usage
behaviors = [
    Behavior(scenario_name='Bad account', object='atm', behavior=[
        BehaviorBlock(prestate='WaitCard', messagee_in='insertCard', messageout=[('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'badAccount'), ('badAccountMessage', 'user', 'void'),
                                  ('printReceipt', 'user', 'void'), ('ejectCard', 'user', 'void'),
                                  ('requestTakeCard', 'user', 'void')], return_v='void', poststate='WaitTakeCard'),
        BehaviorBlock(prestate='WaitTakeCard', messagee_in='takeCard', messageout=[('displayMainScreen', 'user', 'void')],
                      return_v='void', poststate='WaitCard')]),
    Behavior(scenario_name='Bad password', object='atm', behavior=[
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'badPassword'), ('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='cancel',
                      messageout=[('canceledMessage', 'user', 'void'), ('ejectCard', 'user', 'void'),
                                  ('requestTakeCard', 'user', 'void')], return_v='void', poststate='WaitTakeCard')]),
    Behavior(scenario_name='GoodAccount', object='atm', behavior=[
        BehaviorBlock(prestate='WaitCard', messagee_in='insertCard', messageout=[('requestPassword', 'user', 'void')],
                      return_v='void', poststate='WaitPassword'),
        BehaviorBlock(prestate='WaitPassword', messagee_in='enterPassword',
                      messageout=[('verifyAccount', 'consortium', 'OK')], return_v='void', poststate='WaitAmount')]),
    Behavior(scenario_name='Bad account', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[],
                      return_v='badBankAccount', poststate='WaitBankVerify')]),
    Behavior(scenario_name='Bad password', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[],
                      return_v='badBankPassword', poststate='WaitBankVerify')]),
    Behavior(scenario_name='GoodAccount', object='bank', behavior=[
        BehaviorBlock(prestate='WaitBankVerify', messagee_in='verifyCardWithBank', messageout=[], return_v='OK',
                      poststate='WaitBankVerify')]),
    Behavior(scenario_name='Bad account', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'badBankAccount')], return_v='badAccount',
                      poststate='WaitVerify')]),
    Behavior(scenario_name='Bad password', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'badBankPassword')], return_v='badPassword',
                      poststate='WaitVerify')]),
    Behavior(scenario_name='GoodAccount', object='consortium', behavior=[
        BehaviorBlock(prestate='WaitVerify', messagee_in='verifyAccount',
                      messageout=[('verifyCardWithBank', 'bank', 'OK')], return_v='OK', poststate='WaitVerify')])
]

io_automata = get_io_from_behavior(behaviors)

for obj, automaton in io_automata.items():
    print(f"Object: {obj}")
    print(f"States: {automaton.states}")
    for transition in automaton.transitions:
        print(
            f"Transition: {transition.from_transition} -> {transition.to_transition}, message_in: {transition.message_in}, message_out: {transition.message_out}, return_v: {transition.return_v}")





#def write_to_uml(io_automaton: dict[str:IOAutomaton]) -> None:
#    res: str = ""
#    destination: str = "result.uml"
#    print("I am writing res to destination")
#    pass