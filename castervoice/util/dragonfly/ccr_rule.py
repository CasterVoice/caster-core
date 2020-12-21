from dragonfly import CompoundRule, RuleRef, Repetition, Alternative


class CCRRule(CompoundRule):

    """Docstring for MyClass. """

    spec = "[<sequence>]"

    def _process_recognition(self, node, extras):
        _sequence = extras["sequence"]
        if _sequence is not None:
            for action in _sequence:
                action.execute()

    @staticmethod
    def create(from_rule, max_repetitions=50):
        original_rule = RuleRef(rule=from_rule)
        single_action = Alternative([original_rule])
        sequence = Repetition(single_action, min=1, max=max_repetitions,
                              name="sequence")
        myname = from_rule.name + "_ccr"

        return CCRRule(name=myname, spec=CCRRule.spec, extras=[sequence])
