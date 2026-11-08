from dataclasses import dataclass
from itertools import combinations
from project.naming import rename

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
        return Dfa(
            states=self.reachable_states(),
            alphabet=set(self.alphabet),
            start_state=self.start_state,
            accept_states=self.accept_states & self.reachable_states(),
            transitions={
                key: target
                for key, target in self.transitions.items()
                if key[0] in self.reachable_states()
            }
        )

    def minimized(self) -> "Dfa":
        pairs: set[frozenset[str]] = {frozenset(pair) for pair in combinations(self.states, 2)}
        marked: set[frozenset[str]] = set()

        for p, q in pairs:
            if (p in self.accept_states) != (q in self.accept_states):
                marked.add(frozenset({p, q}))

        changed: bool = True
        while changed:
            changed = False

            for p, q in pairs - marked:
                for symbol in self.alphabet:
                    targets: frozenset[str] = frozenset({ self.transitions[(p, symbol)], self.transitions[(q, symbol)] })
                    if targets in marked:
                        marked.add(frozenset({p, q}))
                        changed = True
                        break

        unmarked: set[frozenset[str]] = pairs - marked
        rep: dict[str, str] = {}

        for s in self.states:
            group = {s}
            for pair in unmarked:
                if s in pair: group |= pair
            rep[s] = min(group, key=self._state_key)

        return Dfa(
            states={rep[s] for s in self.states},
            alphabet=set(self.alphabet),
            start_state=rep[self.start_state],
            accept_states={rep[s] for s in self.accept_states},
            transitions={
                (rep[source], symbol): rep[target]
                for (source, symbol), target in self.transitions.items()
            }
        )

    def without(self, drop: set[str]) -> "Dfa":
        return Dfa(
            states=self.states - drop,
            alphabet=set(self.alphabet),
            start_state=self.start_state,
            accept_states=self.accept_states - drop,
            transitions = {
                (source, symbol): target
                for (source, symbol), target in self.transitions.items()
                if source not in drop and target not in drop
            }
        )

    def renamed(self) -> "Dfa":
        return Dfa(
            states={rename(s) for s in self.states},
            alphabet=set(self.alphabet),
            start_state=rename(self.start_state),
            accept_states={rename(s) for s in self.accept_states},
            transitions={
                (rename(source), symbol): rename(target)
                for (source, symbol), target in self.transitions.items()
            }
        )
    