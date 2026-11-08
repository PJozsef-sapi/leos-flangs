from dataclasses import dataclass

@dataclass
class Dfa:
    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], str]

    def completed(self) -> "Dfa":
        if self.is_complete(): return self

        n: int = max(int(state[1:]) for state in self.states)
        trap: str = f'{self.start_state[0]}{n+1}'

        all_states: set[str] = self.states | {trap}
        new_transitions = dict(self.transitions)

        for state in all_states:
            for symbol in self.alphabet:
                if (state, symbol) not in new_transitions:
                    new_transitions[(state, symbol)] = trap

        return Dfa(
            states=all_states,
            alphabet=set(self.alphabet),
            start_state=self.start_state,
            accept_states=set(self.accept_states),
            transitions=new_transitions
        )

    def test_word(self, word: str) -> str:
        current_state: str = self.start_state

        for symbol in word:
            if (current_state, symbol) not in self.transitions: return 'NEM'

            current_state = self.transitions[(current_state, symbol)]

        return 'IGEN' if current_state in self.accept_states else 'NEM'

    def is_complete(self) -> bool:
        return all(
            (state, symbol) in self.transitions
            for state in self.states
            for symbol in self.alphabet
        )

    @staticmethod
    def _state_key(name: str) -> int:
        return int(name[1:])

    @staticmethod
    def _transition_key(item: tuple[tuple[str, str], str]) -> tuple[int, str]:
        (state, symbol), _ = item
        return int(state[1:]), symbol

    def serialize(self) -> str:
        lines: list[str] = []

        states_line: str = ' '.join(sorted(self.states, key=self._state_key))
        alphabet_line: str = ' '.join(sorted(self.alphabet))
        start_line: str = self.start_state
        accept_line: str = ' '.join(sorted(self.accept_states, key=self._state_key))

        transition_lines: list[str] = [
            f'{state} {symbol} {target}'
            for (state, symbol), target in sorted(self.transitions.items(), key=self._transition_key)
        ]

        return '\n'.join([states_line, alphabet_line, start_line, accept_line, *transition_lines])

    def reachable_states(self) -> set[str]:
        reachable: set[str] = {self.start_state}
        pending: list[str] = [self.start_state]

        while pending:
            curr: str = pending.pop(0)

            for symbol in self.alphabet:
                target: str | None = self.transitions.get((curr, symbol))
                if target is not None and target not in reachable:
                    reachable.add(target)
                    pending.append(target)

        return reachable

    def pruned(self) -> "Dfa":
        keep: set[str] = self.reachable_states()

        states: set[str] = keep
        accept_states: set[str] = self.accept_states & keep
        transitions: dict[tuple[str, str], str] = {
            key: target
            for key, target in self.transitions.items()
            if key[0] in keep
        }

        return Dfa(
            states=states,
            alphabet=set(self.alphabet),
            start_state=self.start_state,
            accept_states=accept_states,
            transitions=transitions
        )
    