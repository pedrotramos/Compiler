import argparse


class Token:
    def __init__(self, token_value, token_type):
        self.type = token_type
        self.value = token_value


class Tokenizer:
    def __init__(self, src):
        self.origin = src
        self.position = 0
        self.tokens = []

    def tokenize(self):
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
                    raise ValueError("Operators must have numbers between them")
            elif self.origin[self.position] == "-":
                if last_char.isdigit():
                    self.tokens.append(Token(int(token_value), "INT"))
                    token_value = ""
                    self.tokens.append(Token("-", "MINUS"))
                    last_char = "-"
                else:
                    raise ValueError("Operators must have numbers between them")
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
        for token in self.tokens:
            if token.type == "INT":
                self.result += sign * int(token.value)
            elif token.type == "PLUS":
                sign = 1
            elif token.type == "MINUS":
                sign = -1
            elif token.type == "EOF":
                break
            else:
                raise ValueError("Token type not allowed")
        return self.result


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prefix_chars="-")

    parser.add_argument(
        "-e",
        "--equation",
        type=str,
        help="Argumento que contém a equação a ser calculada",
    )

    args = parser.parse_args()

    tokens = Tokenizer(args.equation).tokenize()
    for token in tokens:
        print(token.value, token.type)
    result = Parser().parse(tokens)

    print(f"{result}")
