#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TABLE_SIZE 100

typedef struct {
    char mnemonic[10];
    int opcode;
} MOTEntry;

typedef struct {
    char mnemonic[10];
    char description[50];
} POTEntry;

int main() {
    MOTEntry motTable[MAX_TABLE_SIZE];
    POTEntry potTable[MAX_TABLE_SIZE];

    int motCount = 0;
    int potCount = 0;

    // Add entries to the Machine Operation Table (MOT)
    strcpy(motTable[motCount].mnemonic, "LDA");
    motTable[motCount].opcode = 1;
    motCount++;

    strcpy(motTable[motCount].mnemonic, "ADD");
    motTable[motCount].opcode = 2;
    motCount++;

    strcpy(motTable[motCount].mnemonic, "SUB");
    motTable[motCount].opcode = 3;
    motCount++;

    // Add entries to the Pseudo Operation Table (POT)
    strcpy(potTable[potCount].mnemonic, "START");
    strcpy(potTable[potCount].description, "Start of program");
    potCount++;

    strcpy(potTable[potCount].mnemonic, "END");
    strcpy(potTable[potCount].description, "End of program");
    potCount++;

    // Print the Machine Operation Table (MOT)
    printf("Machine Operation Table (MOT):\n");
    printf("Mnemonic\tOpcode\n");
    for (int i = 0; i < motCount; i++) {
        printf("%s\t\t%d\n", motTable[i].mnemonic, motTable[i].opcode);
    }

    printf("\n");

    // Print the Pseudo Operation Table (POT)
    printf("Pseudo Operation Table (POT):\n");
    printf("Mnemonic\tDescription\n");
    for (int i = 0; i < potCount; i++) {
        printf("%s\t\t%s\n", potTable[i].mnemonic, potTable[i].description);
    }

    return 0;
}

