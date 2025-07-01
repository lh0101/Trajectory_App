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
#define DELAY_ENTRE_PONTOS_MS 100  // Delay após envio completo de um ponto (ap + ah)

void pic_init(void){

  // TODO: implementar
  
} // pic_init

/**
 * Envia uma string caractere por caractere via UART.
 */
static void sendCommandByteByByte(uint8_t portNum, const char* cmd) {
    for (int i = 0; cmd[i] != '\0'; i++) {
        UARTSend(portNum, &cmd[i], 1);
        sleep_ms(DELAY_BYTE_MS);
    }
}

/**
 * Envia o comando :apXXXX; seguido de :ah; para o motor correspondente.
 */
void pic_sendToPIC(uint8_t portNum, pic_Data data) {
    // Seleciona o setpoint com base no canal
    int setpoint = (portNum == 0) ? (int)data.setPoint1 : (int)data.setPoint2;

    // Limita o valor do setpoint
    if (setpoint < 0) setpoint = 0;
    if (setpoint > 9999) setpoint = 9999;

    // Monta o comando :apXXXX;
    char cmd_ap[16];
    snprintf(cmd_ap, sizeof(cmd_ap), ":ap%d;", setpoint);
    sendCommandByteByByte(portNum, cmd_ap);

    // Pausa entre ap e ah
    sleep_ms(5);

    // Envia comando de habilitação
    sendCommandByteByByte(portNum, ":ah;");

    // Delay entre pontos consecutivos
    sleep_ms(DELAY_ENTRE_PONTOS_MS);
}

extern uint8_t pic_receiveCharFromPIC(uint8_t portNum) {
  return UARTGetChar(portNum, false);
} // pic_receiveFromPIC
