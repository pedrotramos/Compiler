import argparse


class Calculator:
    def __init__(self):
        self.txt = None
        self.result = 0
        self.support = ""
        self.valid = "1234567890+- "
        self.list_sign = []
        self.list_num = []
        self.error = False

    def parse(self, arg):
        self.txt = arg.replace(" ", "")
        for i in range(len(self.txt)):
            if self.txt[i] not in self.valid:
                print("Argumento Inválido. Há caracteres inválidos no argumento.")
                self.error = True
                break
            if i == 0:
                if self.txt[i] == "-":
                    self.list_sign.append(-1)
                elif self.txt[i] == "+":
                    self.list_sign.append(1)
                else:
                    self.list_sign.append(1)
                    self.support += self.txt[i]
            else:
                if self.txt[i] in "+-":
                    self.support += " "
                    if self.txt[i] == "+":
                        self.list_sign.append(1)
                    else:
                        self.list_sign.append(-1)
                else:
                    self.support += self.txt[i]

        self.list_num = self.support.split()

        if len(self.list_sign) != len(self.list_num):
            print("Argumento Inválido. Há problemas com os sinais.")
            self.error = True

    def calculate(self):
        if not self.error:
            for num, sign in zip(self.list_num, self.list_sign):
                self.result += sign * int(num)
            print(f"Resultado: {calc.result}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "equation",
        help="Argumento que contém a equação a ser calculada",
    )

    args = parser.parse_args()

    calc = Calculator()
    calc.parse(args.equation)
    calc.calculate()
