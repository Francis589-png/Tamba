from dataclasses import dataclass


@dataclass
class Program:
    statements: list


@dataclass
class Literal:
    value: object
    line: int = 1
    column: int = 1


@dataclass
class Variable:
    name: str
    line: int = 1
    column: int = 1


@dataclass
class ListLiteral:
    items: list
    line: int = 1
    column: int = 1


@dataclass
class MapLiteral:
    entries: list
    line: int = 1
    column: int = 1


@dataclass
class Index:
    collection: object
    index: object
    line: int = 1
    column: int = 1


@dataclass
class Binary:
    left: object
    op: str
    right: object
    line: int = 1
    column: int = 1


@dataclass
class Unary:
    op: str
    expr: object
    line: int = 1
    column: int = 1


@dataclass
class Assign:
    name: str
    value: object
    line: int = 1
    column: int = 1


@dataclass
class IndexAssign:
    collection: object
    index: object
    value: object
    line: int = 1
    column: int = 1


@dataclass
class Let:
    name: str
    value: object
    line: int = 1
    column: int = 1


@dataclass
class Call:
    callee: object
    args: list
    line: int = 1
    column: int = 1


@dataclass
class ExprStmt:
    expr: object
    line: int = 1
    column: int = 1


@dataclass
class Block:
    statements: list
    line: int = 1
    column: int = 1


@dataclass
class If:
    condition: object
    then: Block
    otherwise: object
    line: int = 1
    column: int = 1


@dataclass
class While:
    condition: object
    body: Block
    line: int = 1
    column: int = 1


@dataclass
class Function:
    name: str
    params: list
    body: Block
    line: int = 1
    column: int = 1


@dataclass
class Return:
    value: object
    line: int = 1
    column: int = 1
