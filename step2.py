# Omar
# key is object, value is list of scenarios
from collections import defaultdict

from models import *


def table_to_projections(table: list[Scenario]) -> dict[str: list[Scenario]]:
    projections = defaultdict(list)
    for scenario in table:
        involved_objects = {scenario.sender, scenario.receiver}
        for obj in involved_objects:
            if obj == scenario.sender or obj == scenario.receiver:
                projections[obj].append(scenario)

    return dict(projections)


# Omar
def projections_to_behavior(projections: dict[str, list[Scenario]]) -> list[Behavior]:
    behaviors = []
    for obj, scenarios in projections.items():
        behavior = Behavior(scenario_name="bad_account", object=obj, behavior=[])

        # Filter scenarios where the object is the receiver
        behavior_block = None

        for scenario in scenarios:
            if scenario.receiver == obj:
                if behavior_block is not None:
                    behavior.behavior.append(behavior_block)
                behavior_block = BehaviorBlock(
                    prestate=scenario.prestate,
                    messagee_in=scenario.operation,
                    messageout=[],
                    return_v=scenario.return_v,
                    poststate=scenario.post_state
                )
            else:
                if behavior_block is None:
                    behavior_block = BehaviorBlock(
                        prestate=scenario.prestate,
                        messagee_in=scenario.operation,
                        messageout=[],
                        return_v=scenario.return_v,
                        poststate=scenario.post_state
                    )
                behavior_block.messageout.append((scenario.operation, scenario.receiver, scenario.return_v))
        behavior.behavior.append(behavior_block)
        behaviors.append(behavior)
    return behaviors


table = [
    Scenario("WaitCard", "user", "insertCard", "atm", "void", "WaitPassword"),
    Scenario("-", "atm", "requestPassword", "user", "void", "-"),
    Scenario("WaitPassword", "user", "enterPassword", "atm", "void", "WaitTakeCard"),
    Scenario("WaitVerify", "atm", "verifyAccount", "consortium", "badAccount", "WaitVerify"),
    Scenario("WaitBankVerify", "consortium", "verifyCardWithBank", "bank", "badBankAccount", "WaitBankVerify"),
    Scenario("-", "atm", "badAccountMessage", "user", "void", "-"),
    Scenario("-", "atm", "printReceipt", "user", "void", "-"),
    Scenario("-", "atm", "ejectCard", "user", "void", "-"),
    Scenario("-", "atm", "requestTakeCard", "user", "void", "-"),
    Scenario("WaitTakeCard", "user", "takeCard", "atm", "void", "WaitCard"),
    Scenario("-", "atm", "displayMainScreen", "user", "void", "-")
]

projections = table_to_projections(table)
behaviors = projections_to_behavior(projections)

# Print each behavior on a separate line
for behavior in behaviors:
    print(f"Behavior of {behavior.object}:")
    for block in behavior.behavior:
        print(
            f"  Pre-state: {block.prestate}, Message-in: {block.messagee_in}, Messages-out: {block.messageout}, Return: {block.return_v}, Post-state: {block.poststate}")
