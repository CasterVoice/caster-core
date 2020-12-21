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
    def create(*from_rules, max_repetitions=50):
        name = "CCR"
        rules = []
        for rule in from_rules:
            rules.append(RuleRef(rule=rule))
            name += "_" + rule.name
        single_action = Alternative(rules)
        sequence = Repetition(single_action, min=1, max=max_repetitions,
                              name="sequence")

        return CCRRule(name=name, spec=CCRRule.spec, extras=[sequence])
