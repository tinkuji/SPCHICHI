#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TABLE_SIZE 100

typedef struct {
    char name[20];
    int address;
} SymbolEntry;

typedef struct {
    char value[20];
    int address;
} LiteralEntry;

int main() {
    char assemblyCode[] = "START LDA A\n"
                          "ADD B\n"
                          "STA RESULT\n"
                          "MOV A, #5\n"
                          "SUB A, #3\n"
                          "HLT\n"
                          "A DB 10\n"
                          "B DB 20\n"
                          "RESULT DB 0\n"
                          "END START\n";

    SymbolEntry symbolTable[MAX_TABLE_SIZE];
    LiteralEntry literalTable[MAX_TABLE_SIZE];

    int symbolCount = 0;
    int literalCount = 0;

    // Tokenize the assembly code
    char* token = strtok(assemblyCode, " \n");
    while (token != NULL) {
        // Check if it is a symbol declaration
        if (strcmp(token, "DB") == 0) {
            // Extract the symbol name and its value
            token = strtok(NULL, " \n");
            strcpy(symbolTable[symbolCount].name, token);
            symbolTable[symbolCount].address = -1;  // Placeholder address

            token = strtok(NULL, " \n");
            token = strtok(NULL, " \n");

            symbolCount++;
        }
        // Check if it is a literal usage
        else if (token[0] == '#') {
            // Extract the literal value
            token = strtok(token, "#");
            strcpy(literalTable[literalCount].value, token);
            literalTable[literalCount].address = -1;  // Placeholder address

            literalCount++;
        }

        token = strtok(NULL, " \n");
    }

    // Assign addresses to the symbol table
    int currentAddress = 1000;  // Start address of the program
    for (int i = 0; i < symbolCount; i++) {
        symbolTable[i].address = currentAddress;
        currentAddress += 1;  // Assuming each symbol takes 1 byte of memory
    }

    // Assign addresses to the literal table
    for (int i = 0; i < literalCount; i++) {
        literalTable[i].address = currentAddress;
        currentAddress += 1;  // Assuming each literal takes 1 byte of memory
    }

    // Print the symbol table
    printf("Symbol Table:\n");
    for (int i = 0; i < symbolCount; i++) {
        printf("%s\t%d\n", symbolTable[i].name, symbolTable[i].address);
    }

    printf("\n");

    // Print the literal table
    printf("Literal Table:\n");
    for (int i = 0; i < literalCount; i++) {
        printf("%s\t%d\n", literalTable[i].value, literalTable[i].address);
    }

    return 0;
}

