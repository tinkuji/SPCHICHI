def macro_processor(code):
    # Initialize tables
    macro_name_table = {}
    macro_def_table = {}
    arg_list_array = {}

    # Process each line of code
    for line in code:
        lines = line.split()
        # Check for macro definition
        if lines[0] == 'MACRO':
            # Parse macro name and arguments
            macro_name, args = lines[1], lines[2:]

            # Add macro to name table
            macro_name_table[macro_name] = len(macro_def_table)

            # Store macro definition and argument list
            i = 1
            while "MEND" not in code[i]:
                macro_def_table[len(macro_def_table)] = code[i]
                i += 1
            arg_list_array[len(macro_def_table)] = args

            # Remove macro definition from code
            code.remove(line)

            # Remove ENDM from code


        else:
            if lines[0] in macro_name_table:
                print(macro_def_table.values())
            break
        # Check for macro invocation

    # Display tables
    print('Macro Name Table:')
    print(macro_name_table)
    print('Macro Definition Table:')
    print(macro_def_table)
    print('Argument List Array:')
    print(arg_list_array)

    # Return processed code
    return code


str1 = '''MACRO ADD 1 2
    LDA %1
    ADD %2
    STA %1
    MEND
    MAIN
    ADD X Y
    HLT
    END
'''

str2 = str1.split('\n')

macro_processor(str2)