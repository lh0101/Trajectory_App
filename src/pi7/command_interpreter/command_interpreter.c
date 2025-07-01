/*
 * Modulo: Interpretador de Comandos
 * Interpreta os comandos recebidos da IHM e processa-os
 */

#define byte uint8_t

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "queue.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

// Drivers for UART, LED and Console(debug)
//#include <cr_section_macros.h>
//#include <NXP/crp.h>
//#include "LPC17xx.h"
//#include "type.h"

// Includes for PI7
#include "command_interpreter.h"
#include "../trj_state/trj_state.h"
#include "../trj_control/trj_control.h"
#include "../trj_program/trj_program.h"


struct valores_reg val = {
    .INICIAR   = 0,
    .SUSPENDER = 0,
    .CONTINUAR = 0,
    .ABORTAR   = 0,
    .JOGX      = 0,
    .JOGY      = 0,
    .PASSOX    = 0,
    .PASSOY    = 0,
    .X         = 0,
    .Y         = 0,
    .LINHA     = 0
};

// communication with TrajectoryController
extern xQueueHandle qControlCommands;

void ctl_init(){

  // TODO: implementar


} // ctl_init

/************************************************************************
 ctl_ReadRegister
 Le o valor de um registrador
 Parametros de entrada:
    (int) numero do registrador a ser lido
 Retorno:
    (int) valor atual do registrador
*************************************************************************/
int ctl_ReadRegister(int registerToRead) {
   switch (registerToRead) {
      case REG_INICIAR: 
         return val.INICIAR;
      case REG_SUSPENDER: 
         return val.SUSPENDER;
      case REG_ABORTAR: 
         return val.ABORTAR;
      case REG_CONTINUAR: 
         return val.CONTINUAR;
      case REG_JOGX: 
         return val.JOGX;
      case REG_JOGY: 
         return val.JOGY;
      case REG_PASSOX: 
         return val.PASSOX;
      case REG_PASSOY: 
         return val.PASSOY;
      case REG_X:
         return (int)tst_getX();
      case REG_Y:
         return (int)tst_getY();
      case REG_LINHA:
         return tst_getCurrentLine();
   } // switch
   return CTL_ERR;
} // ctl_ReadRegister

/************************************************************************
 ctl_WriteRegister
 Escreve o valor de um registrador. Notar que, quando for um registrador
 de controle (por exemplo, INICIAR) deve-se processar as acoes relativas
 a este registrador (no exemplo, iniciar o movimento)
 Parametros de entrada:
    (int) numero do registrador a ser escrito
    (int) valor a ser escrito
 Retorno:
    TRUE se escrita foi aceita, FALSE caso contrario.
*************************************************************************/
int ctl_WriteRegister(int registerToWrite, int value) {
  tcl_Data command;

  printf("Register %d Value %d\n", registerToWrite, value);
  switch(registerToWrite) {
  case REG_INICIAR:
	  printf("start program\n");
	  command.command = CMD_INICIAR;
     val.INICIAR = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
   case REG_SUSPENDER:
	  printf("suspend program\n");
	  command.command = CMD_SUSPENDER;
     val.SUSPENDER = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
   case REG_CONTINUAR:
	  printf("continue program\n");
	  command.command = CMD_CONTINUAR;
     val.CONTINUAR = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
   case REG_ABORTAR:
	  printf("abort program\n");
	  command.command = CMD_ABORTAR;
     val.ABORTAR = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
     // nao sei se aqui mas em algum momento tem que zerar current line
   case REG_JOGX:
	  printf("jogx\n");
	  command.command = CMD_JOGX;
     val.JOGX = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
   case REG_JOGY:
	  printf("jogy\n");
	  command.command = CMD_JOGY;
     val.JOGY = value;
	  xQueueSend(qControlCommands, &command, portMAX_DELAY);
	  break;
   case REG_PASSOX:
	  printf("passox\n");
     val.PASSOX = value;
	//   command.command = CMD_JOGY;
	//   xQueueSend(qControlCommands, &command, portMAX_DELAY);
   // todo implementar o que fazer com valor de passo
	  break;
   case REG_PASSOY:
	  printf("passoy\n");
     val.PASSOY = value;
	//   command.command = CMD_JOGY;
	//   xQueueSend(qControlCommands, &command, portMAX_DELAY);
   // todo implementar o que fazer com valor de passo
	  break;
   default:
	  printf("unknown register to write\n");
	  break;
  } //switch
  return true; //TRUE;
} // ctl_WriteRegister

/************************************************************************
 ctl_WriteProgram
 Escreve um programa. Notar que o programa foi informado como um byte[]
 logo compete neste caso ao controlador decodificar o programa e armazena-lo
 no DEVICE_MEMORY.
 Parametros de entrada:
    (byte[]) bytes que compoe o programa de movimentacao
 Retorno:
    TRUE se escrita foi aceita, FALSE caso contrario.
*************************************************************************/
int ctl_WriteProgram(int* program_bytes, int totalPoints) {
   static char texto[1024];
   texto[0] = '\0';
   char tmp[64];
   // --- Monta string para tpr_storeProgram ---
   
   printf("[DEBUG] Total de pontos:", totalPoints);

   for (int i = 0; i < totalPoints; i++) {
      int x = program_bytes[i * 2];
      int y = program_bytes[i * 2 + 1];
      sprintf(tmp, "X:%d,Y:%d;", x, y);
      strcat(texto, tmp);
   }

   printf("[DEBUG] Chamando tpr_storeProgram com texto:\n    %s\n", texto);
   tpr_storeProgram(texto);

  return true; //TRUE;
} // ctl_WriteRegister
