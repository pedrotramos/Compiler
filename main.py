import sys
import argparse
import re


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
            return self.tokenizer.actual.value
        elif self.tokenizer.actual.type in ["PLUS", "MINUS"]:
            if self.tokenizer.actual.type == "PLUS":
                return self.parseFactor()
            else:
                return -(self.parseFactor())
        elif self.tokenizer.actual.type == "INIT_PARENTHESIS":
            expression = self.parseExpression()
            if self.tokenizer.actual.type == "END_PARENTHESIS":
                return expression
            else:
                raise ValueError("Não foi possível fechar os parênteses")

    def parseTerm(self):
        value = self.parseFactor()
        result = value
        self.tokenizer.nextToken()
        while self.tokenizer.actual.type in ["TIMES", "DIVIDED", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "TIMES":
                value = self.parseFactor()
                result *= value
            elif self.tokenizer.actual.type == "DIVIDED":
                value = self.parseFactor()
                result /= value
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
            self.tokenizer.nextToken()
        return int(result)

    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.actual.type in ["PLUS", "MINUS", "ERROR"]:
            if self.tokenizer.actual.type == "ERROR":
                raise ValueError("Há caracteres inválidos na entrada")
            elif self.tokenizer.actual.type == "PLUS":
                value = self.parseTerm()
                result += value
            elif self.tokenizer.actual.type == "MINUS":
                value = self.parseTerm()
                result -= value
            elif self.tokenizer.actual.type == "INT":
                raise ValueError(
                    "Há números diferentes que não possuem operador entre eles"
                )
        return int(result)

    def parse(self):
        result = self.parseExpression()
        if self.tokenizer.actual.type != "EOF":
            raise ValueError("Erro na equação")
        return int(result)

    def run(self, src):
        self.tokenizer.tokenize(src)
        return self.parse()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = ""
        for i in range(1, len(sys.argv)):
            arg += sys.argv[i]
        txt = PreProcessor().filter(src=arg)
        result = Parser().run(txt)
        print(f"{result}")
    else:
        raise argparse.ArgumentError("The program needs an argument to compile")
