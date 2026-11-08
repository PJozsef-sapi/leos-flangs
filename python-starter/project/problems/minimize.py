from argparse import ArgumentParser
from project.reader import from_file

from project.models import Dfa
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
            '--mini',
            help='Minimizes a given Automaton.',
            action='store_true'
        )

    def is_chosen_problem(self, args):
        """
        Checks if the problem is chosen.
        """

        return bool(args.mini)

    def run(self, args):
        """
        Runs the program.
        """

        f_in: str = args.input
        f_out: str = args.output

        try:
            automaton = from_file(f_in)
            dfa: Dfa = automaton if isinstance(automaton, Dfa) else automaton.determinize()

            pruned: Dfa = dfa.pruned()
            completed: Dfa = pruned.completed()
            trap = completed.states - pruned.states

            minimal: Dfa = completed.minimized()

            drop = trap & minimal.states
            result = minimal.without(drop).renamed()

            with open(f_out, 'w') as file:
                file.write(result.serialize())
        except OSError:
            print(f'Error opening {f_in}')
        except InvalidInputError as e:
            print(e)