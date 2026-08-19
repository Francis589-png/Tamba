from .lexer import Lexer
from .ast import *
from .errors import ParseError
class Parser:
 def __init__(self,source,filename='<stdin>'): self.source=source; self.filename=filename; self.t=Lexer(source,filename).tokens(); self.i=0
 def parse(self):
  ss=[]
  while not self._at('EOF'): ss.append(self.statement())
  return Program(ss)
 def statement(self):
  if self._match('LET'): return self.let_stmt()
  if self._match('IF'): return self.if_stmt()
  if self._match('WHILE'): return self.while_stmt()
  if self._match('FN'): return self.fn_stmt()
  if self._match('RETURN'): return Return(None if self._at('}') or self._at('EOF') else self.expr())
  e=self.expr(); self._match(';'); return ExprStmt(e)
 def let_stmt(self):
  n=self._consume('IDENT','Expected variable name'); self._consume('=','Expected = after variable name'); return Let(n.value,self.expr())
 def if_stmt(self):
  c=self.expr(); th=self.block(); other=self.block() if self._match('ELSE') else None; return If(c,th,other)
 def while_stmt(self): return While(self.expr(),self.block())
 def fn_stmt(self):
  n=self._consume('IDENT','Expected function name'); self._consume('(','Expected ('); ps=[]
  if not self._at(')'):
   while True:
    ps.append(self._consume('IDENT','Expected parameter').value)
    if not self._match(','): break
  self._consume(')','Expected )'); return Function(n.value,ps,self.block())
 def block(self):
  self._consume('{','Expected {'); ss=[]
  while not self._at('}') and not self._at('EOF'): ss.append(self.statement())
  self._consume('}','Expected }'); return Block(ss)
 def expr(self): return self.assign()
 def assign(self):
  e=self.logic_or()
  if self._match('='):
   v=self.assign()
   if isinstance(e,Variable): return Assign(e.name,v)
   self._err('Invalid assignment target',self._prev())
  return e
 def logic_or(self):
  e=self.logic_and()
  while self._match('OR'): e=Binary(e,'or',self.logic_and())
  return e
 def logic_and(self):
  e=self.equality()
  while self._match('AND'): e=Binary(e,'and',self.equality())
  return e
 def equality(self):
  e=self.compare()
  while self._match('==','!='): op=self._prev().kind; e=Binary(e,op,self.compare())
  return e
 def compare(self):
  e=self.term()
  while self._match('<','>','<=','>='): op=self._prev().kind; e=Binary(e,op,self.term())
  return e
 def term(self):
  e=self.factor()
  while self._match('+','-'): op=self._prev().kind; e=Binary(e,op,self.factor())
  return e
 def factor(self):
  e=self.unary()
  while self._match('*','/','%'): op=self._prev().kind; e=Binary(e,op,self.unary())
  return e
 def unary(self):
  if self._match('NOT','-','+'): return Unary(self._prev().kind,self.unary())
  return self.call()
 def call(self):
  e=self.primary()
  while self._match('('):
   args=[]
   if not self._at(')'):
    while True:
     args.append(self.expr())
     if not self._match(','): break
   self._consume(')','Expected ) after arguments'); e=Call(e,args)
  return e
 def primary(self):
  if self._match('NUMBER','STRING'): return Literal(self._prev().value)
  if self._match('BOOL'): return Literal(self._prev().value=='dyame')
  if self._match('IDENT'): return Variable(self._prev().value)
  if self._match('('): e=self.expr(); self._consume(')','Expected )'); return e
  self._err('Expected expression',self._peek())
 def _match(self,*ks):
  if self._peek().kind in ks: self.i+=1; return True
  return False
 def _consume(self,k,msg):
  if self._match(k): return self._prev()
  self._err(msg,self._peek())
 def _peek(self): return self.t[self.i]
 def _prev(self): return self.t[self.i-1]
 def _at(self,k): return self._peek().kind==k
 def _err(self,msg,t): raise ParseError(msg,self.source,t.line,t.column,self.filename)
