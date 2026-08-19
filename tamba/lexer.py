from dataclasses import dataclass
from .errors import LexerError
@dataclass(frozen=True)
class Token:
    kind:str; value:object; line:int; column:int
KEYWORDS={'let':'LET','if':'IF','else':'ELSE','while':'WHILE','fn':'FN','return':'RETURN','dyame':'BOOL','notdyame':'BOOL','and':'AND','or':'OR','not':'NOT'}
class Lexer:
 def __init__(self,source,filename='<stdin>'): self.s,self.f=source,filename; self.i=0; self.line=1; self.col=1
 def tokens(self):
  out=[]
  while self.i<len(self.s):
   c=self.s[self.i]
   if c in ' \t\r': self._adv(); continue
   if c=='\n': self._adv(newline=True); continue
   if c=='#':
    while self.i<len(self.s) and self.s[self.i]!='\n': self._adv()
    continue
   line,col=self.line,self.col
   if c.isalpha() or c=='_':
    st=self.i
    while self.i<len(self.s) and (self.s[self.i].isalnum() or self.s[self.i]=='_'): self._adv()
    v=self.s[st:self.i]; out.append(Token(KEYWORDS.get(v,'IDENT'),v,line,col)); continue
   if c.isdigit():
    st=self.i; dot=False
    while self.i<len(self.s) and (self.s[self.i].isdigit() or (self.s[self.i]=='.' and not dot)):
     if self.s[self.i]=='.': dot=True
     self._adv()
    v=self.s[st:self.i]; out.append(Token('NUMBER',float(v) if dot else int(v),line,col)); continue
   if c=='"':
    self._adv(); chars=[]
    while self.i<len(self.s) and self.s[self.i]!='"':
     if self.s[self.i]=='\\':
      self._adv()
      if self.i>=len(self.s): break
      esc=self.s[self.i]; chars.append({'n':'\n','t':'\t','"':'"','\\':'\\'}.get(esc,esc)); self._adv()
     else: chars.append(self.s[self.i]); self._adv()
    if self.i>=len(self.s): raise LexerError('Unterminated string',self.s,line,col,self.f)
    self._adv(); out.append(Token('STRING',''.join(chars),line,col)); continue
   two=self.s[self.i:self.i+2]
   if two in ('==','!=','<=','>='):
    self._adv(); self._adv(); out.append(Token(two,two,line,col)); continue
   if c in '+-*/%=<>(){},[]:;': self._adv(); out.append(Token(c,c,line,col)); continue
   raise LexerError(f"Unexpected character {c!r}",self.s,line,col,self.f)
  out.append(Token('EOF','',self.line,self.col)); return out
 def _adv(self,newline=False):
  self.i+=1
  if newline: self.line+=1; self.col=1
  else: self.col+=1
