import os


class Assembler:
    def __init__(self):
        with open("base.asm", "r") as f:
            self.code = f.read()
        self.uid = 0

    def pushStack(self):
        self.code += "\n  "
        self.code += "PUSH EBX"

    def popStack(self):
        self.code += "\n  "
        self.code += "POP EAX"

    def newVariable(self):
        self.code += "\n  "
        self.code += "PUSH DWORD 0"

    def setVariable(self, pos):
        self.code += "\n  "
        self.code += f"MOV [EBP-{pos}], EBX"

    def getVariable(self, pos):
        self.code += "\n  "
        self.code += f"MOV EBX, [EBP-{pos}]"

    def intVal(self, val):
        self.code += "\n  "
        self.code += f"MOV EBX, {val}"

    def addOp(self):
        self.code += "\n  "
        self.code += "ADD EAX, EBX"

    def subOp(self):
        self.code += "\n  "
        self.code += "SUB EAX, EBX"

    def multOp(self):
        self.code += "\n  "
        self.code += "MUL EAX, EBX"

    def divOp(self):
        self.code += "\n  "
        self.code += "DIV EAX, EBX"

    def gtOp(self):
        self.code += "\n  "
        self.code += "CMP EAX, EBX"
        self.code += "\n  "
        self.code += f"JG GT_{self.uid}"
        self.code += "\n  "
        self.code += f"MOV EAX, False"
        self.code += "\n"
        self.code += f"GT_{self.uid}:"
        self.code += "\n  "
        self.code += f"MOV EAX, True"
        self.uid += 1

    def ltOp(self):
        self.code += "\n  "
        self.code += "CMP EAX, EBX"
        self.code += "\n  "
        self.code += f"JL LT_{self.uid}"
        self.code += "\n  "
        self.code += f"MOV EAX, False"
        self.code += "\n"
        self.code += f"LT_{self.uid}:"
        self.code += "\n  "
        self.code += f"MOV EAX, True"
        self.uid += 1

    def eqOp(self):
        self.code += "\n  "
        self.code += "CMP EAX, EBX"
        self.code += "\n  "
        self.code += f"JE EQ_{self.uid}"
        self.code += "\n  "
        self.code += f"MOV EAX, False"
        self.code += "\n"
        self.code += f"EQ_{self.uid}:"
        self.code += "\n  "
        self.code += f"MOV EAX, True"
        self.uid += 1

    def andOp(self):
        self.code += "\n  "
        self.code += "AND EAX, EBX"

    def orOP(self):
        self.code += "\n  "
        self.code += "OR EAX, EBX"

    def finalizeBinOp(self):
        self.code += "\n  "
        self.code += "MOV EBX, EAX"

    def printOp(self):
        self.code += "\n  "
        self.code += "CALL print"

    def createLabel(self, label_type, uid):
        self.code += "\n"
        self.code += f"{label_type}_{uid}:"
        return uid

    def checkExit(self, uid):
        self.code += "\n  "
        self.code += "CMP EBX, False"
        self.code += "\n  "
        self.code += f"JE EXIT_{uid}"

    def closeLoop(self, uid):
        self.code += "\n  "
        self.code += f"JMP LOOP_{uid}"
        self.code += "\n"
        self.code += f"EXIT_{uid}:"

    def checkIf(self, uid):
        self.code += "\n  "
        self.code += "CMP EBX, False"
        self.code += "\n  "
        self.code += f"JE ELSE_{uid}"
        return uid

    def elseCommands(self, uid):
        self.code += "\n"
        self.code += f"ELSE_{uid}:"

    def jumpToEndIfElse(self, uid):
        self.code += "\n  "
        self.code += f"JMP ENDIF_{uid}"

    def closeIfElse(self, uid):
        self.code += "\n"
        self.code += f"ENDIF_{uid}:"

    def nextUID(self):
        self.uid += 1
