from .ast import *
from .errors import RuntimeErrorTamba
class ReturnSignal(Exception):
 def __init__(self,v): self.value=v
class Env:
 def __init__(self,parent=None): self.values={}; self.parent=parent
 def get(self,n):
  if n in self.values:return self.values[n]
  if self.parent:return self.parent.get(n)
  raise KeyError(n)
 def set(self,n,v): self.values[n]=v
 def assign(self,n,v):
  if n in self.values:self.values[n]=v; return
  if self.parent:self.parent.assign(n,v); return
  raise KeyError(n)
class FunctionValue:
 def __init__(self,fn,closure): self.fn,self.closure=fn,closure
 def call(self,args,interp):
  if len(args)!=len(self.fn.params): raise RuntimeErrorTamba(f'Function {self.fn.name} expects {len(self.fn.params)} argument(s), got {len(args)}',interp.source,1,1,interp.filename)
  e=Env(self.closure)
  for n,v in zip(self.fn.params,args): e.set(n,v)
  try: interp.exec_block(self.fn.body,e)
  except ReturnSignal as r:return r.value
  return None
class Interpreter:
 def __init__(self,source,filename='<stdin>',output=None):
  self.source,self.filename=source,filename; self.output=output or print; self.env=Env(); self.env.set('toree',lambda *a:self.output(*a))
 def run(self,program):
  for s in program.statements:self.exec(s)
 def exec_block(self,b,e):
  old=self.env; self.env=e
  try:
   for s in b.statements:self.exec(s)
  finally:self.env=old
 def exec(self,n):
  if isinstance(n,ExprStmt): self.eval(n.expr)
  elif isinstance(n,Let): self.env.set(n.name,self.eval(n.value))
  elif isinstance(n,Assign): self.env.assign(n.name,self.eval(n.value))
  elif isinstance(n,Block): self.exec_block(n,Env(self.env))
  elif isinstance(n,If): self.exec_block(n.then,Env(self.env)) if self.eval(n.condition) else (self.exec_block(n.otherwise,Env(self.env)) if n.otherwise else None)
  elif isinstance(n,While):
   while self.eval(n.condition): self.exec_block(n.body,Env(self.env))
  elif isinstance(n,Function): self.env.set(n.name,FunctionValue(n,self.env))
  elif isinstance(n,Return): raise ReturnSignal(None if n.value is None else self.eval(n.value))
 def eval(self,n):
  try:
   if isinstance(n,Literal):return n.value
   if isinstance(n,Variable):return self.env.get(n.name)
   if isinstance(n,Unary):
    v=self.eval(n.expr); return (not v) if n.op=='NOT' else (-v if n.op=='-' else +v)
   if isinstance(n,Binary):
    a=self.eval(n.left); b=self.eval(n.right)
    return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b,'%':lambda:a%b,'==':lambda:a==b,'!=':lambda:a!=b,'<':lambda:a<b,'>':lambda:a>b,'<=':lambda:a<=b,'>=':lambda:a>=b,'and':lambda:a and b,'or':lambda:a or b}[n.op]()
   if isinstance(n,Assign): v=self.eval(n.value); self.env.assign(n.name,v); return v
   if isinstance(n,Call):
    f=self.eval(n.callee); args=[self.eval(x) for x in n.args]
    if isinstance(f,FunctionValue): return f.call(args,self)
    if not callable(f): raise TypeError(f'{f!r} is not callable')
    return f(*args)
  except KeyError as e: raise RuntimeErrorTamba(f"Undefined variable '{e.args[0]}'",self.source,1,1,self.filename,hint='Check the variable name.')
  except ZeroDivisionError: raise RuntimeErrorTamba('Division by zero',self.source,1,1,self.filename)
  except TypeError as e: raise RuntimeErrorTamba(str(e),self.source,1,1,self.filename)
