import sys
import argparse
import re


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    def __init__(self):
        self.origin = ""
        self.position = 0
        self.tokens = []

    def tokenize(self, src):
        self.origin = src
        scanner = re.Scanner(
            [
                (r"[0-9]+", lambda scanner, token: Token("INT", token)),
                (r"\+", lambda scanner, token: Token("PLUS", token)),
                (r"\-", lambda scanner, token: Token("MINUS", token)),
                (r"\s+", None),  # None == skip token.
                (r".*", lambda scanner, token: Token("ERROR", token)),
            ]
        )
        results, remainder = scanner.scan(self.origin)
        self.tokens = results
        self.tokens.append(Token("EOF", ""))
        return self.tokens

    def getNextToken(self):
        tk = self.tokens[self.position]
        self.position += 1
        return tk


class Parser:
    def __init__(self):
        self.tokenizer = Tokenizer()

    def parse(self):
        token = self.tokenizer.getNextToken()
        if token.type == "INT":
            result = int(token.value)
            token = self.tokenizer.getNextToken()
            while token.type != "EOF":
                if token.type == "ERROR":
                    raise ValueError("Há caracteres inválidos na entrada")
                elif token.type == "PLUS":
                    token = self.tokenizer.getNextToken()
                    if token.type == "INT":
                        result += int(token.value)
                    else:
                        raise ValueError(
                            "O sinal de soma deve ser seguido de um número"
                        )
                elif token.type == "MINUS":
                    token = self.tokenizer.getNextToken()
                    if token.type == "INT":
                        result -= int(token.value)
                    else:
                        raise ValueError(
                            "O sinal de subtração deve ser seguido de um número"
                        )
                elif token.type == "INT":
                    raise ValueError(
                        "Há números diferentes que não possuem operador entre eles"
                    )
                token = self.tokenizer.getNextToken()
            return result
        else:
            raise ValueError("O primeiro token deve ser um número")

    def run(self, src):
        self.tokenizer.tokenize(src)
        return self.parse()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = ""
        for i in range(1, len(sys.argv)):
            arg += sys.argv[i]
        result = Parser().run(arg)
        print(f"{result}")
    else:
        raise argparse.ArgumentError("The program needs an argument to compile")
