class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def getSymbol(self, s):
        if s in self.symbols:
            return self.symbols[s]
        else:
            raise ValueError("Tentando ler uma variável não inicializada")

    def setSymbol(self, s, val):
        self.symbols[s] = val