from .tokenization import Tokenizer
from .node_structures import (
    BlockOperation,
    BinaryOperation,
    IfOperation,
    UnaryOperation,
    IntegerValue,
    BoolValue,
    Variable,
    PrintOperation,
    WhileOperation,
)
from .symbolTable import SymbolTable
from .assembler import Assembler


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.symbols = SymbolTable()
        self.assembler = Assembler()

    def parseFactor(self):
        self.tokenizer.nextToken()
        if self.tokenizer.actual.type == "VAR":
            return Variable(self.tokenizer.actual.value, self.assembler, self.symbols)
        elif self.tokenizer.actual.type == "INT":
            return IntegerValue(self.tokenizer.actual.value, self.assembler)
        elif self.tokenizer.actual.type == "BOOL":
            return BoolValue(self.tokenizer.actual.value, self.assembler)
        elif self.tokenizer.actual.type in ["PLUS", "MINUS", "NOT"]:
            return UnaryOperation(
                self.tokenizer.actual.type, [self.parseFactor()], self.assembler
            )
        elif self.tokenizer.actual.type == "INIT_PARENTHESIS":
            expression_tree = self.parseOrExpression()
            if self.tokenizer.actual.type == "END_PARENTHESIS":
                return expression_tree
            else:
                raise ValueError("Não foi possível fechar os parênteses")

    def parseTerm(self):
        firstChild = self.parseFactor()
        output = firstChild
        if self.tokenizer.actual.type in ["EOL", "END_BLOCK", "WHILE"]:
            return output
        self.tokenizer.nextToken()
        while self.tokenizer.actual.type in ["TIMES", "DIVIDED", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["TIMES", "DIVIDED"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseFactor()
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
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
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseRelExpression(self):
        firstChild = self.parseExpression()
        output = firstChild
        while self.tokenizer.actual.type in ["GT_COMPARE", "LT_COMPARE", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["GT_COMPARE", "LT_COMPARE"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseExpression()
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseEqExpression(self):
        firstChild = self.parseRelExpression()
        output = firstChild
        while self.tokenizer.actual.type in ["EQ_COMPARE", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "EQ_COMPARE":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseRelExpression()
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseAndExpression(self):
        firstChild = self.parseEqExpression()
        output = firstChild
        while self.tokenizer.actual.type in ["AND", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "AND":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseEqExpression()
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseOrExpression(self):
        firstChild = self.parseAndExpression()
        output = firstChild
        while self.tokenizer.actual.type in ["OR", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "OR":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseAndExpression()
                tree = BinaryOperation(
                    token_type, [output, secondChild], self.assembler, self.symbols
                )
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseCommand(self):
        if self.tokenizer.actual.type == "INIT_BLOCK":
            output = self.parse()
            self.tokenizer.nextToken()
        elif self.tokenizer.actual.type == "PRINTLN":
            output = PrintOperation(
                "PRINTLN", [self.parseOrExpression()], self.assembler
            )
            if self.tokenizer.actual.type != "EOL":
                raise ("Um println deve terminar com ;")
            else:
                self.tokenizer.nextToken()
        elif self.tokenizer.actual.type == "TYPE":
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "VAR":
                output = Variable(
                    self.tokenizer.actual.value, self.assembler, self.symbols
                )
                exists = None
                try:
                    exists = self.symbols.getSymbol(output.value)
                except:
                    pass
                if exists != None:
                    raise ValueError("Não é possível redeclarar variáveis")
                self.tokenizer.nextToken()
                if self.tokenizer.actual.type == "EQUALS":
                    token_type = self.tokenizer.actual.type
                    secondChild = self.parseOrExpression()
                    tree = BinaryOperation(
                        token_type,
                        [output.value, secondChild],
                        self.assembler,
                        self.symbols,
                    )
                    output = tree
                    if self.tokenizer.actual.type != "EOL":
                        raise ValueError("Uma atribuição deve terminar com ;")
                    else:
                        self.tokenizer.nextToken()
                elif self.tokenizer.actual.type == "EOL":
                    self.tokenizer.nextToken()
            else:
                raise ValueError("Erro na definição de variável")
        elif self.tokenizer.actual.type == "VAR":
            output = Variable(self.tokenizer.actual.value, self.assembler, self.symbols)
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "EQUALS":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseOrExpression()
                tree = BinaryOperation(
                    token_type,
                    [output.value, secondChild],
                    self.assembler,
                    self.symbols,
                )
                output = tree
                if self.tokenizer.actual.type != "EOL":
                    raise ("Uma atribuição deve terminar com ;")
                else:
                    self.tokenizer.nextToken()
            else:
                raise ("Erro na definição de variável")
        elif self.tokenizer.actual.type == "WHILE":
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                condition = self.parseOrExpression()
                if self.tokenizer.actual.type != "END_PARENTHESIS":
                    raise ValueError("Não foi possível fechar os parênteses")
            else:
                raise ValueError(
                    "Um WHILE deve ser seguido de uma expressão entre parênteses"
                )
            self.tokenizer.nextToken()
            command = self.parseCommand()
            output = WhileOperation("WHILE", [condition, command], self.assembler)
        elif self.tokenizer.actual.type == "IF":
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                condition = self.parseOrExpression()
                if self.tokenizer.actual.type != "END_PARENTHESIS":
                    raise ValueError("Não foi possível fechar os parênteses")
            else:
                raise ValueError(
                    "Um IF deve ser seguido de uma expressão entre parênteses"
                )
            self.tokenizer.nextToken()
            command_if = self.parseCommand()
            if self.tokenizer.actual.type == "ELSE":
                self.tokenizer.nextToken()
                command_else = self.parseCommand()
                output = IfOperation(
                    "IF-ELSE", [condition, command_if, command_else], self.assembler
                )
            else:
                output = IfOperation("IF-ELSE", [condition, command_if], self.assembler)
        return output

    def parse(self):
        if self.tokenizer.actual.type == "INIT_BLOCK":
            block = BlockOperation()
            self.tokenizer.nextToken()
        else:
            raise ("Todo bloco deve começar com {")
        while self.tokenizer.actual.type != "END_BLOCK":
            child = self.parseCommand()
            if child != None:
                block.newChild(child)
        return block

    def run(self, src):
        self.tokenizer.tokenize(src)
        self.tokenizer.nextToken()
        ast = self.parse()
        self.tokenizer.nextToken()
        # for i in ast.children:
        #     print(i)
        if self.tokenizer.actual.type != "EOF":
            raise ValueError(f"Erro no programa. Token: {self.tokenizer.actual.type}")
        ast.evaluate()
        return self.assembler.code