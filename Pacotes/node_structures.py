from enum import unique


class Node:
    def __init__(self, val, child_list, assembler):
        self.value = val
        self.children = child_list
        self.assembler = assembler

    def evaluate(self):
        pass


class BlockOperation(Node):
    def __init__(self):
        self.value = "BLOCK"
        self.children = []

    def newChild(self, newNode):
        self.children.append(newNode)

    def evaluate(self):
        for node in self.children:
            node.evaluate()


class PrintOperation(Node):
    def __init__(self, val, child_list, assembler):
        if len(child_list) != 1:
            raise ValueError("Uma operação de println deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list, assembler)

    def evaluate(self):
        self.children[0].evaluate()
        self.assembler.pushStack()
        self.assembler.printOp()
        self.assembler.popStack()


class BinaryOperation(Node):
    def __init__(self, val, child_list, assembler, s):
        if len(child_list) != 2:
            raise ValueError("Uma operação binária deve possuir dois nós filhos")
        else:
            self.symbols = s
            super().__init__(val, child_list, assembler)

    def evaluate(self):
        if self.value == "EQUALS":
            try:
                self.symbols.getSymbol(self.children[0])
                self.children[1].evaluate()
            except:
                self.assembler.newVariable()
                self.symbols.setSymbol(self.children[0])
                self.children[1].evaluate()
            self.assembler.setVariable(self.symbols.getSymbol(self.children[0]))
            return
        self.children[0].evaluate()
        self.assembler.pushStack()
        self.children[1].evaluate()
        self.assembler.popStack()
        if self.value == "PLUS":
            self.assembler.addOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "MINUS":
            self.assembler.subOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "TIMES":
            self.assembler.multOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "DIVIDED":
            self.assembler.divOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "EQ_COMPARE":
            self.assembler.eqOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "GT_COMPARE":
            self.assembler.gtOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "LT_COMPARE":
            self.assembler.ltOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "AND":
            self.assembler.andOp()
            self.assembler.finalizeBinOp()
            return
        elif self.value == "OR":
            self.assembler.orOp()
            self.assembler.finalizeBinOp()
            return
        else:
            raise ValueError("Operador binário com valor inválido")


class UnaryOperation(Node):
    def __init__(self, val, child_list, assembler):
        if len(child_list) != 1:
            raise ValueError("Uma operação unária deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list, assembler)

    def evaluate(self):
        if self.value == "PLUS":
            plus = self.children[0].evaluate()
            return (plus[0], plus[1])
        elif self.value == "MINUS":
            minus = self.children[0].evaluate()
            return (minus[0], -minus[1])
        elif self.value == "NOT":
            not_op = self.children[0].evaluate()
            return (not_op[0], not not_op[1])
        else:
            raise ValueError("Operador unário com valor inválido")


class IntegerValue(Node):
    def __init__(self, val, assembler):
        super().__init__(val, None, assembler)

    def evaluate(self):
        return self.assembler.intVal(self.value)


class BoolValue(Node):
    def __init__(self, val, assembler):
        if val == "true":
            boolVal = True
        elif val == "false":
            boolVal = False
        else:
            if type(val) == type(0):
                if val == 0:
                    boolVal = False
                else:
                    boolVal = True
            else:
                raise ValueError(
                    "não é possível atribuir esse tipo de valor a uma variável booleana"
                )
        super().__init__(boolVal, None, assembler)

    def evaluate(self):
        return (type(self.value), self.value)


class WhileOperation(Node):
    def __init__(self, val, child_list, assembler):
        if len(child_list) != 2:
            raise ValueError("Uma operação while deve possuir dois nós filhos")
        else:
            super().__init__(val, child_list, assembler)

    def evaluate(self):
        uniqueID = self.assembler.createLabel("LOOP", self.assembler.uid)
        self.assembler.nextUID()
        self.children[0].evaluate()
        self.assembler.checkExit(uniqueID)
        self.children[1].evaluate()
        self.assembler.closeLoop(uniqueID)


class IfOperation(Node):
    def __init__(self, val, child_list, assembler):
        if len(child_list) not in [2, 3]:
            raise ValueError(
                "Uma operação if-else deve possuir dois ou três nós filhos"
            )
        else:
            super().__init__(val, child_list, assembler)

    def evaluate(self):
        self.children[0].evaluate()
        uniqueID = self.assembler.checkIf(self.assembler.uid)
        self.assembler.nextUID()
        self.children[1].evaluate()
        self.assembler.jumpToEndIfElse(uniqueID)
        self.assembler.elseCommands(uniqueID)
        if len(self.children) == 3:
            self.children[2].evaluate()
            self.assembler.jumpToEndIfElse(uniqueID)
        self.assembler.closeIfElse(uniqueID)


class NoOperation(Node):
    def __init__(self, val):
        super().__init__(None, None)

    def evaluate(self):
        super().evaluate()


class Variable(Node):
    def __init__(self, val, assembler, s):
        self.symbols = s
        super().__init__(val, None, assembler)

    def evaluate(self):
        try:
            self.assembler.getVariable(self.symbols.getSymbol(self.value))
        except:
            self.assembler.newVariable()
            self.symbols.setSymbol(self.value)
        return