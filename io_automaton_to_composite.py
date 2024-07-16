from MSE.models import CompositeState


def get_composite_states(automat) -> list[CompositeState]:
    return [CompositeState("verifyAccount", {"bank.verifyCardWithBank": ["badBankAccount \n badBankPassword \n OK"]}, ["","",""] ), CompositeState("cancel", {}, ["user.canceledMessage \n user.ejectCard \n user.requestTakeCard"])]
    