class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def getSymbol(self, f, s):
        if s in self.symbols[f]["vars"]:
            return (
                self.symbols[f]["vars"][s]["type"],
                self.symbols[f]["vars"][s]["value"],
            )
        else:
            raise ValueError("Tentando ler uma variável não inicializada")

    def getFunctionType(self, f):
        if f in self.symbols:
            return self.symbols[f]["type"]
        else:
            raise ValueError("Tentando ler uma função não declarada")

    def getFunctionParam(self, f, param):
        if f in self.symbols:
            if param in self.symbols["params"]:
                return (
                    self.symbols[f]["params"][param]["type"],
                    self.symbols[f]["params"][param]["value"],
                )
            else:
                raise ValueError("Tentando ler um parâmetro inexistente")
        else:
            raise ValueError("Tentando ler uma função não declarada")

    def getFunctionParams(self, f):
        if f in self.symbols:
            return self.symbols[f]["params"]
        else:
            raise ValueError("Tentando ler uma função não declarada")

    def getFunctionStmts(self, f):
        if f in self.symbols:
            return self.symbols[f]["stmts"]
        else:
            raise ValueError("Tentando ler uma função não declarada")

    def setSymbol(self, function, name, value, val_type):
        finalType = None
        if val_type in ["int", type(0)]:
            finalType = type(0)
            try:
                self.symbols[function]["vars"][name] = {
                    "value": int(value),
                    "type": finalType,
                }
            except:
                print(function, name, value, val_type)
                raise TypeError("Erro de tipagem")
        elif val_type in ["bool", type(True)]:
            finalType = type(False)
            try:
                self.symbols[function]["vars"][name] = {
                    "value": bool(value),
                    "type": finalType,
                }
            except:
                raise TypeError("Erro de tipagem")
        elif val_type in ["string", type("pedro")]:
            finalType = type("pedro")
            if type(value) == finalType:
                self.symbols[function]["vars"][name] = {
                    "value": value,
                    "type": finalType,
                }
            else:
                raise TypeError("Erro de tipagem")
        else:
            raise TypeError("Esse tipo não é suportado")

    def setFunction(self, name, parameters, func_type):
        self.symbols[name] = {
            "params": parameters,
            "vars": {},
            "type": func_type,
        }

    def setFunctionStmts(self, name, statements):
        self.symbols[name]["stmts"] = statements
