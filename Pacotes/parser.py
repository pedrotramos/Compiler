from .tokenization import Tokenizer
from .node_structures import (
    BlockOperation,
    BinaryOperation,
    UnaryOperation,
    IntegerValue,
    Variable,
    PrintOperation,
)
from .symbolTable import SymbolTable


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.symbols = SymbolTable()

    def parseFactor(self):
        self.tokenizer.nextToken()
        if self.tokenizer.actual.type == "VAR":
            return Variable(self.tokenizer.actual.value, self.symbols)
        elif self.tokenizer.actual.type == "PRINTLN":
            print_tree = PrintOperation("PRINTLN", [self.parseExpression()])
            return print_tree
        elif self.tokenizer.actual.type == "INT":
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
        if self.tokenizer.actual.type == "EOL":
            return output
        self.tokenizer.nextToken()
        while self.tokenizer.actual.type in ["TIMES", "DIVIDED", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["TIMES", "DIVIDED"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseFactor()
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
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
        while self.tokenizer.actual.type in ["PLUS", "MINUS", "EQUALS", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["PLUS", "MINUS"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseTerm()
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "EQUALS":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseExpression()
                self.symbols.setSymbol(output.value, 0)
                tree = BinaryOperation(
                    token_type, [output.value, secondChild], self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseCommand(self):
        tree = BlockOperation()
        while self.tokenizer.position < len(self.tokenizer.tokens):
            newBranch = self.parseExpression()
            if self.tokenizer.actual.type != "EOL":
                raise ValueError("Cada comando deve terminar com ;")
            if self.tokenizer.tokens[self.tokenizer.position].type == "EOF":
                tree.newChild(newBranch)
                return tree
            else:
                tree.newChild(newBranch)

    def parse(self):
        tree = self.parseCommand()
        self.tokenizer.nextToken()
        if self.tokenizer.actual.type != "EOF":
            raise ValueError("Erro no programa")
        return tree.evaluate()

    def run(self, src):
        self.tokenizer.tokenize(src)
        teste = self.parse()
        return teste