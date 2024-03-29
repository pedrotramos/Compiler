import re
import sys
import argparse
from Pacotes.preprocessor import PreProcessor
from Pacotes.parser import Parser


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".c"):
            with open(sys.argv[1], "r") as f:
                arg = f.read()
            txt = PreProcessor().filter(src=arg)
            result = Parser().run(txt)
            with open("base.asm", "r") as f:
                baseCode = f.read()
            repl = "; codigo gerado pelo compilador" + result
            finalCode = re.sub(r"; codigo gerado pelo compilador\n", repl, baseCode)
            print(finalCode)
        else:
            raise argparse.ArgumentError(
                "O argumento do programa deve ser um arquivo C"
            )
    else:
        raise argparse.ArgumentError("O programa precisa de um argumento para rodar")
