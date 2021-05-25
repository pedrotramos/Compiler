class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.position = 4

    def getSymbol(self, s):
        if s in self.symbols:
            return self.symbols[s]
        else:
            raise ValueError("Tentando ler uma variável não inicializada")

    def setSymbol(self, s):
        try:
            pos = self.getSymbol(s)
        except:
            pos = self.position
            self.position += 4
        self.symbols[s] = pos
