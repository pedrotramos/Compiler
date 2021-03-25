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