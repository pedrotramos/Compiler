from .tokenization import Tokenizer
from .node_structures import BinaryOperation, UnaryOperation, IntegerValue


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
                tree = BinaryOperation(token_type, [output, secondChild])
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
                tree = BinaryOperation(token_type, [output, secondChild])
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