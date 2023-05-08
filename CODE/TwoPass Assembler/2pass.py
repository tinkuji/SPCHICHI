import pandas as pd
print()
print()
f = open("SPCC1.txt", "r")
n = 0
lines = []
ads = ['START', 'END', 'USING', 'DROP', 'DC', 'DS']
adsAddress = ['P1 START', 'P1 END', 'P1 USING', 'P1 DROP', 'P1 DC', 'P1 DS']
for l in f:
    n = n+1
    lines.append(l)
instructions = []
for l in lines:
    instructions.append(l.strip().split())


def generateInstruction(opcode, binOpcode, length, mode):
    instruction = [opcode, binOpcode, length, mode]
    return instruction


def isLiteral(i):
    if (i.find("F'") == -1 or i.find("H'") == -1):
        return False
    else:
        return True


def getValueAndSize(i):
    idx = i.find("F'")
    if (idx != -1):
        val = int(i[idx+2:-1])
        return val, 4
    else:
        idx = i.find("H'")
        if (idx != -1):
            val = int(i[idx+2:-1])
            return val, 2
        else:
            return 0, 0


def getSTIdx(s, st):
    i = 0
    for j in st:
        if (s == j[0]):
            return i
        else:
            i = i+1
    return -1


def performPassOne(instructions):
    mot = []
    st = []
    lt = []
    lc = [0]
    op1 = []
    symbols = []
    opcodes = []
    arguments = []
    for i in instructions:
        if (len(i) == 1):
            lc.append(lc[-1])
            op1.append("-")
            symbols.append("-")
            opcodes.append(i[0])
            arguments.append("-")

        if (len(i) == 3):
            if (i[1].upper() == 'START'):
                lc.append(int(i[2]))
                mode = "R"
                if (int(i[2]) != 0):
                    mode = "A"
                st.append([i[0], i[2], 1, mode])
                op1.append("-")

            else:
                if (i[1].upper() == 'DC'):
                    symbol = i[0]
                    value, size = getValueAndSize(i[2])
                    mode = "R"
                    st.append([i[0], lc[-1], size, mode])
                    lt.append([i[2], lc[-1], size, mode])
                    lc.append(lc[-1] + size)
                    op1.append(value)
                else:
                    lc.append(lc[-1])
                    st.append([i[0], lc[-1], size, mode])
                    op1.append("-")
                symbols.append(i[0])
                opcodes.append(i[1])
                arguments.append(i[2])

        if (len(i) == 2):
            if (i[0] not in ads):
                if (i[0].find("R") != -1):
                    instruction = generateInstruction(i[0], "-", 2, "000")
                    mot.append(instruction)
                    lc.append(lc[-1] + 2)
                    operands = i[1].split(",")
                    if (not isLiteral(operands[1])):
                        operands[1] = "-"
                    operands = ",".join(operands)
                    op_inst = " ".join([i[0], operands])
                    op1.append(op_inst)
                else:
                    instruction = generateInstruction(i[0], "-", 4, "001")
                    mot.append(instruction)
                    lc.append(lc[-1] + 4)
                    operands = i[1].split(",")
                    if (not isLiteral(operands[1])):
                        operands[1] = "-"
                    operands = ",".join(operands)
                    op_inst = " ".join([i[0], operands])
                    op1.append(op_inst)
            else:
                lc.append(lc[-1])
                op1.append("-")
            symbols.append("-")
            opcodes.append(i[0])
            arguments.append(i[1])

    firstPass = pd.DataFrame(list(zip(lc, op1)), columns=[
                             'Relative Address', 'Mnemonic'])
    motpd = pd.DataFrame(
        mot, columns=['Opcode', 'Binary Opcode', 'Length', 'Format'])
    ltpd = pd.DataFrame(
        lt, columns=['Literal', 'Value', 'Length', 'Relocation'])
    stpd = pd.DataFrame(
        st, columns=['Symbol', 'Value', 'Length', 'Relocation'])
    potpd = pd.DataFrame(list(zip(ads, adsAddress)), columns=[
                         'Pseudo Opcode', 'Address'])

    print("MOT: ")
    print(motpd)
    print("\n")
    print("POT: ")
    print(potpd)
    print("\n")
    print("LT: ")
    print(ltpd)
    print("\n")
    print("ST: ")
    print(stpd)
    print("\n")
    print("Output of PASS 1: ")
    print(firstPass)

    performPassTwo(instructions, lc, mot, lt, st,
                   op1, symbols, opcodes, arguments)


