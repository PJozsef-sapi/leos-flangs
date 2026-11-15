from argparse import ArgumentParser
from project.problem import Problem
import re

class RegexProblem(Problem):

    def initialize_parser(self, parser: ArgumentParser):
        parser.add_argument(
            '--rgx',
            help="No help provided.",
            type=int
        )

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        path_in: str = args.input
        path_out: str = args.output

        with open(path_in, 'r') as f:
            lines: list[str] = f.readlines()

            match args.rgx:
                case 1:
                    output: str = self._rx1(lines)
                case 2:
                    output: str = self._rx2(lines)
                case _:
                    pass

        with open(path_out, 'w') as f:
            f.write(output)

    def _rx1(self, lines: list[str]) -> str:
        TIMESTAMP = r'^\S+\s+\S+\s+'
        IDS = r'\d+\s+\d+\s+'
        PREFIX = TIMESTAMP + IDS


        patterns = [
            re.compile(r'^10-15'),                         # date
            re.compile(r'^10-15\s+10:18:51'),              # datetime
            re.compile(r'^\S+\s+(?:\d{2}:){2}51\.'),       # 51 seconds (from timestamp)
            re.compile(PREFIX + r'\w\s+lowmemorykiller:'), # lowmemorykiller tag
            re.compile(r'^\S+\s+10:18:51\.\d{3}\s+221\b'), # 221 PID at 10:18:51
            re.compile(PREFIX + r'E\s'),                   # Errors
            re.compile(PREFIX + r'W\s+PackageManager:'),   # PackageManageer Warnings
            re.compile(PREFIX + r'D\s+.*ExoPlayer'),       # ExoPlayer Debug
            re.compile(PREFIX + r'[EW]\s+.*\.java:'),      # .java file Warnings and Errors
            re.compile(PREFIX + r'[IDVEFAW]\s+.+?:\s.*Thread')
        ]

        counts = [sum(1 for line in lines if p.search(line)) for p in patterns]

        return '\n'.join(str(c) for c in counts)

    def _rx2(self, lines: list[str]) -> str:
        ERROR = re.compile(r'^\S+\s+\S+\s+\d+\s+\d+\s+E')
        errors: list[str] = [line for line in lines if ERROR.search(line)]

        JAVA_FILES = re.compile(r'\(([a-zA-Z0-9]+\.java):\d+\)')
        names = [
            name
            for line in errors
            for name in JAVA_FILES.findall(line)
        ]

        return '\n'.join(names)