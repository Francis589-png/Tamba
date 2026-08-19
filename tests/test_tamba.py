import unittest

from tamba.errors import RuntimeErrorTamba
from tamba.interpreter import Interpreter
from tamba.parser import Parser


class TambaTests(unittest.TestCase):
    def execute(self, source):
        output = []
        Interpreter(source, output=lambda *values: output.append(' '.join(map(str, values)))).run(
            Parser(source).parse()
        )
        return output

    def test_arithmetic_and_boolean_literals(self):
        self.assertEqual(
            self.execute('let x = 2 + 3 * 4\ntoree(x)\ntoree(dyame)\ntoree(notdyame)'),
            ['14', 'dyame', 'notdyame'],
        )

    def test_if_else(self):
        self.assertEqual(
            self.execute('if dyame { toree("yes") } else { toree("no") }'),
            ['yes'],
        )

    def test_function(self):
        self.assertEqual(
            self.execute('fn add(a,b){ return a+b }\ntoree(add(2,5))'),
            ['7'],
        )

    def test_loop(self):
        self.assertEqual(
            self.execute('let x=0 while x<3 { x=x+1 } toree(x)'),
            ['3'],
        )

    def test_parser_error_location(self):
        from tamba.errors import ParseError
        with self.assertRaises(ParseError) as context:
            Parser('let x =\n').parse()
        self.assertEqual((context.exception.line, context.exception.column), (2, 1))

    def test_undefined_variable_location(self):
        source = 'let name = "Tamba"\ntoree(nmae)\n'
        with self.assertRaises(RuntimeErrorTamba) as context:
            Interpreter(source, 'main.tmb').run(Parser(source, 'main.tmb').parse())
        error = context.exception
        self.assertEqual((error.line, error.column), (2, 7))
        self.assertIn("Undefined variable 'nmae'", str(error))
        self.assertIn('main.tmb', str(error))
        self.assertIn('Check the variable name', str(error))

    def test_division_by_zero_location(self):
        source = 'let x = 10\nlet y = x / 0\n'
        with self.assertRaises(RuntimeErrorTamba) as context:
            Interpreter(source, 'math.tmb').run(Parser(source, 'math.tmb').parse())
        # Point at the '/' operator that caused the division-by-zero error.
        self.assertEqual((context.exception.line, context.exception.column), (2, 11))
        self.assertIn('Division by zero', str(context.exception))

    def test_short_circuit_and(self):
        self.assertEqual(self.execute('toree(notdyame and missing)'), ['notdyame'])

    def test_short_circuit_or(self):
        self.assertEqual(self.execute('toree(dyame or missing)'), ['dyame'])

    def test_function_argument_error_location(self):
        source = 'fn add(a,b) { return a+b }\ntoree(add(1))\n'
        with self.assertRaises(RuntimeErrorTamba) as context:
            Interpreter(source, 'args.tmb').run(Parser(source, 'args.tmb').parse())
        self.assertEqual((context.exception.line, context.exception.column), (2, 10))

    def test_nested_function_call_stack(self):
        source = (
            'fn inner() {\n'
            '    toree(missing)\n'
            '}\n'
            'fn outer() {\n'
            '    inner()\n'
            '}\n'
            'outer()\n'
        )
        with self.assertRaises(RuntimeErrorTamba) as context:
            Interpreter(source, 'stack.tmb').run(Parser(source, 'stack.tmb').parse())
        error = context.exception
        # Point at the first character of the undefined identifier.
        self.assertEqual((error.line, error.column), (2, 11))
        self.assertIn("Undefined variable 'missing'", str(error))
        self.assertEqual(error.stack, [('outer', 8, 1), ('inner', 5, 5)])
        rendered = str(error)
        self.assertIn('Call stack:', rendered)
        self.assertIn('inner() at line 5, column 5', rendered)
        self.assertIn('outer() at line 8, column 1', rendered)


if __name__ == '__main__':
    unittest.main()
