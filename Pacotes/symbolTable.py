class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def getSymbol(self, s):
        if s in self.symbols:
            return (self.symbols[s]["type"], self.symbols[s]["value"])
        else:
            raise ValueError("Tentando ler uma variável não inicializada")

    def setSymbol(self, s, val, val_type):
        finalType = None
        if val_type in ["int", type(0)]:
            finalType = type(0)
            try:
                self.symbols[s] = {"value": int(val), "type": finalType}
            except:
                raise TypeError("Erro de tipagem")
        elif val_type in ["bool", type(True)]:
            finalType = type(False)
            try:
                self.symbols[s] = {"value": bool(val), "type": finalType}
            except:
                raise TypeError("Erro de tipagem")
        elif val_type in ["string", type("pedro")]:
            finalType = type("pedro")
            if type(val) == finalType:
                self.symbols[s] = {"value": val, "type": finalType}
            else:
                raise TypeError("Erro de tipagem")
        else:
            raise TypeError("Esse tipo não é suportado")
