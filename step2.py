# Omar
# key is object, value is list of scenarios
from collections import defaultdict

from models import *


def get_behaviors(scenarios: list[Scenario]) -> list[Behavior]:
    behaviors = []
    for scenario in scenarios:
        scenario_name = scenario.name
        table = scenario.communications
        projections = table_to_projections(table)
        behaviors.extend(projections_to_behavior(scenario_name, projections))
    return behaviors


def table_to_projections(table: list[Communication]) -> dict[str: list[Communication]]:
    projections = defaultdict(list)
    for scenario in table:
        involved_objects = {scenario.sender, scenario.receiver}
        for obj in involved_objects:
            if (obj == scenario.sender or obj == scenario.receiver) and obj != "user":
                projections[obj].append(scenario)

    return dict(projections)


# Omar
def projections_to_behavior(scenario_name: str, projections: dict[str, list[Communication]]) -> list[Behavior]:
    behaviors = []
    for obj, scenarios in projections.items():
        behavior = Behavior(scenario_name=scenario_name, object=obj, behavior=[])

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

