from dataclasses import dataclass
from typing import List, Any
from .lexer import Token

@dataclass
class Tree: # Main
    children: List
    def __repr__(self):
        return f"Tree({self.children})"
    def pretty(self, idt=0):
        lines = [f"{'  '*idt}tree"]
        for node in self.children:
            lines.append(node.pretty(idt+1))
        return "\n".join(lines)

@dataclass
class BinaryOp: # For l | r, l - r, l = r, (...)
    left: Any
    op: Token
    right: Any
    def __repr__(self):
        return f"BinaryOp(left={self.left}, op={str(self.op)!r}, right={self.right})"
    def pretty(self, idt=0):
        return "\n".join([f"{idt*'  '}binary_op", self.left.pretty(idt+1), f"{(idt+1)*'  '}{str(self.op)}", self.right.pretty(idt+1)])

@dataclass
class String:
    value: str
    line:int=1
    column:int=1
    def __repr__(self):
        return f"String({self.value!r})"
    
    def pretty(self, idt=0):
        return f"{'  '*idt}{self.value!r}"

@dataclass
class Rule:
    rule: str
    line:int=1
    column:int=1
    def __repr__(self):
        return f"Rule({self.rule})"
    def pretty(self, idt=0):
        return f"{'  '*idt}RULE {self.rule}"
        
@dataclass
class Terminal:
    term: str
    line:int=1
    column:int=1
    def __repr__(self):
        return f"Terminal({self.term})"
    def pretty(self, idt=0):
        return f"{'  '*idt}term {self.term}"

class Star:
    def pretty(self, idt=0):
        return f"{'  '*idt}star"
        
class Default:
    def pretty(self, idt=0):
        return f"{'  '*idt}default"

class Optional:
    def pretty(self, idt=0):
        return f"{'  '*idt}optional"