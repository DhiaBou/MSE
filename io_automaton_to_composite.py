from MSE.models import CompositeState


def get_composite_states(automat) -> list[CompositeState]:
    composite_states = []
    
    message_in_map = {}
    for transition in automat.transitions:
        if transition.message_in not in message_in_map:
            message_in_map[transition.message_in] = []
        message_in_map[transition.message_in].append(transition)
    
    for message_in, transitions in message_in_map.items():
        if not transitions:
            continue

        check = {}
        actions = []

        if len(transitions) == 1 or len(transitions[0].message_out) == 0:
            if len(transitions) > 1:
                check[message_in] = [transition.return_v for transition in transitions]
            for transition in transitions:
                message_out = transition.message_out[1:] if len(transitions) > 1 else transition.message_out
                actions.append(" \n ".join([f"{recipient}.{action}" for action, recipient, _ in message_out]))
        else:
            check[f"{transitions[0].message_out[0][1]}.{transitions[0].message_out[0][0]}"] = [transition.message_out[0][2] for transition in transitions]
            for transition in transitions:
                message_out = transition.message_out[1:]
                actions.append(" \n ".join([f"{recipient}.{action}" for action, recipient, _ in message_out]))

        composite_state = CompositeState(name=message_in, check=check, actions=actions)
        composite_states.append(composite_state)

    return composite_states
    