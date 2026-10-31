from argparse import ArgumentParser
from project.reader import from_file

from project.models import Dfa, Nfa
from project.errors import InvalidInputError
from project.problem import Problem

class DeterminizeProblem(Problem):
    """
    Implements an NFA to DFA conversion.
    """

    def initialize_parser(self, parser: ArgumentParser):
        """
        Initializes the parser with the necessary arguments.
        """

        parser.add_argument(
            '--det',
            help='Determinizes a Non-deterministic Finite Automaton',
            action='store_true'
        )

    def is_chosen_problem(self, args):
        """
        Checks if the problem is chosen.
        """

        return bool(args.det)

    def run(self, args):
        """
        Runs the program.
        """

        f_in: str = args.input
        f_out: str = args.output

        try:
            automaton = from_file(f_in)
            nfa: Nfa = automaton if isinstance(automaton, Nfa) else Nfa.from_dfa(automaton)
            dfa: Dfa = nfa.determinize()

            with open(f_out, 'w') as file:
                file.write(dfa.serialize())
        except OSError:
            print(f'Error opening {f_in}')
        except InvalidInputError as e:
            print(e)