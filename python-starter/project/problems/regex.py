from argparse import ArgumentParser
from collections import Counter
from re import compile
from re import Pattern

from project.problem import Problem

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
                case 3:
                    output: str = self._rx3(lines)
                case 4:
                    output: str = self._rx4(lines)
                case 5:
                    output: str = self._rx5(lines)
                case _:
                    pass

        with open(path_out, 'w') as f:
            f.write(output)

    def _rx1(self, lines: list[str]) -> str:
        TIMESTAMP = r'^\S+\s+\S+\s+'
        IDS = r'\d+\s+\d+\s+'
        PREFIX = TIMESTAMP + IDS


        patterns: list[Pattern[str]] = [
            compile(r'^10-15'),                         # date
            compile(r'^10-15\s+10:18:51'),              # datetime
            compile(r'^\S+\s+(?:\d{2}:){2}51\.'),       # 51 seconds (from timestamp)
            compile(PREFIX + r'\w\s+lowmemorykiller:'), # lowmemorykiller tag
            compile(r'^\S+\s+10:18:51\.\d{3}\s+221\b'), # 221 PID at 10:18:51
            compile(PREFIX + r'E\s'),                   # Errors
            compile(PREFIX + r'W\s+PackageManager:'),   # PackageManageer Warnings
            compile(PREFIX + r'D\s+.*ExoPlayer'),       # ExoPlayer Debug
            compile(PREFIX + r'[EW]\s+.*\.java:'),      # .java file Warnings and Errors
            compile(PREFIX + r'[IDVEFAW]\s+.+?:\s.*Thread')
        ]

        counts = [sum(1 for line in lines if p.search(line)) for p in patterns]

        return '\n'.join(str(c) for c in counts)

    def _rx2(self, lines: list[str]) -> str:
        ERROR = compile(r'^\S+\s+\S+\s+\d+\s+\d+\s+E')
        errors: list[str] = [line for line in lines if ERROR.search(line)]

        JAVA_FILES = compile(r'\(([a-zA-Z0-9]+\.java):\d+\)')
        names = [
            name
            for line in errors
            for name in JAVA_FILES.findall(line)
        ]

        return '\n'.join(names)

    def _rx3(self, lines: list[str]) -> str:
        LINE: Pattern[str] = compile(r'(([0-9-]+ [0-9:.]+) +([0-9]+) +([0-9]+) ([IDVEFAW]) (.+?):(?: (.+))?)')

        seen: set[str] = set()
        order: list[str] = []

        for line in lines:
            matching = LINE.search(line)
            if matching is None:
                continue

            pid: str = matching.group(3)
            if pid not in seen:
                seen.add(pid)
                order.append(pid)

        return '\n'.join(order)

    def _rx4(self, lines: list[str]) -> str:
        ERROR = compile(r'^\S+\s+\S+\s+\d+\s+\d+\s+E')
        LINE: Pattern[str] = compile(r'(([0-9-]+ [0-9:.]+) +([0-9]+) +([0-9]+) ([IDVEFAW]) (.+?):(?: (.+))?)')

        errors: list[str] = [line for line in lines if ERROR.search(line)]

        counts: Counter[str] = Counter()
        for err in errors:
            matching = LINE.match(err)
            if matching is None:
                continue

            pid: str = matching.group(3)
            counts[pid] += 1

        most: tuple[str, int] = counts.most_common(1)[0]
        return f'PID={most[0]} ({most[1]} errors)'

    def _rx5(self, lines: list[str]) -> str:
        ERROR = compile(r'^\S+\s+\S+\s+\d+\s+\d+\s+E')
        LINE: Pattern[str] = compile(r'(([0-9-]+ [0-9:.]+) +([0-9]+) +([0-9]+) ([IDVEFAW]) (.+?):(?: (.+))?)')

        errors: list[str] = [line for line in lines if ERROR.search(line)]

        count: int = 0
        for err in errors:
            matching = LINE.match(err)
            if matching is None:
                continue

            pid: str = matching.group(3)
            tid: str = matching.group(4)

            if pid == tid: count += 1

        return str(count)
