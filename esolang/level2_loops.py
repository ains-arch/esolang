import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop
        | range

    forloop: "for" NAME "in" range block

    range: "range" "(" start ")"
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined
    >>> interpreter.visit(parser.parse("a=0; b=10; for i in range(b) {a = a + i}; a"))
    45
    '''
    def range(self, tree):
        return range(int(self.visit(tree.children[0])))

    def forloop(self, tree):
        varname = tree.children[0].value
        xs = self.visit(tree.children[1])
        self.stack.append({})
        for x in xs:
            self.stack[-1][varname] = x
            result = self.visit(tree.children[2])
        self.stack.pop()
        return result
