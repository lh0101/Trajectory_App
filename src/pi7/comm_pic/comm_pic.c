/**
 * Modulo: Comunicacao MODBUS (simplificada)
 * Usa a Serial0 para comunicar-se
 * [jo:230927] usa UART0 e UART1 para comunicação
 */

/*
 * FreeRTOS includes
 */
//#include "FreeRTOS.h"
//#include "queue.h"
#include <stdbool.h>
#include <stdio.h>
#include "pico/stdlib.h"


// Drivers for UART, LED and Console(debug)
//#include <cr_section_macros.h>
//#include <NXP/crp.h>
//#include "LPC17xx.h"
//#include "type.h"
#include "drivers/uart/uart.h"
//#include "hardware/uart.h"

// Header files for PI7
#include "comm_pic.h"

// === PARÂMETROS DE TEMPO ===
#define DELAY_BYTE_MS     10    // Delay entre cada caractere enviado
#define DELAY_ENTRE_PONTOS_MS 500  // Delay após envio completo de um ponto (ap + ah)

void pic_init(void){

  // TODO: implementar
  
} // pic_init

/**
 * Envia uma string caractere por caractere via UART.
 */
void sendCommandByteByByte(uint8_t portNum, const char* cmd) {
    for (int i = 0; cmd[i] != '\0'; i++) {
        UARTSend(portNum, (uint8_t *)&cmd[i], 1);
        sleep_ms(DELAY_BYTE_MS);
    }
}

/**
 * Envia o comando :apXXXX; seguido de :ah; para o motor correspondente.
 */
void pic_sendToPIC(pic_Data data) {
    

    // Monta o comando :apXXXX;
    char cmd_ap[16];
    
    snprintf(cmd_ap, sizeof(cmd_ap), ":ap%d;", (int)data.setPoint1);
    sendCommandByteByByte(0, cmd_ap);

    snprintf(cmd_ap, sizeof(cmd_ap), ":ap%d;", (int)data.setPoint2);
    sendCommandByteByByte(1, cmd_ap);

    // Pausa entre ap e ah
    sleep_ms(900);

    // Envia comando de habilitação
    sendCommandByteByByte(0, ":ah;");
    sendCommandByteByByte(1, ":ah;");


  //   int delay = 10;
  //   UARTSend(1, ":", 1); // [jo:231004] alternativa linha acima sem NULL no final
  //   sleep_ms(delay);
  //   UARTSend(1, "a", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "p", 1);
  //   sleep_ms(delay);
  //   // UARTSend(portNum, "3", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "-", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "6", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "0", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "0", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, ";", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, ":", 1); // [jo:231004] alternativa linha acima sem NULL no final
  //   sleep_ms(delay);
  //   UARTSend(0, "a", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, "p", 1);
  //   sleep_ms(delay);
  //   //UARTSend(portNum, "3", 1);
  //   //sleep_ms(delay);
  //   UARTSend(0, "6", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, "0", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, "0", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, ";", 1);
  //   sleep_ms(1000);
  //   UARTSend(1, ":", 1); // [jo:231004] alternativa linha acima sem NULL no final
  //   sleep_ms(delay);
  //   UARTSend(1, "a", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, "h", 1);
  //   sleep_ms(delay);
  //   UARTSend(1, ";", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, ":", 1); // [jo:231004] alternativa linha acima sem NULL no final
  //   sleep_ms(delay);
  //   UARTSend(0, "a", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, "h", 1);
  //   sleep_ms(delay);
  //   UARTSend(0, ";", 1);
  // // TODO: implementar
}

extern uint8_t pic_receiveCharFromPIC(uint8_t portNum) {
  return UARTGetChar(portNum, false);
} // pic_receiveFromPIC
