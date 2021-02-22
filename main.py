import argparse


def calculator(eq):

    valid = "1234567890-+ "

    txt = eq.replace(" ", "")

    list_sign = []

    support = ""

    for char in txt:
        if char not in valid:
            print("Argumento Inválido. Há caracteres inválidos no argumento.")
            return
        if char in "+-":
            support += " "
            if char == "+":
                list_sign.append(1)
            else:
                list_sign.append(-1)
        else:
            support += char

    list_num = support.split()

    if len(list_sign) != len(list_num):
        print("Argumento Inválido. Há problemas com os sinais.")
        return

    result = 0

    for num, sign in zip(list_num, list_sign):
        result += sign * int(num)

    print(f"{txt}={result}")
    return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "equation",
        help="Argumento que contém a equação a ser calculada",
    )

    args = parser.parse_args()

    calculator(args.equation)
