from Pacotes.symbolTable import SymbolTable
from copy import deepcopy


class Node:
    def __init__(self, val, child_list):
        self.value = val
        self.children = child_list

    def evaluate(self):
        pass


class BlockOperation(Node):
    def __init__(self, func, s):
        self.func_name = func
        self.symbols = s
        self.value = "BLOCK"
        self.children = []

    def newChild(self, newNode):
        self.children.append(newNode)

    def evaluate(self):
        for node in self.children:
            last = node.evaluate()
            try:
                return self.symbols.getSymbol(self.func_name, "return")
            except:
                continue
        return last


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


class Attribuition:
    def __init__(self, func_name, var_name, expression, s):
        self.func_name = func_name
        self.var_name = var_name
        self.expression = expression
        self.symbols = s

    def evaluate(self):
        self.symbols.setSymbol(
            self.func_name,
            self.var_name,
            self.expression.evaluate()[1],
            self.symbols.getSymbol(self.func_name, self.var_name)[0],
        )


class BinaryOperation(Node):
    def __init__(self, val, child_list, s):
        if len(child_list) != 2:
            raise ValueError("Uma operação binária deve possuir dois nós filhos")
        else:
            self.symbols = s
            super().__init__(val, child_list)

    def evaluate(self):
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
            if type(and_op) == type(0):
                if and_op != 0:
                    and_op = True
                else:
                    and_op = False
            return (type(and_op), and_op)
        elif self.value == "OR":
            if node1[0] == type("pedro") or node2[0] == type("pedro"):
                raise TypeError("Não é possível fazer operação or de strings")
            or_op = node1[1] or node2[1]
            if type(or_op) == type(0):
                if or_op != 0:
                    or_op = True
                else:
                    or_op = False
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
        while self.children[0].evaluate()[1]:
            if self.children[0].evaluate()[0] == type("pedro"):
                raise ValueError("O resultado de uma condição não pode ser uma STRING")
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
        condition = self.children[0].evaluate()
        if condition[0] != type("pedro"):
            if condition[1]:
                return self.children[1].evaluate()
            else:
                if len(self.children) == 3:
                    return self.children[2].evaluate()
        else:
            raise ValueError("O resultado de uma condição não pode ser uma STRING")


class NoOperation(Node):
    def __init__(self, val):
        super().__init__(None, None)

    def evaluate(self):
        super().evaluate()


class Variable(Node):
    def __init__(self, func, val, s):
        self.symbols = s
        self.func_name = func
        super().__init__(val, None)

    def evaluate(self):
        return self.symbols.getSymbol(self.func_name, self.value)


class Parameter(Node):
    def __init__(self, func, val, s):
        self.symbols = s
        self.func_name = func
        super().__init__(val, None)

    def evaluate(self):
        return self.symbols.getFunctionParam(self.func_name, self.value)


class Function:
    def __init__(self, name, func_type):
        self.name = name
        self.type = func_type

    def evaluate(self):
        return (self.type, self.name)


class VarDec:
    def __init__(self, children):
        self.children = children

    def evaluate():
        pass


class FuncDec:
    def __init__(self, name, var_dec, stmts, s):
        self.name = name
        self.var_dec = var_dec
        self.statements = stmts
        self.symbols = s

    def evaluate(self):
        self.statements.evaluate()


class FuncCall:
    def __init__(self, func_name, children, s):
        if len(children) == len(s.getFunctionParams(func_name)):
            self.name = func_name
            self.children = children
            self.symbols = s
        else:
            raise ValueError(f"Argumentos faltantes na chamada da função {func_name}")

    def evaluate(self):
        newSymbols = deepcopy(self.symbols)
        function_params = self.symbols.getFunctionParams(self.name)
        for child, param_name in zip(self.children, function_params.keys()):
            child_type, child_val = child.evaluate()
            newSymbols.setSymbol(self.name, param_name, child_val, child_type)
        statements = newSymbols.getFunctionStmts(self.name)
        call_output = statements.evaluate()
        return call_output


class Return:
    def __init__(self, expression, func, s):
        self.func_name = func
        self.symbols = s
        self.exp = expression

    def evaluate(self):
        self.symbols.setSymbol(
            self.func_name,
            "return",
            self.exp.evaluate()[1],
            self.symbols.getFunctionType(self.func_name),
        )
        return self.exp.evaluate()


class Root(Node):
    def __init__(self, val, child_list):
        super().__init__(val, child_list)

    def evaluate(self):
        for child in self.children:
            if child.name == "main":
                child.evaluate()
