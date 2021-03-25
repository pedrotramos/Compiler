import re
import sys
import argparse


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


class PreProcessor:
    def __init__(self):
        self.text = None

    def filter(self, src):
        self.text = re.sub(r"/\*.*?\*/", r"", src)
        return self.text


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    def __init__(self):
        self.origin = ""
        self.position = 0
        self.tokens = []
        self.actual = None

    def tokenize(self, src):
        self.origin = src
        scanner = re.Scanner(
            [
                (r"[0-9]+", lambda scanner, token: Token("INT", int(token))),
                (r"\+", lambda scanner, token: Token("PLUS", token)),
                (r"\-", lambda scanner, token: Token("MINUS", token)),
                (r"\*", lambda scanner, token: Token("TIMES", token)),
                (r"/", lambda scanner, token: Token("DIVIDED", token)),
                (r"\(", lambda scanner, token: Token("INIT_PARENTHESIS", token)),
                (r"\)", lambda scanner, token: Token("END_PARENTHESIS", token)),
                (r"\s+", None),  # None == skip token.
                (r".*", lambda scanner, token: Token("ERROR", token)),
            ]
        )
        results = scanner.scan(self.origin)[0]
        # for result in results:
        #     print(result.type, result.value)
        self.tokens = results
        self.tokens.append(Token("EOF", ""))
        return self.tokens

    def nextToken(self):
        self.actual = self.tokens[self.position]
        self.position += 1


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()

    def parseFactor(self):
        self.tokenizer.nextToken()
        if self.tokenizer.actual.type == "INT":
            return IntegerValue(self.tokenizer.actual.value)
        elif self.tokenizer.actual.type in ["PLUS", "MINUS"]:
            return UnaryOperation(self.tokenizer.actual.type, [self.parseFactor()])
        elif self.tokenizer.actual.type == "INIT_PARENTHESIS":
            expression_tree = self.parseExpression()
            if self.tokenizer.actual.type == "END_PARENTHESIS":
                return expression_tree
            else:
                raise ValueError("Não foi possível fechar os parênteses")

    def parseTerm(self):
        firstChild = self.parseFactor()
        output = firstChild
        self.tokenizer.nextToken()
        while self.tokenizer.actual.type in ["TIMES", "DIVIDED", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["TIMES", "DIVIDED"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseFactor()
                tree = BinaryOperation(token_type, [firstChild, secondChild])
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
            self.tokenizer.nextToken()
        return output

    def parseExpression(self):
        firstChild = self.parseTerm()
        output = firstChild
        while self.tokenizer.actual.type in ["PLUS", "MINUS", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["PLUS", "MINUS"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseTerm()
                tree = BinaryOperation(token_type, [firstChild, secondChild])
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parse(self):
        tree = self.parseExpression()
        if self.tokenizer.actual.type != "EOF":
            raise ValueError("Erro na equação")
        return tree.evaluate()

    def run(self, src):
        self.tokenizer.tokenize(src)
        return self.parse()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".c"):
            with open(sys.argv[1], "r") as f:
                arg = f.readline()
            txt = PreProcessor().filter(src=arg)
            result = Parser().run(txt)
            print(f"{result}")
        else:
            raise argparse.ArgumentError(
                "O argumento do programa deve ser um arquivo C"
            )
    else:
        raise argparse.ArgumentError("O programa precisa de um argumento para rodar")
