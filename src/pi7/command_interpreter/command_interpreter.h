#ifndef __command_interpreter_h
#define __command_interpreter_h

#include <stdint.h>

// identification of register to write
#define REG_INICIAR 1
#define REG_SUSPENDER 2
#define REG_CONTINUAR 3
#define REG_ABORTAR 4
#define REG_JOGX 5
#define REG_JOGY 6
#define REG_PASSOX 7
#define REG_PASSOY 8
#define REG_X 9
#define REG_Y 10
#define REG_LINHA 11

// error
#define CTL_ERR -1

struct valores_reg {
    int INICIAR;
    int SUSPENDER;
    int CONTINUAR;
    int ABORTAR;
    int JOGX;
    int JOGY;
    int PASSOX;
    int PASSOY;
    int X;
    int Y;
    int LINHA;
};

// único extern, instanciado em command_interpreter.c
extern struct valores_reg val;

extern int ctl_ReadRegister(int registerToRead);
extern int ctl_WriteRegister(int registerToWrite, int value);
extern int ctl_WriteProgram(int* programBytes, int totalPoints);
extern void ctl_init();

#endif
