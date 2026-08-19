class TambaError(Exception):
    def __init__(self, message, source, line, column, filename='<stdin>', hint=None, stack=None):
        self.message = message
        self.source = source
        self.line = line
        self.column = column
        self.filename = filename
        self.hint = hint
        self.stack = list(stack or [])
        super().__init__(message)

    def __str__(self):
        lines = self.source.splitlines()
        text = lines[self.line - 1] if 0 < self.line <= len(lines) else ''
        out = (
            f'TambaError: {self.message}\n\n'
            f'  File "{self.filename}", line {self.line}, column {self.column}\n\n'
            f'    {text}\n'
            f'    ' + ' ' * max(self.column - 1, 0) + '^'
        )
        if self.stack:
            out += '\n\nCall stack:\n' + '\n'.join(
                f'  {name}() at line {line}, column {column}'
                for name, line, column in reversed(self.stack)
            )
        if self.hint:
            out += f'\n\nHint: {self.hint}'
        return out


class LexerError(TambaError):
    pass


class ParseError(TambaError):
    pass


class RuntimeErrorTamba(TambaError):
    pass
