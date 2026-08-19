import argparse
import unittest

from . import __version__
from .interpreter import Interpreter
from .parser import Parser


def run_file(path):
    with open(path, encoding='utf-8') as handle:
        source = handle.read()
    program = Parser(source, path).parse()
    Interpreter(source, path).run(program)


def run_tests():
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def repl():
    print(f'Tamba {__version__} — JUSU REPL')
    while True:
        try:
            source = input('>>> ')
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not source.strip():
            continue
        try:
            Interpreter(source).run(Parser(source).parse())
        except Exception as error:
            print(error)


def main():
    parser = argparse.ArgumentParser(prog='jusu', description='JUSU CLI for Tamba')
    parser.add_argument('command', choices=['run', 'repl', 'test', 'version'])
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()

    if args.command == 'version':
        print(f'Tamba {__version__}')
    elif args.command == 'repl':
        repl()
    elif args.command == 'test':
        raise SystemExit(run_tests())
    elif not args.file:
        parser.error('run requires a .tmb file')
    else:
        run_file(args.file)


if __name__ == '__main__':
    main()
