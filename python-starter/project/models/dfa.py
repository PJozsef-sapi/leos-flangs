from dataclasses import dataclass

@dataclass
class Dfa:
    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], str]

    @classmethod
    def from_file(cls, filename: str) -> "Dfa":
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip() != '']

            states: set[str] = set(lines[0].split())
            alphabet: set[str] = set(lines[1].split())
            start_state: str = lines[2]
            accept_states: set[str] = set(lines[3].split())

            transitions: dict[tuple[str, str], str] = {}
            for line in lines[4:]:
                state, symbol, target = line.split()
                transitions[(state), symbol] = target

        return cls(states, alphabet, start_state, accept_states, transitions)

    def test_word(self, word: str) -> str:
        current_state: str = self.start_state

        for symbol in word:
            if (current_state, symbol) not in self.transitions: return 'NEM'

            current_state = self.transitions[(current_state, symbol)]

        return 'IGEN' if current_state in self.accept_states else 'NEM'

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
    