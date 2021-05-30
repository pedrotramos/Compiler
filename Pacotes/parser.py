from .tokenization import Tokenizer
from .node_structures import (
    Attribuition,
    BlockOperation,
    BinaryOperation,
    FuncCall,
    FuncDec,
    Function,
    IfOperation,
    Parameter,
    ReadOperation,
    Return,
    Root,
    UnaryOperation,
    IntegerValue,
    BoolValue,
    StringValue,
    VarDec,
    Variable,
    PrintOperation,
    ReadOperation,
    WhileOperation,
)
from .symbolTable import SymbolTable


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.symbols = SymbolTable()

    def parseFactor(self, func_name):
        self.tokenizer.nextToken()
        if self.tokenizer.actual.type == "IDENTIFIER":
            ident = self.tokenizer.actual.value
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                call_children = []
                self.tokenizer.nextToken()
                while True:
                    self.tokenizer.prevToken()
                    child = self.parseOrExpression(func_name)
                    call_children.append(child)
                    if self.tokenizer.actual.type == "SEP":
                        self.tokenizer.nextToken()
                    elif self.tokenizer.actual.type == "END_PARENTHESIS":
                        break
                return FuncCall(ident, call_children, self.symbols)
            else:
                self.tokenizer.prevToken()
                return Variable(func_name, ident, self.symbols)
        elif self.tokenizer.actual.type == "READLN":
            self.tokenizer.nextToken()
            self.tokenizer.nextToken()
            read_tree = ReadOperation("READLN", [self.parseOrExpression()])
            if self.tokenizer.actual.type != "EOL":
                raise ("Um readln deve terminar com ;")
            return read_tree
        elif self.tokenizer.actual.type == "INT":
            return IntegerValue(self.tokenizer.actual.value)
        elif self.tokenizer.actual.type == "STRING":
            return StringValue(self.tokenizer.actual.value)
        elif self.tokenizer.actual.type == "BOOL":
            return BoolValue(self.tokenizer.actual.value)
        elif self.tokenizer.actual.type in ["PLUS", "MINUS", "NOT"]:
            return UnaryOperation(
                self.tokenizer.actual.type, [self.parseFactor(func_name)]
            )
        elif self.tokenizer.actual.type == "INIT_PARENTHESIS":
            expression_tree = self.parseOrExpression(func_name)
            if self.tokenizer.actual.type == "END_PARENTHESIS":
                return expression_tree
            else:
                raise ValueError("Não foi possível fechar os parênteses")

    def parseTerm(self, func_name):
        firstChild = self.parseFactor(func_name)
        output = firstChild
        if self.tokenizer.actual.type in ["EOL", "END_BLOCK", "WHILE"]:
            return output
        self.tokenizer.nextToken()
        while self.tokenizer.actual.type in ["TIMES", "DIVIDED", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["TIMES", "DIVIDED"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseFactor(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
            self.tokenizer.nextToken()
        return output

    def parseExpression(self, func_name):
        firstChild = self.parseTerm(func_name)
        output = firstChild
        while self.tokenizer.actual.type in ["PLUS", "MINUS", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["PLUS", "MINUS"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseTerm(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseRelExpression(self, func_name):
        firstChild = self.parseExpression(func_name)
        output = firstChild
        while self.tokenizer.actual.type in ["GT_COMPARE", "LT_COMPARE", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type in ["GT_COMPARE", "LT_COMPARE"]:
                token_type = self.tokenizer.actual.type
                secondChild = self.parseExpression(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseEqExpression(self, func_name):
        firstChild = self.parseRelExpression(func_name)
        output = firstChild
        while self.tokenizer.actual.type in ["EQ_COMPARE", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "EQ_COMPARE":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseRelExpression(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseAndExpression(self, func_name):
        firstChild = self.parseEqExpression(func_name)
        output = firstChild
        while self.tokenizer.actual.type in ["AND", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "AND":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseEqExpression(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseOrExpression(self, func_name):
        firstChild = self.parseAndExpression(func_name)
        output = firstChild
        while self.tokenizer.actual.type in ["OR", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "OR":
                token_type = self.tokenizer.actual.type
                secondChild = self.parseAndExpression(func_name)
                tree = BinaryOperation(token_type, [output, secondChild], self.symbols)
                output = tree
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return output

    def parseCommand(self, func_name):
        if self.tokenizer.actual.type == "INIT_BLOCK":
            output = self.parseBlock(func_name)
            self.tokenizer.nextToken()
        elif self.tokenizer.actual.type == "PRINTLN":
            output = PrintOperation("PRINTLN", [self.parseOrExpression(func_name)])
            if self.tokenizer.actual.type != "EOL":
                raise ("Um println deve terminar com ;")
            else:
                self.tokenizer.nextToken()
        elif self.tokenizer.actual.type == "RETURN":
            output = Return(self.parseOrExpression(func_name), func_name, self.symbols)
            if self.tokenizer.actual.type != "EOL":
                raise ("Um return deve terminar com ;")
            else:
                self.tokenizer.nextToken()
        elif self.tokenizer.actual.type == "TYPE":
            val_type = self.tokenizer.actual.value
            if val_type == "string":
                val = ""
            elif val_type == "int":
                val = 0
            else:
                val = False
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "IDENTIFIER":
                output = Variable(func_name, self.tokenizer.actual.value, self.symbols)
                exists = None
                try:
                    exists = self.symbols.getSymbol(func_name, output.value)
                except:
                    pass
                if exists != None:
                    raise ValueError("Não é possível redeclarar variáveis")
                self.symbols.setSymbol(func_name, output.value, val, val_type)
                self.tokenizer.nextToken()
                if self.tokenizer.actual.type == "EQUALS":
                    secondChild = self.parseOrExpression(func_name)
                    tree = Attribuition(
                        func_name, output.value, secondChild, self.symbols
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
        elif self.tokenizer.actual.type == "IDENTIFIER":
            identifier_name = self.tokenizer.actual.value
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "EQUALS":
                output = Variable(func_name, identifier_name, self.symbols)
                self.tokenizer.nextToken()
                try:
                    self.symbols.getFunctionParams(self.tokenizer.actual.value)
                    secondChild = self.parseCommand(func_name)
                except:
                    self.tokenizer.prevToken()
                    secondChild = self.parseOrExpression(func_name)
                if self.symbols.getSymbol(func_name, output.value)[0] == type("pedro"):
                    val = ""
                elif self.symbols.getSymbol(func_name, output.value)[0] == type(0):
                    val = 0
                else:
                    val = False
                self.symbols.setSymbol(
                    func_name,
                    output.value,
                    val,
                    self.symbols.getSymbol(func_name, output.value)[0],
                )
                tree = Attribuition(func_name, output.value, secondChild, self.symbols)
                output = tree
                if self.tokenizer.actual.type != "EOL":
                    raise ("Uma atribuição deve terminar com ;")
                else:
                    self.tokenizer.nextToken()

            elif self.tokenizer.actual.type == "INIT_PARENTHESIS":
                self.tokenizer.nextToken()
                call_children = []
                while self.tokenizer.actual.type != "END_PARENTHESIS":
                    self.tokenizer.prevToken()
                    child = self.parseOrExpression(func_name)
                    call_children.append(child)
                    if self.tokenizer.actual.type == "SEP":
                        self.tokenizer.nextToken()
                self.tokenizer.nextToken()
                if self.tokenizer.actual.type != "EOL":
                    raise ("Uma atribuição deve terminar com ;")
                output = FuncCall(identifier_name, call_children, self.symbols)
            else:
                raise ("Erro na definição de variável ou na chamada de uma função")
        elif self.tokenizer.actual.type == "WHILE":
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                condition = self.parseOrExpression(func_name)
                if self.tokenizer.actual.type != "END_PARENTHESIS":
                    raise ValueError("Não foi possível fechar os parênteses")
            else:
                raise ValueError(
                    "Um WHILE deve ser seguido de uma expressão entre parênteses"
                )
            self.tokenizer.nextToken()
            command = self.parseCommand(func_name)
            output = WhileOperation("WHILE", [condition, command])
        elif self.tokenizer.actual.type == "IF":
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                condition = self.parseOrExpression(func_name)
                if self.tokenizer.actual.type != "END_PARENTHESIS":
                    raise ValueError("Não foi possível fechar os parênteses")
            else:
                raise ValueError(
                    "Um IF deve ser seguido de uma expressão entre parênteses"
                )
            self.tokenizer.nextToken()
            command_if = self.parseCommand(func_name)
            if self.tokenizer.actual.type == "ELSE":
                self.tokenizer.nextToken()
                command_else = self.parseCommand(func_name)
                output = IfOperation("IF-ELSE", [condition, command_if, command_else])
            else:
                output = IfOperation("IF-ELSE", [condition, command_if])
        return output

    def parseBlock(self, func_name):
        if self.tokenizer.actual.type == "INIT_BLOCK":
            block = BlockOperation(func_name, self.symbols)
            self.tokenizer.nextToken()
        else:
            raise ("Todo bloco deve começar com {")
        while self.tokenizer.actual.type != "END_BLOCK":
            child = self.parseCommand(func_name)
            if child != None:
                block.newChild(child)
        return block

    def parseFuncDef(self):
        output = []
        while self.tokenizer.actual.type == "TYPE":
            func_type = self.tokenizer.actual.value
            if func_type == "string":
                func_type = type("pedro")
            elif func_type == "int":
                func_type = type(0)
            else:
                func_type = type(False)
            self.tokenizer.nextToken()
            if self.tokenizer.actual.type == "IDENTIFIER":
                func_name = self.tokenizer.actual.value
                self.tokenizer.nextToken()
                if self.tokenizer.actual.type == "INIT_PARENTHESIS":
                    self.tokenizer.nextToken()
                    params = {}
                    var_dec_children = [Function(func_name, func_type)]
                    while True:
                        if self.tokenizer.actual.type == "TYPE":
                            param_type = self.tokenizer.actual.value
                            if param_type == "string":
                                param_type = type("pedro")
                            elif param_type == "int":
                                param_type = type(0)
                            else:
                                param_type = type(False)
                            self.tokenizer.nextToken()
                            if self.tokenizer.actual.type == "IDENTIFIER":
                                param_name = self.tokenizer.actual.value
                                params[param_name] = {"type": param_type, "value": None}
                                param = Parameter(func_name, param_name, self.symbols)
                                var_dec_children.append(param)
                                self.tokenizer.nextToken()
                                if self.tokenizer.actual.type == "END_PARENTHESIS":
                                    self.tokenizer.nextToken()
                                    break
                                elif self.tokenizer.actual.type == "SEP":
                                    self.tokenizer.nextToken()
                                else:
                                    raise ValueError("Erro na declaração de função")
                            else:
                                raise ValueError("Erro na declaração de função")
                        elif self.tokenizer.actual.type == "END_PARENTHESIS":
                            self.tokenizer.nextToken()
                            break
                        else:
                            raise ValueError("Erro na declaração de função")
                    var_dec = VarDec(var_dec_children)
                    self.symbols.setFunction(func_name, params, func_type)
                    statements = self.parseCommand(func_name)
                    self.symbols.setFunctionStmts(func_name, statements)
                    output.append(FuncDec(func_name, var_dec, statements, self.symbols))
                else:
                    raise ValueError("Erro na declaração de função")
            else:
                raise ValueError("Erro na declaração de função")

            if self.tokenizer.actual.type == "EOF":
                self.tokenizer.prevToken()
                break
        else:
            raise ValueError("Erro na declaração de função")
        return output

    def run(self, src):
        self.tokenizer.tokenize(src)
        self.tokenizer.nextToken()
        ast = Root("ROOT", self.parseFuncDef())
        self.tokenizer.nextToken()
        # for i in ast.children:
        #     print(i, i.statements.children)
        if self.tokenizer.actual.type != "EOF":
            raise ValueError(f"Erro no programa. Token: {self.tokenizer.actual.type}")
        return ast.evaluate()