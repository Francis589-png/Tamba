class TambaError(Exception):
    def __init__(self, message, source, line, column, filename='<stdin>', hint=None):
        self.message,self.source,self.line,self.column,self.filename,self.hint=message,source,line,column,filename,hint
        super().__init__(message)
    def __str__(self):
        lines=self.source.splitlines()
        text=lines[self.line-1] if 0 < self.line <= len(lines) else ''
        out=f'TambaError: {self.message}\n\n  File "{self.filename}", line {self.line}, column {self.column}\n\n    {text}\n    ' + ' '*(max(self.column-1,0)) + '^'
        if self.hint: out += f'\n\nHint: {self.hint}'
        return out
class LexerError(TambaError): pass
class ParseError(TambaError): pass
class RuntimeErrorTamba(TambaError): pass
