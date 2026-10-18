from project.models.dfa import Dfa
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

    def run(self, args):
        f_in: str = args.input
        f_out: str = args.output
        words: list[str] = args.check.split(',')


        dfa: Dfa = Dfa.from_file(f_in)

        results: list[str] = [dfa.test_word(word) for word in words]

        with open(f_out, 'w') as file:
            file.write('\n'.join(results))
