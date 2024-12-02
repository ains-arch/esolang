'''

The following tests show example strings in the language.
There are no meaningful commands at this point,
only a block structure.

>>> tree = parser.parse("")
>>> tree = parser.parse(";")
>>> tree = parser.parse(";;;;")
>>> tree = parser.parse("{{}}")
>>> tree = parser.parse(";{};{;;}")
>>> tree = parser.parse(";{{}{{}}};{;{}{;};}")

The following tests check that unbalanced blocks correctly raise exceptions.

>>> tree = parser.parse("{") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{{}{}{{{}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

>>> tree = parser.parse("{;;;}}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedCharacters:
    
The following checks test that comments work.

>>> tree = parser.parse(";{};#")
>>> tree = parser.parse(";{};#{")
>>> tree = parser.parse(";{#}") # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
lark.exceptions.UnexpectedEOF:

'''

import lark
import esolang.level0_arithmetic


grammar = esolang.level0_arithmetic.grammar + r"""
    %extend start: start (";" start)*
        | /#.*/                -> comment
        | assign_var
        | block
        | COMPARISON_OPERATOR
        | comparison
        | condition
        | if_statement
        |

    # semantics
    # the first start will be run if condition is true
    # the second start if condition is false
    # sometimes called "the ternary operator"
    # C derived languages use this notation
    # python doesn't do this, exactly - it's related to inline if

    # we will not implement a boolean variable type
    # conditionals represented by numbers
    # where 0 is True
    # and all non-zero is False
    # semantics of the C language / Unix terminal

    assign_var: NAME "=" start

    block: "{" start* "}"

    COMPARISON_OPERATOR: ">" | "<" | ">=" | "<=" | "==" | "!="
    
    comparison: start COMPARISON_OPERATOR start

    ?condition: start

    if_statement: condition "?" start ":" start

    NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

    %extend atom: NAME -> access_var
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level0_arithmetic.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("a = 2"))
    2
    >>> interpreter.visit(parser.parse("a + 2"))
    4
    >>> interpreter.visit(parser.parse("a = a + 3"))
    5
    >>> interpreter.visit(parser.parse("b = 3"))
    3
    >>> interpreter.visit(parser.parse("a * b"))
    15
    >>> interpreter.visit(parser.parse("a = 3; {a+5}"))
    8
    >>> interpreter.visit(parser.parse("a = 3; {a=5; a+5}"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {a=5}; a+5"))
    10
    >>> interpreter.visit(parser.parse("a = 3; {c=5}; c+5")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable c undefined
    >>> interpreter.visit(parser.parse("0 ? 2 : 3"))
    2
    >>> interpreter.visit(parser.parse("1 ? 2 : 3"))
    3
    >>> interpreter.visit(parser.parse("1-1 ? 2 : 3"))
    2
    >>> interpreter.visit(parser.parse("1-2 ? 2 : 3"))
    3
    >>> interpreter.visit(parser.parse("1-1 ? {a=2; a+3} : 3"))
    5
    >>> interpreter.visit(parser.parse("a = 0; a ? 2 : 3"))
    2
    >>> interpreter.visit(parser.parse("a = 10; a ? 2 : 3"))
    3
    >>> interpreter.visit(parser.parse("a=2; b=2; a-b ? 2 : 3"))
    2
    >>> interpreter.visit(parser.parse("a=2; b=1; a-b ? 2 : 3"))
    3
    >>> interpreter.visit(parser.parse("1 > 0"))
    0
    >>> interpreter.visit(parser.parse("0 > 1"))
    1
    >>> interpreter.visit(parser.parse("1 < 0"))
    1
    >>> interpreter.visit(parser.parse("0 < 1"))
    0
    >>> interpreter.visit(parser.parse("1 == 1"))
    0
    >>> interpreter.visit(parser.parse("1 == 0"))
    1
    >>> interpreter.visit(parser.parse("1 != 0"))
    0
    >>> interpreter.visit(parser.parse("1 != 1"))
    1
    >>> interpreter.visit(parser.parse("1 >= 0"))
    0
    >>> interpreter.visit(parser.parse("0 >= 1"))
    1
    >>> interpreter.visit(parser.parse("1 >= 1"))
    0
    >>> interpreter.visit(parser.parse("0 <= 1"))
    0
    >>> interpreter.visit(parser.parse("1 <= 0"))
    1
    >>> interpreter.visit(parser.parse("1 <= 1"))
    0
    >>> interpreter.visit(parser.parse("a = 0; { a == 0 } ? 2 : 3"))
    2
    >>> interpreter.visit(parser.parse("a = 0; { a == 1 } ? 2 : 3"))
    3
    '''
    def __init__(self):
        self.stack = [{}]

    def _get_from_stack(self, name):
        for d in reversed(self.stack):
            if name in d:
                return d[name]
        raise ValueError(f"Variable {name} undefined")

    def _assign_to_stack(self, name, value):
        for d in reversed(self.stack):
            if name in d:
                d[name] = value
                return value
        self.stack[-1][name] = value
        return value

    def assign_var(self, tree):
        name = tree.children[0].value
        value = self.visit(tree.children[1])
        self._assign_to_stack(name, value)
        return value

    def access_var(self, tree):
        name = tree.children[0].value
        return self._get_from_stack(name)

    def block(self, tree):
        self.stack.append({})
        res = self.visit(tree.children[0])
        self.stack.pop()
        return res

    def if_statement(self, tree):
        condition = self.visit(tree.children[0])
        if condition == 0:
            branch_true = self.visit(tree.children[1])
            return branch_true
        else:
            branch_false = self.visit(tree.children[2])
            return branch_false

    def comparison(self, tree):
        v1 = self.visit(tree.children[0])
        op = tree.children[1].value
        v2 = self.visit(tree.children[2])
        if eval(str(v1) + op + str(v2)):
            return 0
        else:
            return 1
        pass

# tree = parser.parse("1 ? 2 : 3")
# interpreter = Interpreter()
