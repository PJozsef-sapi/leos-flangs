from project.models import Dfa, Nfa
from project.errors import MalformedInputError, InvalidStateError, InvalidSymbolError

def from_file(path: str) -> Dfa | Nfa:
    """Reads an automaton from a file.

    Args:
        path: Path to the automaton specification file.

    Returns:
        An Nfa or Dfa instance depending on the structure.

    Raises:
        MalformedInputError: If the file format is invalid.
        InvalidStateError: If a transition references an unknown state.
        InvalidSymbolError: If a transition references an unknown symbol.

    File Format:
        q0 q1 q2 ...  (states, space-separated)
        0 1 ...       (alphabet, space-separated)
        q0            (start state)
        q3 ...        (accept states, space-separated)
        q0 0 q1       (transitions: state symbol target)
"""

    states: set[str]
    alphabet: set[str]
    start_state: str
    accept_states: set[str]
    transitions: dict[tuple[str, str], set[str]] = {}

    with open(path, 'r') as file:
        lines = [line.strip() for line in file]

        states = set(lines[0].split())
        alphabet = set(lines[1].split())
        start_state = lines[2]
        accept_states = set(lines[3].split())

        for line_number, line in enumerate(lines[4:], start=5):
            try:
                state, symbol, target = line.split()
            except ValueError:
                raise MalformedInputError(f'File {path} Line {line_number}: Expected "state symbol state", got "{line}".') from None

            if state not in states:
                raise InvalidStateError(f'File {path} Line {line_number}: State {state} not in state list.')
            if symbol not in alphabet:
                raise InvalidSymbolError(f'File {path} Line {line_number}: Symbol {symbol} not in alphabet.')
            if target not in states:
                raise InvalidStateError(f'File {path} Line {line_number}: State {target} not in state list.')

            if (state, symbol) not in transitions: transitions[(state, symbol)] = {target}
            else: transitions[((state, symbol))].add(target)

    is_det: bool = all(len(targets) == 1 for targets in transitions.values())

    if is_det:
        dfa_transitions: dict[tuple[str, str], str] = {
            key: target
            for key, (target,) in transitions.items()
        }
        return Dfa(states, alphabet, start_state, accept_states, dfa_transitions)
    else:
        return Nfa(states, alphabet, start_state, accept_states, transitions)
