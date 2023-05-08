#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TABLE_SIZE 100

typedef struct {
    char name[20];
    int address;
} SymbolEntry;

typedef struct {
    char name[20];
    int value;
} BaseEntry;

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
                          "BASE A\n"
                          "END START\n";

    SymbolEntry symbolTable[MAX_TABLE_SIZE];
    BaseEntry baseTable[MAX_TABLE_SIZE];

    int symbolCount = 0;
    int baseCount = 0;

    int locationCounter = 0;

    // Tokenize the assembly code
    char* token = strtok(assemblyCode, " \n");
    while (token != NULL) {
        // Check if it is a symbol declaration
        if (strcmp(token, "DB") == 0) {
            // Extract the symbol name and its value
            token = strtok(NULL, " \n");
            strcpy(symbolTable[symbolCount].name, token);
            symbolTable[symbolCount].address = locationCounter;

            token = strtok(NULL, " \n");
            token = strtok(NULL, " \n");

            symbolCount++;
        }
        // Check if it is a base declaration
        else if (strcmp(token, "BASE") == 0) {
            // Extract the base name
            token = strtok(NULL, " \n");
            strcpy(baseTable[baseCount].name, token);
            baseTable[baseCount].value = locationCounter;

            baseCount++;
        }

        token = strtok(NULL, " \n");
        locationCounter++;
    }

    // Print the base table
    printf("Base Table:\n");
    for (int i = 0; i < baseCount; i++) {
        printf("%s\t%d\n", baseTable[i].name, baseTable[i].value);
    }

    printf("\n");

    // Print the location counter
    printf("Location Counter: %d\n", locationCounter);

    return 0;
}

