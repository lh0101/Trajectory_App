#ifndef __trj_control_h
#define __trj_control_h

/**
 * Commands for TrajectoryController
 */

#define NO_CMD      0
#define CMD_INICIAR   1
#define CMD_SUSPENDER 2
#define CMD_CONTINUAR  3
#define CMD_ABORTAR    4
#define CMD_JOGX    5
#define CMD_JOGY   6


// Possible status for TrajectoryController
#define STATUS_RUNNING   0
#define STATUS_NOT_RUNNING 1
#define STATUS_JOGGINGX   2
#define STATUS_JOGGINGY   3

// struct for communication between TrajectoryController and Controller
typedef struct {
	int command;
} tcl_Data;

// external interface
extern void tcl_processCommand(tcl_Data data);
extern void tcl_generateSetpoint();
extern void tcl_init();
#endif
