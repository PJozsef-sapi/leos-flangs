from project.types.dfa import Dfa
from project.problem import Problem

from argparse import ArgumentParser

class DfaProblem(Problem):
    """
    Implements a Deterministic Finite Automaton.
    """

    def initialize_parser(self, parser: ArgumentParser):
        """
        Initializes the parser with the necessary arguments.
        """
        parser.add_argument(
            '--check',
            help='check word(s) against a Deterministic Finite Automaton, separated by commas (e.g. a,b,ab,aabb)',
        )

    def is_chosen_problem(self, args):
        """
        Check if the problem is chosen
        """
        return bool(args.check)

    def _test(self, dfa: Dfa, word: str) -> tuple[str, str]:
        """
        Tests a word against the DFA.
        """

        current_state: str = dfa.start_state

        for letter in word:
            if (current_state, letter) not in dfa.transitions: return word, 'REJECTED'

            current_state = dfa.transitions[(current_state, letter)]

        return (word, 'ACCEPTED') if current_state in dfa.accept_states else (word, 'REJECTED')

    def run(self, args):

        # Determine input and output files
        f_in: str = args.input
        f_out: str = args.output
        words: str = args.check.split(',')

        with open(f_in, 'r') as f1:
            lines = [line.strip() for line in f1 if line.strip() != '']

        states: set[str] = set(lines[0].split(' '))
        alphabet: set[str] = set(lines[1].split(' '))
        start_state: str = lines[2]
        accept_states: set[str] = set(lines[3].split(' '))

        transitions: dict[tuple[str, str], str] = {}
        for line in lines[4:]:
            state1, symbol, state2 = line.split(' ')
            transitions[(state1, symbol)] = state2

        dfa: Dfa = Dfa(states, alphabet, start_state, accept_states, transitions)

        results: list[tuple[str, str]] = [self._test(dfa, word) for word in words]

        with open(f_out, 'w') as f2:
            f2.write('\n'.join([f'{word} {result}' for (word, result) in results]))
