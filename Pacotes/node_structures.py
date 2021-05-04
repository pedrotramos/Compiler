class Node:
    def __init__(self, val, child_list):
        self.value = val
        self.children = child_list

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
    def __init__(self, val, child_list):
        if len(child_list) != 1:
            raise ValueError("Uma operação de println deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        print(self.children[0].evaluate())


class ReadOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) != 1:
            raise ValueError("Uma operação de readln deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        try:
            return int(input())
        except:
            raise ("O valor inputado deve ser um número inteiro")


class BinaryOperation(Node):
    def __init__(self, val, child_list, s):
        if len(child_list) != 2:
            raise ValueError("Uma operação binária deve possuir dois nós filhos")
        else:
            self.symbols = s
            super().__init__(val, child_list)

    def evaluate(self):
        if self.value == "EQUALS":
            self.symbols.setSymbol(self.children[0], self.children[1].evaluate())
            return
        node1 = self.children[0].evaluate()
        node2 = self.children[1].evaluate()
        if self.value == "PLUS":
            return int(node1 + node2)
        elif self.value == "MINUS":
            return int(node1 - node2)
        elif self.value == "TIMES":
            return int(node1 * node2)
        elif self.value == "DIVIDED":
            return int(node1 / node2)
        elif self.value == "EQ_COMPARE":
            if node1 == node2:
                return 1
            else:
                return 0
        elif self.value == "GT_COMPARE":
            if node1 > node2:
                return 1
            else:
                return 0
        elif self.value == "LT_COMPARE":
            if node1 < node2:
                return 1
            else:
                return 0
        elif self.value == "AND":
            return node1 and node2
        elif self.value == "OR":
            return node1 or node2
        elif self.value == "EQUALS":
            print(node1, node2)
            self.symbols.setSymbol(node1, node2)
            return self.symbols.getSymbol(node1)
        else:
            raise ValueError("Operador binário com valor inválido")


class UnaryOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) != 1:
            raise ValueError("Uma operação unária deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        if self.value == "PLUS":
            return int(self.children[0].evaluate())
        elif self.value == "MINUS":
            return int(-self.children[0].evaluate())
        elif self.value == "NOT":
            return not self.children[0].evaluate()
        else:
            raise ValueError("Operador unário com valor inválido")


class IntegerValue(Node):
    def __init__(self, val):
        super().__init__(val, None)

    def evaluate(self):
        return self.value


class WhileOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) != 2:
            raise ValueError("Uma operação while deve possuir dois nós filhos")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()


class IfOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) not in [2, 3]:
            raise ValueError(
                "Uma operação if-else deve possuir dois ou três nós filhos"
            )
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        condition = condition = self.children[0].evaluate()
        if condition:
            self.children[1].evaluate()
        else:
            if len(self.children) == 3:
                self.children[2].evaluate()


class NoOperation(Node):
    def __init__(self, val):
        super().__init__(None, None)

    def evaluate(self):
        super().evaluate()


class Variable(Node):
    def __init__(self, val, s):
        self.symbols = s
        super().__init__(val, None)

    def evaluate(self):
        return self.symbols.getSymbol(self.value)