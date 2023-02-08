MAX_CONSTANTS = 10


class Node:
    def __init__(self, val=None, outputIndex=None):
        self._val = val
        self._children = {}
        self.output = outputIndex

        self._str = None
        self.set_string_representation()

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value
        self.set_string_representation()

    def set_string_representation(self):
        self._str = self._val

    def __bool__(self):
        return True

    def __str__(self):
        return self._str

    def __eq__(self, other):
        return str(self) == str(other)


class Prop(Node):
    def __init__(self, val=None, outputIndex=6):
        super().__init__(val, outputIndex)

    def copy(self):
        return Prop(self.val, self.output)


class Unary(Node):
    def __init__(self, val=None, outputIndex=None):
        super().__init__(val, outputIndex)

    @property
    def child(self):
        return self._children.get(0, None)

    @child.setter
    def child(self, value):
        if not isinstance(value, Node):
            raise ValueError("Only nodes can be the children of other nodes")
        self._children[0] = value
        self.set_string_representation()


class Negation(Unary):
    def __init__(self, val=None, outputIndex=7):
        super().__init__(val, outputIndex)

    def set_string_representation(self):
        self._str = f"{str(self.val)}{str(self.child)}"

    def copy(self):
        copied = type(self)(self.val, self.output)
        copied.child = self.child.copy()
        return copied


class Binary(Node):
    def __init__(self, val=None, outputIndex=None):
        super().__init__(val, outputIndex)

    @property
    def lhs(self):
        return self._children.get(0, None)

    @lhs.setter
    def lhs(self, value):
        if not isinstance(value, Node):
            raise ValueError("Only nodes can be the children of other nodes")
        self._children[0] = value
        self.set_string_representation()

    @property
    def rhs(self):
        return self._children.get(1, None)

    @rhs.setter
    def rhs(self, value):
        if not isinstance(value, Node):
            raise ValueError("Only nodes can be the children of other nodes")
        self._children[1] = value
        self.set_string_representation()

    def set_string_representation(self):
        self._str = f"({str(self.lhs)}{str(self.val)}{str(self.rhs)})"

    def copy(self):
        copied = type(self)(self.val, self.output)
        copied.lhs = self.lhs.copy()
        copied.rhs = self.rhs.copy()
        return copied


class Pred(Binary):
    def __init__(self, val=None, outputIndex=1):
        super().__init__(val, outputIndex)

    def set_string_representation(self):
        self._str = f"{str(self.val)}({str(self.lhs)},{str(self.rhs)})"


class Quantifier(Unary):
    def __init__(self, val=None, outputIndex=None):
        self._var = None

        # For gamma expansions. Stores how many times this specific node has been expanded. Helps prevent expanding
        # with used constant over and over again.
        self.used_constants = 0

        super().__init__(val, outputIndex)

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, value):
        self._var = value
        self.set_string_representation()

    def set_string_representation(self):
        self._str = f"{str(self.val)}{str(self.var)}{str(self.child)}"

    def copy(self):
        copied = type(self)(self.val, self.output)
        copied.var = self.var
        copied.child = self.child.copy()
        copied.used_constants = self.used_constants
        return copied


class Exist(Quantifier):
    def __init__(self, val=None, outputIndex=4):
        super().__init__(val, outputIndex)


class Universal(Quantifier):
    def __init__(self, val=None, outputIndex=3):
        super().__init__(val, outputIndex)


QUANTIFIERS = {"E": Exist, "A": Universal}
PRED_VARS = {"x", "y", "z", "w"}
PREDICATES = {"P", "Q", "R", "S"}

PROP_VARS = {"p", "q", "r", "s"}
BINARY_CONNECTIVES = {"^", ">", "v"}
UNARY_CONNECTIVES = {"-"}


# Parse a formula, consult parseOutputs for return values.
def parse(formula):
    is_prop_res = is_prop_formula(formula)
    if is_prop_res:
        return is_prop_res

    is_pred_res = is_pred_formula(formula)
    if is_pred_res:
        return is_pred_res

    return 0


def is_prop_formula(formula):
    res = (
            is_prop(formula)
            or is_negation(formula, is_prop_formula, 7)
            or is_binary(formula, is_prop_formula, 8)
    )
    return res


def is_pred_formula(formula):
    res = (
            is_pred(formula)
            or is_quantifier(formula)
            or is_negation(formula, is_pred_formula, 2)
            or is_binary(formula, is_pred_formula, 5)
    )
    return res


# for each of the following functions, it either returns the node which is truthy, or returns nothing, which is falsy
# all of them are also wrapped in a try block to catch any index errors. This is there to detect if the formula received
# by the function is not long enough.
def is_pred(formula):
    pattern = ["(", PRED_VARS, ",", PRED_VARS, ")"]
    var_indices = [i + 1 for i, ch in enumerate(pattern) if ch == PRED_VARS]

    try:
        if formula[0] in PREDICATES and len(formula) == len(pattern) + 1:
            if all([ch in pattern[i] for i, ch in enumerate(formula[1:])]):
                node = Pred(formula[0])
                node.lhs, node.rhs = Prop(formula[var_indices[0]]), Prop(formula[var_indices[1]])
                return node
    except IndexError:
        return False


def is_quantifier(formula):
    try:
        if formula[0] in QUANTIFIERS and formula[1] in PRED_VARS:
            child = is_pred_formula(formula[2:])
            if child:
                node = QUANTIFIERS[formula[0]](formula[0])
                node.var = formula[1]
                node.child = child
                return node
    except IndexError:
        return False


def is_prop(formula):
    if formula in PROP_VARS:
        return Prop(formula)


def is_negation(formula, prop_or_pred_formula, outputIndex):
    try:
        if formula[0] in UNARY_CONNECTIVES:
            child = prop_or_pred_formula(formula[1:])
            if child:
                node = Negation(formula[0], outputIndex)
                node.child = child
                return node
    except IndexError:
        return False


def is_binary(formula, prop_or_pred_formula, outputIndex):
    try:
        if formula[0] == "(" and formula[-1] == ")":
            con_tuple = con(formula)
            if con_tuple:
                con_index, con_val = con_tuple
                child1, child2 = prop_or_pred_formula(
                    formula[1:con_index]
                ), prop_or_pred_formula(formula[con_index + 1: -1])
                if child1 and child2:
                    node = Binary(con_val, outputIndex)
                    node.lhs, node.rhs = child1, child2
                    return node
    except IndexError:
        return False


# Return the connective symbol of a binary connective formula
def con(formula):
    stack = []
    con_index = ()
    seen = False

    for i, ch in enumerate(formula):
        if ch in ("(", ")"):
            stack.append(ch)
        if stack[-2:] == ["(", ")"]:
            stack = stack[:-2]

        if len(stack) == 1 and ch in BINARY_CONNECTIVES:
            if not seen:
                con_index = (i, ch)
                seen = True
            else:
                con_index = ()

    if len(stack) != 0:
        con_index = ()

    return con_index


# check for satisfiability
def sat(root):
    return 0


#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)
    parsedOutput = 0
    if parsed:
        parsedOutput = parsed.output

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsedOutput])
        if parsedOutput in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (parsed.lhs, parsed.val ,parsed.rhs)
        print(output)

    if SAT:
        if parsed:
            #print('%s is not a formula.' % line)
            #tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(parsed)]))
        else:
            print('%s is not a formula.' % line)
