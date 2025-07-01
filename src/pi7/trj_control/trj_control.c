/**
 * Modulo: Controlador de trajetoria (exemplo!!)
 *
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"

#include <stdio.h>

// Header files for PI7
#include "trj_control.h"
#include "../trj_program/trj_program.h"
#include "../polinomio_pc/polinomio.h"
#include "../trj_state/trj_state.h"
#include "../comm_pic/comm_pic.h"
#include "../command_interpreter/command_interpreter.h"


// local variables
int tcl_status;
extern xQueueHandle qCommPIC;

void tcl_generateSetpoint() {

  // TODO: implementar

  int currLine;
  int theta1;
  int theta2;
  tpr_Data line;
  pic_Data toPic;

  if (tcl_status == STATUS_RUNNING) {
    currLine = tst_getCurrentLine();
    theta1 = 100*tpr_getLineTheta1(currLine).theta;
    theta2 = 100*tpr_getLineTheta2(currLine).theta;
    toPic.setPoint1 = theta1;
    toPic.setPoint2 = theta2;
    // printf("CurrLine %d, X1:%d\n", currLine, line.x);
    xQueueSend(qCommPIC, &toPic, portMAX_DELAY);
    currLine++;
    tst_setCurrentLine(currLine);
    return;
  }

  if (tcl_status == STATUS_JOGGINGX) {
    float xj;
    float yj;
    currLine = tst_getCurrentLine();
    printf("CurrLine %d\n", currLine);
    line = tpr_getLine(currLine);
    float passox = ctl_ReadRegister(7);
    if (ctl_ReadRegister(5) == -1){
      passox = -passox; ///// criar funcao
    }
    xj = line.x + passox;
    yj = line.y ; ///// criar funcao
    toPic.setPoint1 = xj;
    toPic.setPoint2 = yj;
    xQueueSend(qCommPIC, &toPic, portMAX_DELAY);
    return;
  }

  if (tcl_status == STATUS_JOGGINGY) {
    float xj;
    float yj;
    currLine = tst_getCurrentLine();
    printf("CurrLine %d\n", currLine);
    line = tpr_getLine(currLine);
    float passoy = ctl_ReadRegister(8);
    if (ctl_ReadRegister(6) == -1){
      passoy = -passoy; ///// criar funcao
    }
    xj = line.x;
    yj = line.y + passoy; ///// criar funcao
    toPic.setPoint1 = xj;
    toPic.setPoint2 = yj;
    xQueueSend(qCommPIC, &toPic, portMAX_DELAY);
    return;
  }

  else {
    return;
  }

  
} // trj_generateSetpoint

void tcl_processCommand(tcl_Data data) {

  if ((data.command == CMD_SUSPENDER) || (data.command == CMD_ABORTAR)) {
    tcl_status = STATUS_NOT_RUNNING;
  }

  if ((data.command == CMD_INICIAR) || (data.command == CMD_CONTINUAR)) {
    printf("starting trajectory\n");
    tcl_status = STATUS_RUNNING;
  }

  if (data.command == CMD_INICIAR) {
    tst_setCurrentLine(0);
  }

  if ((data.command == CMD_JOGX)) {
    printf("JOGX\n");
    tcl_status = STATUS_JOGGINGX;
  }

  if ((data.command == CMD_JOGY)) {
    printf("JOGY\n");
    tcl_status = STATUS_JOGGINGY;
  }

} // trj_executeCommand

void tcl_init() {
  tcl_status = STATUS_NOT_RUNNING;
} // init
