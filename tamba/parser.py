from .lexer import Lexer
from .ast import *
from .errors import ParseError


class Parser:
    def __init__(self, source, filename='<stdin>'):
        self.source = source
        self.filename = filename
        self.t = Lexer(source, filename).tokens()
        self.i = 0

    def parse(self):
        statements = []
        while not self._at('EOF'):
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self._match('LET'):
            return self.let_stmt(self._prev())
        if self._match('IF'):
            return self.if_stmt(self._prev())
        if self._match('WHILE'):
            return self.while_stmt(self._prev())
        if self._match('FN'):
            return self.fn_stmt(self._prev())
        if self._match('RETURN'):
            token = self._prev()
            return Return(None if self._at('}') or self._at('EOF') else self.expr(), token.line, token.column)
        token = self._peek()
        expression = self.expr()
        self._match(';')
        return ExprStmt(expression, token.line, token.column)

    def let_stmt(self, token):
        name = self._consume('IDENT', 'Expected variable name')
        self._consume('=', 'Expected = after variable name')
        return Let(name.value, self.expr(), token.line, token.column)

    def if_stmt(self, token):
        condition = self.expr()
        then = self.block()
        otherwise = self.block() if self._match('ELSE') else None
        return If(condition, then, otherwise, token.line, token.column)

    def while_stmt(self, token):
        return While(self.expr(), self.block(), token.line, token.column)

    def fn_stmt(self, token):
        name = self._consume('IDENT', 'Expected function name')
        self._consume('(', 'Expected (')
        params = []
        if not self._at(')'):
            while True:
                params.append(self._consume('IDENT', 'Expected parameter').value)
                if not self._match(','):
                    break
        self._consume(')', 'Expected )')
        return Function(name.value, params, self.block(), token.line, token.column)

    def block(self):
        opening = self._consume('{', 'Expected {')
        statements = []
        while not self._at('}') and not self._at('EOF'):
            statements.append(self.statement())
        self._consume('}', 'Expected }')
        return Block(statements, opening.line, opening.column)

    def expr(self):
        return self.assign()

    def assign(self):
        expression = self.logic_or()
        if self._match('='):
            operator = self._prev()
            value = self.assign()
            if isinstance(expression, Variable):
                return Assign(expression.name, value, operator.line, operator.column)
            self._err('Invalid assignment target', operator)
        return expression

    def logic_or(self):
        expression = self.logic_and()
        while self._match('OR'):
            operator = self._prev()
            expression = Binary(expression, 'or', self.logic_and(), operator.line, operator.column)
        return expression

    def logic_and(self):
        expression = self.equality()
        while self._match('AND'):
            operator = self._prev()
            expression = Binary(expression, 'and', self.equality(), operator.line, operator.column)
        return expression

    def equality(self):
        expression = self.compare()
        while self._match('==', '!='):
            operator = self._prev()
            expression = Binary(expression, operator.kind, self.compare(), operator.line, operator.column)
        return expression

    def compare(self):
        expression = self.term()
        while self._match('<', '>', '<=', '>='):
            operator = self._prev()
            expression = Binary(expression, operator.kind, self.term(), operator.line, operator.column)
        return expression

    def term(self):
        expression = self.factor()
        while self._match('+', '-'):
            operator = self._prev()
            expression = Binary(expression, operator.kind, self.factor(), operator.line, operator.column)
        return expression

    def factor(self):
        expression = self.unary()
        while self._match('*', '/', '%'):
            operator = self._prev()
            expression = Binary(expression, operator.kind, self.unary(), operator.line, operator.column)
        return expression

    def unary(self):
        if self._match('NOT', '-', '+'):
            operator = self._prev()
            return Unary(operator.kind, self.unary(), operator.line, operator.column)
        return self.call()

    def call(self):
        expression = self.primary()
        while self._match('('):
            opening = self._prev()
            args = []
            if not self._at(')'):
                while True:
                    args.append(self.expr())
                    if not self._match(','):
                        break
            self._consume(')', 'Expected ) after arguments')
            expression = Call(expression, args, opening.line, opening.column)
        return expression

    def primary(self):
        if self._match('NUMBER', 'STRING'):
            token = self._prev()
            return Literal(token.value, token.line, token.column)
        if self._match('BOOL'):
            token = self._prev()
            return Literal(token.value == 'dyame', token.line, token.column)
        if self._match('IDENT'):
            token = self._prev()
            return Variable(token.value, token.line, token.column)
        if self._match('('):
            expression = self.expr()
            self._consume(')', 'Expected )')
            return expression
        self._err('Expected expression', self._peek())

    def _match(self, *kinds):
        if self._peek().kind in kinds:
            self.i += 1
            return True
        return False

    def _consume(self, kind, message):
        if self._match(kind):
            return self._prev()
        self._err(message, self._peek())

    def _peek(self):
        return self.t[self.i]

    def _prev(self):
        return self.t[self.i - 1]

    def _at(self, kind):
        return self._peek().kind == kind

    def _err(self, message, token):
        raise ParseError(message, self.source, token.line, token.column, self.filename)
