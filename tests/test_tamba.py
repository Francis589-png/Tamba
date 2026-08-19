import unittest
from tamba.parser import Parser
from tamba.interpreter import Interpreter
class T(unittest.TestCase):
 def execute(self,s):
  out=[]; Interpreter(s,output=lambda *x:out.append(' '.join(map(str,x)))).run(Parser(s).parse()); return out
 def test_values(self): self.assertEqual(self.execute('let x = 2 + 3 * 4\ntoree(x)\ntoree(dyame)'),['14','True'])
 def test_if(self): self.assertEqual(self.execute('if dyame { toree("yes") } else { toree("no") }'),['yes'])
 def test_function(self): self.assertEqual(self.execute('fn add(a,b){ return a+b }\ntoree(add(2,5))'),['7'])
 def test_loop(self): self.assertEqual(self.execute('let x=0 while x<3 { x=x+1 } toree(x)'),['3'])
 def test_error_location(self):
  from tamba.errors import ParseError
  with self.assertRaises(ParseError) as c: Parser('let x =\n').parse()
  self.assertEqual((c.exception.line,c.exception.column),(2,1))
if __name__=='__main__': unittest.main()