def performPassTwo(instructions, lc, mot, lt, st, op1, symbols, opcodes, arguments):
    bt = []
    br = []
    op2 = []
    for i in instructions:
        if (len(i) == 1):
            op2.append("-")

        if (len(i) == 3):
            if (i[1].upper() == 'START'):
                op2.append("-")
            else:
                if (i[1].upper() == 'DC'):
                    symbol = i[0]
                    value, size = getValueAndSize(i[2])
                    mode = "R"
                    st.append([i[0], lc[-1], size, mode])
                    lt.append([i[2], lc[-1], size, mode])
                    lc.append(lc[-1] + size)
                    op2.append(value)
                else:
                    lc.append(lc[-1])
                    st.append([i[0], lc[-1], size, mode])
                    op2.append("-")

        if (len(i) == 2):
            if (i[0] not in ads):
                if (i[0].find("R") != -1):
                    print(i[0]+" RR Format")
                    instruction = generateInstruction(i[0], "", 2, "000")
                    mot.append(instruction)
                    lc.append(lc[-1] + 2)
                    operands = i[1].split(",")
                    if (not isLiteral(operands[1])):
                        operands[1] = "-"
                    operands = ",".join(operands)
                    op_inst = " ".join([i[0], operands])
                    op1.append(op_inst)

                else:
                    operands = i[1].split(",")
                    idx = getSTIdx(operands[1], st)

                    if (idx != -1):
                        value = st[idx][1]
                        base = 0
                        if (len(br) > 0):
                            base = br[0]
                        operands[1] = str(value) + "(0," + str(base) + ")"
                        operands = ",".join(operands)
                        op_inst = " ".join([i[0], operands])
                        op2.append(op_inst)

            else:
                lc.append(lc[-1])
                op2.append("-")

                if (i[0] == "USING"):
                    operands = i[1].split(",")
                    idx = getSTIdx(operands[1], st)
                    if (idx == -1):
                        if (not isLiteral(operands[1])):
                            value = int(operands[1])
                            br.append(value)
                        else:
                            value, size = getValueAndSize(operands[1])

                    else:
                        br.append(st[idx][1])

    for i in range(0, 16):
        if (i in br):
            bt.append([i, "Y", 00])
        else:
            bt.append([i, "N", 00])

    secondPass = pd.DataFrame(list(zip(lc, op2)), columns=[
                              'Relative Address', 'Mnemonic'])
    btpd = pd.DataFrame(bt, columns=['Register', 'Availability', 'Contents'])

    print("BT: ")
    print(btpd)
    print()
    print("Output of PASS 2: ")
    print(secondPass)
    print()
    print("Result: ")
    output = pd.DataFrame(list(zip(symbols, opcodes, arguments, lc, op1, op2)),
                          columns=['Symbol', 'Opcode', 'Operand', 'Relative Address', 'PASS 1', 'PASS 2'])
    print(output)
    print()
    print()


performPassOne(instructions)

'''
MOT: 
  Opcode Binary Opcode  Length Format
0      L             -       4    001
1      A             -       4    001
2     ST             -       4    001


POT: 
  Pseudo Opcode   Address
0         START  P1 START
1           END    P1 END
2         USING  P1 USING
3          DROP   P1 DROP
4            DC     P1 DC
5            DS     P1 DS


LT:
  Literal  Value  Length Relocation
0    F'4'     12       4          R
1    F'5'     16       4          R


ST:
  Symbol Value  Length Relocation
0     Ni     0       1          R
1   FOUR    12       4          R
2   FIVE    16       4          R
3   TEMP    20       4          R


Output of PASS 1:
   Relative Address Mnemonic
0                 0        -
1                 0        -
2                 0    L 1,-
3                 4    A 1,-
4                 8   ST 1,-
5                12        4
6                16        5
7                20        -
8                20        -
BT: 
    Register Availability  Contents
0          0            N         0
1          1            N         0
2          2            N         0
3          3            N         0
4          4            N         0
5          5            N         0
6          6            N         0
7          7            N         0
8          8            N         0
9          9            N         0
10        10            N         0
11        11            N         0
12        12            N         0
13        13            N         0
14        14            N         0
15        15            Y         0

Output of PASS 2:
   Relative Address       Mnemonic
0                 0              -
1                 0              -
2                 0   L 1,16(0,15)
3                 4   A 1,12(0,15)
4                 8  ST 1,20(0,15)
5                12              4
6                16              5
7                20              -
8                20              -

Result:
  Symbol Opcode Operand  Relative Address  PASS 1         PASS 2
0      -  USING    *,15                 0       -              -
1      -      L  1,FIVE                 0       -              -
2      -      A  1,FOUR                 0   L 1,-   L 1,16(0,15)
3      -     ST  1,TEMP                 4   A 1,-   A 1,12(0,15)
4   FOUR     DC    F'4'                 8  ST 1,-  ST 1,20(0,15)
5   FIVE     DC    F'5'                12       4              4
6   TEMP     DS    1'F'                16       5              5
7      -    END       -                20       -              -
'''
