from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union


nivel = 0


def _indent() -> str:
    return " " * nivel


# Programa
@dataclass
class Program:
    items: List[Item]

    def print(self):
        for i, item in enumerate(self.items):
            item.print()
            if i < len(self.items) - 1:
                print()


# Itens de nível superior
class Item(ABC):
    @abstractmethod
    def print(self):
        pass


@dataclass
class ConstDecl(Item):
    name: str
    type_spec: Optional[str]
    value: Expression

    def print(self):
        type_part = f": {self.type_spec}" if self.type_spec else ""
        print(f"{_indent()}const {self.name}{type_part} = ", end="")
        self.value.print()
        print(";", end="")


@dataclass
class VarDecl(Item):
    name: str
    type_spec: Optional[str]
    value: Expression

    def print(self):
        type_part = f": {self.type_spec}" if self.type_spec else ""
        print(f"{_indent()}var {self.name}{type_part} = ", end="")
        self.value.print()
        print(";", end="")


@dataclass
class Function(Item):
    name: str
    params: List[Param]
    return_type: Optional[str]
    body: Block
    visibility: Optional[str]

    def print(self):
        vis = "pub " if self.visibility else ""
        params_txt = ", ".join([p.format() for p in self.params])
        ret = f" {self.return_type}" if self.return_type else ""
        print(f"{_indent()}{vis}fn {self.name}({params_txt}){ret} ", end="")
        self.body.print()


@dataclass
class Param:
    name: str
    type_spec: str

    def format(self) -> str:
        return f"{self.name}: {self.type_spec}"


# Blocos e comandos
@dataclass
class Block:
    statements: List[Statement]

    def print(self):
        global nivel
        print("{")
        nivel += 4
        for i, stmt in enumerate(self.statements):
            print(_indent(), end="")
            stmt.print()
            if i < len(self.statements) - 1:
                print()
        nivel -= 4
        print(f"\n{_indent()}}}", end="")


class Statement(ABC):
    @abstractmethod
    def print(self):
        pass


@dataclass
class ExprStmt(Statement):
    expr: Expression

    def print(self):
        self.expr.print()
        print(";", end="")


@dataclass
class AssignStmt(Statement):
    name: str
    value: Expression

    def print(self):
        print(f"{self.name} = ", end="")
        self.value.print()
        print(";", end="")


@dataclass
class ReturnStmt(Statement):
    value: Optional[Expression]

    def print(self):
        if self.value is None:
            print("return;", end="")
        else:
            print("return ", end="")
            self.value.print()
            print(";", end="")


@dataclass
class IfStmt(Statement):
    condition: Expression
    then_block: Block
    else_block: Optional[Block]

    def print(self):
        print("if (", end="")
        self.condition.print()
        print(") ", end="")
        self.then_block.print()
        if self.else_block:
            print(" else ", end="")
            self.else_block.print()


@dataclass
class WhileStmt(Statement):
    condition: Expression
    body: Block

    def print(self):
        print("while (", end="")
        self.condition.print()
        print(") ", end="")
        self.body.print()


# Expressões
class Expression(ABC):
    @abstractmethod
    def print(self):
        pass


@dataclass
class BinaryExpr(Expression):
    op: str
    left: Expression
    right: Expression

    def print(self):
        print("(", end="")
        self.left.print()
        print(f" {self.op} ", end="")
        self.right.print()
        print(")", end="")


@dataclass
class UnaryExpr(Expression):
    op: str
    expr: Expression

    def print(self):
        print(f"{self.op}", end="")
        self.expr.print()


@dataclass
class Literal(Expression):
    value: Union[int, float, bool, str]

    def print(self):
        if isinstance(self.value, str):
            print(f'"{self.value}"', end="")
        else:
            print(self.value, end="")


@dataclass
class Identifier(Expression):
    name: str

    def print(self):
        print(self.name, end="")
