from dataclasses import dataclass

from .dfa import Dfa
from project.errors import InvalidStateError, InvalidSymbolError, MalformedInputError

@dataclass
class Nfa:
    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], set[str]]

    @classmethod
    def from_dfa(cls, dfa: Dfa) -> "Nfa":
        return cls(
            set(dfa.states),
            set(dfa.alphabet),
            dfa.start_state,
            set(dfa.accept_states),
            { key: {target} for key, target in dfa.transitions.items() }
        )

    def determinize(self) -> Dfa:
        start: frozenset[str] = frozenset([self.start_state])
        correspondence: dict[frozenset[str], str] = {start: 's0'}
        pending: list[frozenset[str]] = [start]
        transitions: dict[tuple[str, str], str] = {}
        accept_states: set[str] = set()

        index: int = 1
        while pending:
            group: frozenset[str] = pending.pop(0)
            name: str = correspondence[group]

            if any(member in self.accept_states for member in group):
                accept_states.add(name)

            for symbol in sorted(self.alphabet):
                target: set[str] = set()
                for member in group:
                    target |= self.transitions.get((member, symbol), set())

                if not target: continue

                frozen: frozenset[str] = frozenset(target)
                if frozen not in correspondence:
                    correspondence[frozen] = f's{index}'
                    index += 1

                    pending.append(frozen)

                transitions[(name, symbol)] = correspondence[frozen]

        return Dfa(
            states = set(correspondence.values()),
            alphabet = self.alphabet,
            start_state = correspondence[start],
            accept_states = accept_states,
            transitions = transitions
        )
    