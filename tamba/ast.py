from dataclasses import dataclass
@dataclass
class Program: statements:list
@dataclass
class Literal: value:object
@dataclass
class Variable: name:str
@dataclass
class Binary: left:object; op:str; right:object
@dataclass
class Unary: op:str; expr:object
@dataclass
class Assign: name:str; value:object
@dataclass
class Let: name:str; value:object
@dataclass
class Call: callee:object; args:list
@dataclass
class ExprStmt: expr:object
@dataclass
class Block: statements:list
@dataclass
class If: condition:object; then:Block; otherwise:object
@dataclass
class While: condition:object; body:Block
@dataclass
class Function: name:str; params:list; body:Block
@dataclass
class Return: value:object
