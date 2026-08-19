import argparse
from . import __version__
from .parser import Parser
from .interpreter import Interpreter

def run_file(path):
 src=open(path,encoding='utf-8').read()
 program=Parser(src,path).parse()
 Interpreter(src,path).run(program)
def repl():
 print(f'Tamba {__version__} — JUSU REPL')
 while True:
  try: s=input('>>> ')
  except (EOFError,KeyboardInterrupt): print(); break
  if not s.strip(): continue
  try: Interpreter(s).run(Parser(s).parse())
  except Exception as e: print(e)
def main():
 ap=argparse.ArgumentParser(prog='jusu',description='JUSU CLI for Tamba')
 ap.add_argument('command',choices=['run','repl','version'])
 ap.add_argument('file',nargs='?')
 a=ap.parse_args()
 if a.command=='version': print(f'Tamba {__version__}')
 elif a.command=='repl': repl()
 elif not a.file: ap.error('run requires a .tmb file')
 else: run_file(a.file)
if __name__=='__main__': main()
