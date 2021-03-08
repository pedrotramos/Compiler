import sys
import argparse


class Token:
    def __init__(self, token_value, token_type):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    def __init__(self):
        self.origin = ""
        self.position = 0
        self.tokens = []

    def tokenize(self, src):
        self.origin = src
        token_value = ""
        last_char = ""
        while self.position <= len(self.origin):
            if self.position == len(self.origin):
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("", "EOF"))
                else:
                    raise ValueError("Last token must be a number")
            elif self.origin[self.position].isdigit():
                token_value += self.origin[self.position]
                last_char = self.origin[self.position]
            elif self.origin[self.position] == "+":
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("+", "PLUS"))
                    last_char = "+"
                else:
                    raise ValueError(
                        "An operator must always have numbers on both of its sides"
                    )
            elif self.origin[self.position] == "-":
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("-", "MINUS"))
                    last_char = "-"
                else:
                    raise ValueError(
                        "An operator must always have numbers on both of its sides"
                    )
            elif self.origin[self.position] == "*":
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("*", "TIMES"))
                    last_char = "-"
                else:
                    raise ValueError(
                        "An operator must always have numbers on both of its sides"
                    )
            elif self.origin[self.position] == "/":
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("/", "DIVIDED"))
                    last_char = "-"
                else:
                    raise ValueError(
                        "An operator must always have numbers on both of its sides"
                    )
            elif self.origin[self.position] == " ":
                pass
            else:
                raise ValueError("Input contains invalid characters")
            self.position += 1
        return self.tokens


class Parser:
    def __init__(self):
        self.result = 0
        self.tokens = None

    def parse(self, objs):
        self.tokens = objs
        sign = 1
        last_token = ""
        for token in self.tokens:
            if token.type == "INT":
                if last_token == "DIVIDED":
                    self.result /= int(token.value)
                    last_token = ""
                else:
                    self.result += sign * int(token.value)
            elif token.type == "PLUS":
                sign = 1
            elif token.type == "MINUS":
                sign = -1
            elif token.type == "TIMES":
                sign = self.result
                self.result = 0
            elif token.type == "DIVIDED":
                last_token = "DIVIDED"
            elif token.type == "EOF":
                break
            else:
                raise ValueError("Token type not allowed")
        return self.result


if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = ""
        for i in range(1, len(sys.argv)):
            arg += sys.argv[i]
        tokens = Tokenizer().tokenize(arg)
        result = Parser().parse(tokens)
        print(f"{result}")
    else:
        raise argparse.ArgumentError("The program needs an argument to compile")
