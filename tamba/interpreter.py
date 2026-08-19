from .ast import *
from .errors import RuntimeErrorTamba


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Env:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise KeyError(name)

    def set(self, name, value):
        self.values[name] = value

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise KeyError(name)


class FunctionValue:
    def __init__(self, function, closure):
        self.function = function
        self.closure = closure

    def call(self, args, interpreter, call_node):
        if len(args) != len(self.function.params):
            raise RuntimeErrorTamba(
                f'Function {self.function.name} expects {len(self.function.params)} argument(s), got {len(args)}',
                interpreter.source,
                call_node.line,
                call_node.column,
                interpreter.filename,
                hint=f'Pass exactly {len(self.function.params)} argument(s).',
            )
        environment = Env(self.closure)
        for name, value in zip(self.function.params, args):
            environment.set(name, value)
        try:
            interpreter.exec_block(self.function.body, environment)
        except ReturnSignal as signal:
            return signal.value
        return None


class Interpreter:
    def __init__(self, source, filename='<stdin>', output=None):
        self.source = source
        self.filename = filename
        self.output = output if output is not None else print
        self.env = Env()
        self.env.set('toree', self._toree)

    def _toree(self, *args):
        rendered = [
            'dyame' if value is True else
            'notdyame' if value is False else
            str(value)
            for value in args
        ]
        self.output(*rendered)

    def run(self, program):
        for statement in program.statements:
            self.exec(statement)

    def exec_block(self, block, environment):
        old = self.env
        self.env = environment
        try:
            for statement in block.statements:
                self.exec(statement)
        finally:
            self.env = old

    def exec(self, node):
        if isinstance(node, ExprStmt):
            self.eval(node.expr)
        elif isinstance(node, Let):
            self.env.set(node.name, self.eval(node.value))
        elif isinstance(node, Assign):
            self.env.assign(node.name, self.eval(node.value))
        elif isinstance(node, Block):
            self.exec_block(node, Env(self.env))
        elif isinstance(node, If):
            if self.eval(node.condition):
                self.exec_block(node.then, Env(self.env))
            elif node.otherwise:
                self.exec_block(node.otherwise, Env(self.env))
        elif isinstance(node, While):
            while self.eval(node.condition):
                self.exec_block(node.body, Env(self.env))
        elif isinstance(node, Function):
            self.env.set(node.name, FunctionValue(node, self.env))
        elif isinstance(node, Return):
            raise ReturnSignal(None if node.value is None else self.eval(node.value))

    def eval(self, node):
        try:
            if isinstance(node, Literal):
                return node.value

            if isinstance(node, Variable):
                return self.env.get(node.name)

            if isinstance(node, Unary):
                value = self.eval(node.expr)
                if node.op == 'NOT':
                    return not value
                if node.op == '-':
                    return -value
                return +value

            if isinstance(node, Binary):
                left = self.eval(node.left)
                if node.op == 'and':
                    return self.eval(node.right) if left else left
                if node.op == 'or':
                    return left if left else self.eval(node.right)

                right = self.eval(node.right)
                operations = {
                    '+': lambda: left + right,
                    '-': lambda: left - right,
                    '*': lambda: left * right,
                    '/': lambda: left / right,
                    '%': lambda: left % right,
                    '==': lambda: left == right,
                    '!=': lambda: left != right,
                    '<': lambda: left < right,
                    '>': lambda: left > right,
                    '<=': lambda: left <= right,
                    '>=': lambda: left >= right,
                }
                return operations[node.op]()

            if isinstance(node, Assign):
                value = self.eval(node.value)
                self.env.assign(node.name, value)
                return value

            if isinstance(node, Call):
                function = self.eval(node.callee)
                args = [self.eval(argument) for argument in node.args]
                if isinstance(function, FunctionValue):
                    return function.call(args, self, node)
                if not callable(function):
                    raise TypeError(f'{function!r} is not callable')
                return function(*args)

        except KeyError as error:
            raise RuntimeErrorTamba(
                f"Undefined variable '{error.args[0]}'",
                self.source,
                node.line,
                node.column,
                self.filename,
                hint='Check the variable name or define it before use.',
            ) from None
        except ZeroDivisionError:
            raise RuntimeErrorTamba(
                'Division by zero',
                self.source,
                node.line,
                node.column,
                self.filename,
                hint='Make sure the divisor cannot be zero.',
            ) from None
        except TypeError as error:
            raise RuntimeErrorTamba(
                str(error),
                self.source,
                node.line,
                node.column,
                self.filename,
            ) from None
