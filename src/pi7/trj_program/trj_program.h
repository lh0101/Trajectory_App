#ifndef __trj_program_h
#define __trj_program_h

#define MAX_PROGRAM_LINES 200

typedef struct {
	float x;
	float y;
} tpr_Data;

extern tpr_Data tpr_program[MAX_PROGRAM_LINES]; 

extern void tpr_storeProgram(char* texto);
extern tpr_Data tpr_getLine(int line);
extern void tpr_init();
#endif
