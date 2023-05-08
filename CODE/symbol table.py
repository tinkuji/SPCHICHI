SYMBOL_TABLE = {}
LITERAL_TABLE = {}

# First pass
def first_pass(lines):
    loc_counter = 0
    for line in lines:
        tokens = line.split()
        if tokens and tokens[0] not in ['.', 'START','END']:
            label = tokens[1]
            SYMBOL_TABLE[label] = loc_counter
            if ',' in line:
                LITERAL_TABLE[line.split(',')[1].strip()] = loc_counter
            loc_counter += 1
    print(SYMBOL_TABLE)
    print(LITERAL_TABLE)
input_file = '''START 100
LOOP LDA #0
    ADD X
    STA Y
    MOV A, #5
    JNZ LOOP
    END
X DC 2
Y DS 1'''
lines = input_file.split('\n')

first_pass(lines)