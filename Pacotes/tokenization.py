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
                (r"int", lambda scanner, token: Token("TYPE", token)),
                (r"bool", lambda scanner, token: Token("TYPE", token)),
                (r"string", lambda scanner, token: Token("TYPE", token)),
                (r"true", lambda scanner, token: Token("BOOL", token)),
                (r"false", lambda scanner, token: Token("BOOL", token)),
                (r"while", lambda scanner, token: Token("WHILE", token)),
                (r"if", lambda scanner, token: Token("IF", token)),
                (r"else", lambda scanner, token: Token("ELSE", token)),
                (r"readln", lambda scanner, token: Token("READLN", token)),
                (r"println", lambda scanner, token: Token("PRINTLN", token)),
                (
                    r"[a-zA-Z_$][a-zA-Z_$0-9]*",
                    lambda scanner, token: Token("VAR", token),
                ),
                (r"\".*\"", lambda scanner, token: Token("STRING", token)),
                (r"[0-9]+", lambda scanner, token: Token("INT", int(token))),
                (r"\;", lambda scanner, token: Token("EOL", token)),
                (r"\&\&", lambda scanner, token: Token("AND", token)),
                (r"\|\|", lambda scanner, token: Token("OR", token)),
                (r"\!", lambda scanner, token: Token("NOT", token)),
                (r"\=\=", lambda scanner, token: Token("EQ_COMPARE", token)),
                (r"\>", lambda scanner, token: Token("GT_COMPARE", token)),
                (r"\<", lambda scanner, token: Token("LT_COMPARE", token)),
                (r"\=", lambda scanner, token: Token("EQUALS", token)),
                (r"\+", lambda scanner, token: Token("PLUS", token)),
                (r"\-", lambda scanner, token: Token("MINUS", token)),
                (r"\*", lambda scanner, token: Token("TIMES", token)),
                (r"/", lambda scanner, token: Token("DIVIDED", token)),
                (r"\(", lambda scanner, token: Token("INIT_PARENTHESIS", token)),
                (r"\)", lambda scanner, token: Token("END_PARENTHESIS", token)),
                (r"\{", lambda scanner, token: Token("INIT_BLOCK", token)),
                (r"\}", lambda scanner, token: Token("END_BLOCK", token)),
                (r"\s+", None),  # None == skip token.
                (r".*", lambda scanner, token: Token("ERROR", token)),
            ]
        )
        results = scanner.scan(self.origin)[0]
        # for result in results:
        #     print(result.type, result.value)
        results.append(Token("EOF", ""))
        self.tokens = results
        return self.tokens

    def nextToken(self):
        if self.position + 1 <= len(self.tokens):
            self.actual = self.tokens[self.position]
            self.position += 1
