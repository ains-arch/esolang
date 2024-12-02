"""
Level 0: Arithmetic Expressions

This module defines the grammar and interpreter for basic arithmetic operations. 
It supports addition, subtraction, multiplication, and division, as well as 
parenthesized expressions. The interpreter evaluates expressions, and the 
transformer simplifies them.
"""

import lark


grammar = r"""
    start: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: exponentiation
        | product "*" exponentiation     -> mul
        | product "/" exponentiation     -> div
        | product "%" exponentiation     -> mod
        | product "(" start ")"          -> mul

    ?exponentiation: atom
        | exponentiation "**" atom       -> exp

    ?atom: NUMBER           -> number
        | "(" start ")"     -> paren

    NUMBER: /-?[0-9]+/

    %import common.WS_INLINE
    %ignore WS_INLINE
"""
parser = lark.Lark(grammar)


class Interpreter(lark.visitors.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("1"))
    1
    >>> interpreter.visit(parser.parse("1+2"))
    3
    >>> interpreter.visit(parser.parse("1-2"))
    -1
    >>> interpreter.visit(parser.parse("(1+2)*3"))
    9
    >>> interpreter.visit(parser.parse("1+2*3"))
    7
    >>> interpreter.visit(parser.parse("1*2+3"))
    5
    >>> interpreter.visit(parser.parse("1*(2+3)"))
    5
    >>> interpreter.visit(parser.parse("(1*2)+3+4*(5-6)"))
    1
    '''
    def start(self, tree):
        res = None
        for child in tree.children:
            res = self.visit(child)
        return res

    def number(self, tree):
        return int(tree.children[0].value)

    def add(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 + v1

    def sub(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 - v1

    def mul(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 * v1

    def div(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 // v1

    def mod(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return v0 % v1

    def exp(self, tree):
        v0 = self.visit(tree.children[0])
        v1 = self.visit(tree.children[1])
        return round(v0 ** v1)

    def paren(self, tree):
        return self.visit(tree.children[0])


class Simplifier(lark.Transformer):
    '''
    >>> simplifier = Simplifier()
    >>> simplifier.transform(parser.parse("1"))
    1
    >>> simplifier.transform(parser.parse("1+2"))
    3
    >>> simplifier.transform(parser.parse("1-2"))
    -1
    >>> simplifier.transform(parser.parse("(1+2)*3"))
    9
    >>> simplifier.transform(parser.parse("1+2*3"))
    7
    >>> simplifier.transform(parser.parse("1*2+3"))
    5
    >>> simplifier.transform(parser.parse("1*(2+3)"))
    5
    >>> simplifier.transform(parser.parse("(1*2)+3+4*(5-6)"))
    1
    '''
    def start(self, xs):
        if len(xs) > 0:
            return xs[-1]
        else:
            None

    def number(self, xs):
        return int(xs[0].value)

    def add(self, xs):
        return xs[0] + xs[1]

    def sub(self, xs):
        return xs[0] - xs[1]

    def mul(self, xs):
        return xs[0] * xs[1]

    def div(self, xs):
        return xs[0] // xs[1]

    def mod(self, children):
        return children[0] % children[1]

    def exp(self, children):
        return round(children[0] ** children[1])

    def paren(self, xs):
        return xs[0]
