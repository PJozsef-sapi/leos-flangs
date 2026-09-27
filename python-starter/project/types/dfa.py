from dataclasses import dataclass

@dataclass
class Dfa:
    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], str]
