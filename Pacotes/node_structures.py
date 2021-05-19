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
        if self.children[0].evaluate()[0] == type("pedro"):
            print(self.children[0].evaluate()[-1][1:-1])
        else:
            print(self.children[0].evaluate()[-1])


class ReadOperation(Node):
    def __init__(self, val, child_list):
        if len(child_list) != 1:
            raise ValueError("Uma operação de readln deve ter apenas um nó filho")
        else:
            super().__init__(val, child_list)

    def evaluate(self):
        try:
            val = int(input())
            return (type(val), val)
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
            self.symbols.setSymbol(
                self.children[0],
                self.children[1].evaluate()[1],
                self.symbols.getSymbol(self.children[0])[0],
            )
            return
        node1 = self.children[0].evaluate()
        node2 = self.children[1].evaluate()
        if type(node1[0]) == type("pedro") or type(node2[0]) == type("pedro"):
            raise ValueError(
                "Operações binárias só podem ser feitas entre 'int' e 'bool'"
            )
        if self.value == "PLUS":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer soma de strings")
            soma = node1[1] + node2[1]
            return (type(soma), soma)
        elif self.value == "MINUS":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer subtração de strings")
            subtracao = node1[1] - node2[1]
            return (type(subtracao), subtracao)
        elif self.value == "TIMES":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer multiplicação de strings")
            multiplicacao = int(node1[1] * node2[1])
            return (type(multiplicacao), multiplicacao)
        elif self.value == "DIVIDED":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer divisão de strings")
            divisao = int(node1[1] / node2[1])
            return (type(divisao), divisao)
        elif self.value == "EQ_COMPARE":
            eq_comp = node1[1] == node2[1]
            if eq_comp:
                return (type(eq_comp), 1)
            else:
                return (type(eq_comp), 0)
        elif self.value == "GT_COMPARE":
            gt_comp = node1[1] > node2[1]
            if gt_comp:
                return (type(gt_comp), 1)
            else:
                return (type(gt_comp), 0)
        elif self.value == "LT_COMPARE":
            lt_comp = node1[1] < node2[1]
            if lt_comp:
                return (type(lt_comp), 1)
            else:
                return (type(lt_comp), 0)
        elif self.value == "AND":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer operação and de strings")
            and_op = node1[1] and node2[1]
            return (type(and_op), and_op)
        elif self.value == "OR":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer operação or de strings")
            or_op = node1[1] or node2[1]
            return (type(or_op), or_op)
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
            plus = int(self.children[0].evaluate())
            return (plus[0], plus[1])
        elif self.value == "MINUS":
            minus = int(-self.children[0].evaluate())
            return (minus[0], minus[1])
        elif self.value == "NOT":
            not_op = not self.children[0].evaluate()
            return (not_op[0], not_op[1])
        else:
            raise ValueError("Operador unário com valor inválido")


class IntegerValue(Node):
    def __init__(self, val):
        super().__init__(val, None)

    def evaluate(self):
        return (type(self.value), self.value)


class StringValue(Node):
    def __init__(self, val):
        super().__init__(val, None)

    def evaluate(self):
        return (type(self.value), self.value)


class BoolValue(Node):
    def __init__(self, val):
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
        super().__init__(boolVal, None)

    def evaluate(self):
        return (type(self.value), self.value)


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