from dataclasses import dataclass

from project.models.dfa import Dfa
from project.models.errors import InvalidStateError, InvalidSymbolError, MalformedInputError

@dataclass
class Nfa:
    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], set[str]]

    @classmethod
    def from_file(cls, filename: str) -> "Nfa":
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file]

            states: set[str] = set(lines[0].split())
            alphabet: set[str] = set(lines[1].split())
            start_state: str = lines[2]
            accept_states: set[str] = set(lines[3].split())

            transitions: dict[tuple[str, str], set[str]] = {}
            for line_number, line in enumerate(lines[4:], start = 5):
                try:
                    state1, symbol, state2 = line.split()
                except ValueError:
                    raise MalformedInputError(f'File {filename}, Line {line_number}: Expected "state symbol state", got "{line}".') from None

                if state1 not in states:
                    raise InvalidStateError(f'File {filename}, Line {line_number}: State {state1} not in state list.')
                if state2 not in states:
                    raise InvalidStateError(f'File {filename}, Line {line_number}: State {state2} not in state list.')
                if symbol not in alphabet:
                    raise InvalidSymbolError(f'File {filename}, Line {line_number}: Symbol {symbol} not in alphabet.')
                
                if (state1, symbol) not in transitions:
                    transitions[(state1, symbol)] = {state2}
                else: transitions[(state1, symbol)].add(state2)

        return cls(states, alphabet, start_state, accept_states, transitions)

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
    