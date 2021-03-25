class Node:
    def __init__(self, val, child_list):
        self.value = val
        self.children = child_list

    def evaluate(self):
        pass


class BinaryOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) != 2:
            raise ValueError("Uma operação binária deve possuir dois nós filhos")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
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
        else:
            raise ValueError("Operador unário com valor inválido")


class IntegerValue(Node):
    def __init__(self, val):
        super().__init__(val, None)

    def evaluate(self):
        return self.value


class NoOperation(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self):
        return super().evaluate()