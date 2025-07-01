/**
 * Modulo: Comunicacao MODBUS (simplificada)
 * Usa a Serial0 para comunicar-se
 *
 * Versão para DEBUG: imprime no console todo caractere recebido,
 * o quadro completo (rxBuffer) e mensagens de LRC/funcionalidade.
 */

/*
 * FreeRTOS includes
 */
#include "FreeRTOS.h"
#include "portmacro.h"
#include "queue.h"
#include "projdefs.h"

// std includes
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>        // adicionado para strcat/strchr

// PICO W include
//#include "hardware/uart.h"
#include "pico/stdio.h"

#define byte uint8_t

// Drivers para UART, LED e Console(debug)
//#include <cr_section_macros.h>
//#include <NXP/crp.h>
//#include "LPC17xx.h"
//#include "type.h"
//#include "drivers/uart/uart.h"
//#include "drivers/console/basic_io.h"
//#include "drivers/ledonboard/leds.h"

// Includes para PI7
#include "modbus.h"
#include "../command_interpreter/command_interpreter.h"
#include "../trj_program/trj_program.h"  // assinatura: extern void tpr_storeProgram(char* texto);

// CommModes: Dev_mode para debug; escreve na console
//            Real_mode para execucao real escreve nas UARTs
//#define DEVELOPMENT_MODE 0
//#define REAL_MODE 1

// *** Configuracao da serial (_mode = REAL_MODE)
//#define BAUD 115200 // 9600
#define MAX_RX_SIZE 2000  // ajustado para caber grandes blocos de WRITE FILE

// *** endereco deste node
#define MY_ADDRESS 0x01

// Function Codes
#define READ_REGISTER  0x03
#define WRITE_REGISTER 0x06
#define WRITE_FILE     0x15

// Defines de uso geral
#define MB_NO_CHAR 0xff

// Estados do canal de recepcao
#define HUNTING_FOR_START_OF_MESSAGE 0
#define HUNTING_FOR_END_OF_MESSAGE   1
#define IDLE                         3
#define MESSAGE_READY                4

int _state;
int _mode;
byte rxBuffer[MAX_RX_SIZE];
int idxRxBuffer;
byte txBuffer[2048];
int idxTxBuffer;
// extern xQueueHandle qCommDev;

/************************************************************************
 initCommunication
 Inicializa modulo de comunicacaoes
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void com_init() {
    _state = HUNTING_FOR_START_OF_MESSAGE;
    // _mode = DEVELOPMENT_MODE; // [jo:231004] testando REAL_MODE
    // //_mode = REAL_MODE; // [jo:231004] testando REAL_MODE
    // if (_mode == REAL_MODE ) {
    //   if (!UARTIsEnabled(0)) UARTInit(0, BAUD);
    //   if (!UARTIsEnabled(1)) UARTInit(1, BAUD);
    // }
    printf("[DEBUG] com_init(): estado inicial = HUNTING_FOR_START_OF_MESSAGE\n");
} // initCommunication

/************************************************************************
 sendTxBufferToSerialUSB
 Envia o conteudo atual do txBuffer pela serial USB
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void sendTxBufferToSerialUSB(void) {
    // printf("[DEBUG] Enviando resposta Modbus ASCII: %s\n", txBuffer);
    printf("[PICO] %s\r\n", txBuffer);
}

/************************************************************************
 putCharToSerial
 Escreve o conteudo atual do txBuffer na serial, de acordo com _mode
 _mode = DEV_MODE : printf na console de debug
 _mode = REAL_MODE : escreve da UART0
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void putCharToSerial() {
    // if (_mode == DEVELOPMENT_MODE ) {
    //   printf("%s\r\n", txBuffer); // [jo:231003] SOLVED: pode enviar direto para o console
    // } else { // _mode == REAL_MODE
    //   UARTSendNullTerminated(0, txBuffer);
    // }
    printf("[DEBUG] putCharToSerial(): %s\n", txBuffer);
    printf("%s\r\n", txBuffer);
} // putCharToSerial

/************************************************************************
 getCharFromSerial
 Obtem um caracter da interface serial. A interface a utilizar depende de
 _mode = DEV_MODE : obter caracter da fila qCommDev
 _mode = REAL_MODE : obter da UART0
 Parametros de entrada:
    nenhum
 Retorno:
    (int) caracter obtido ou MB_NO_CHAR se nenhum caracter disponivel
*************************************************************************/
char getCharFromSerial() {
    // char ch = NO_CHAR;
    // BaseType_t status = pdFAIL;
    // if (_mode == DEVELOPMENT_MODE ) {
    //   status = xQueueReceive(qCommDev, &ch, pdMS_TO_TICKS(200));
    //   if (status == pdFAIL) ch = NO_CHAR;
    // } else { // REAL_MODE
    //   ch = UARTGetChar(0, false);
    // }
    // return ch;
    return getchar_timeout_us(0);
} // getCharFromSerial

/************************************************************************
 decode, encodeLow, encodeHigh
 Transforma de/para o codigo ASCII de 2 bytes usado no protocolo
 Parametros de entrada:
    decode: high, low
    encodeLow, encodeHigh: value
 Retorno:
    decode: (byte) conversao de 2 bytes ASCII para 1 byte
    encodeLow, encodeHigh: (byte) valor convertido de 1 byte para 1 byte ASCII
*************************************************************************/
byte decode(byte high, byte low) {
    byte x, y;
    if (low < 'A') {
        x = (low & 0x0f);
    } else {
        x = (low & 0x0f) + 0x09;
    }
    if (high < 'A') {
        y = (high & 0x0f);
    } else {
        y = (high & 0x0f) + 0x09;
    }
    return (x | (y << 4));
} // decode

byte encodeLow(byte value) {
    byte x = value & 0x0f;
    if (x < 10) {
        return (0x30 + x);
    } else {
        return (0x41 + (x - 10));
    }
} // encodeLow

byte encodeHigh(byte value) {
    byte x = ((value & 0xf0) >> 4);
    if (x < 10) {
        return (0x30 + x);
    } else {
        return (0x41 + (x - 10));
    }
} // encodeHigh

/**
 * decode16:
 * Recebe quatro caracteres ASCII hex: h1/l1 para o byte alto,
 * h2/l2 para o byte baixo. Retorna o inteiro 16 bits.
 */
uint16_t decode16(byte h1, byte l1, byte h2, byte l2) {
    uint16_t hi = decode(h1, l1);
    uint16_t lo = decode(h2, l2);
    return (hi << 8) | lo;
}

/**
 * encode16:
 * Dado um valor 16 bits, preenche os quatro caracteres ASCII
 * apontados por outH1,outL1 (byte alto) e outH2,outL2 (byte baixo).
 */
void encode16(uint16_t value,
              byte *outH1, byte *outL1,
              byte *outH2, byte *outL2) {
    byte hi = (value >> 8) & 0xFF;
    byte lo = value & 0xFF;
    *outH1 = encodeHigh(hi);
    *outL1 = encodeLow(hi);
    *outH2 = encodeHigh(lo);
    *outL2 = encodeLow(lo);
}

/************************************************************************
 calculateLRC, checkLRC
 Calcula e verifica o checksum
 Parametros de entrada:
    calculateLRC: (byte[]) bytes, (int) start, (int) end
    checkLRC: nenhum
 Retorno:
    calculateLRC: (byte) LRC calculado
    checkLRC: TRUE se correto, FALSE caso contrario
*************************************************************************/
byte calculateLRC(byte* frame, int start, int end) {
    byte accum = 0;
    for (int i = start; i < end; i++) {
        accum = (byte)((accum + frame[i]) & 0xFF);
    }
    accum = (byte)((0xFF - accum) + 0x01);
    return accum;
} // calculateLRC

int checkLRC() {
    byte receivedLRC   = decode(rxBuffer[idxRxBuffer - 3], rxBuffer[idxRxBuffer - 2]);
    byte calculatedLRC = calculateLRC(rxBuffer, 1, idxRxBuffer - 3);
    if (receivedLRC == calculatedLRC) {
        printf("[DEBUG] LRC OK: recebido=0x%02X, calculado=0x%02X\n", receivedLRC, calculatedLRC);
        return true;
    } else {
        printf("[DEBUG] LRC INVÁLIDO: recebido=0x%02X, calculado=0x%02X\n", receivedLRC, calculatedLRC);
        return false;
    }
} // checkLRC

/************************************************************************
 processReadRegister, processWriteRegister, processWriteFile
 As funcoes realizam o processamento das mensagens
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void processReadRegister() {
    int registerToRead;
    int registerValue;
    byte lrc;

    printf("[DEBUG] processReadRegister: mensagem recebida completa: ");
    for (int j = 0; j <= idxRxBuffer; j++) {
        putchar(rxBuffer[j]);
    }
    printf("\n");

    registerToRead = decode(rxBuffer[5], rxBuffer[6]);
    printf("[DEBUG] processReadRegister: registerToRead = %d\n", registerToRead);

    // Aciona controller para obter valor. Note que a informacao
    // ate´ poderia ser acessada diretamente. Mas a arquitetura MVC
    // exige que todas as interacoes se deem atraves do controller.
    registerValue = ctl_ReadRegister(registerToRead);
    printf("[DEBUG] ctl_ReadRegister(%d) retornou = %d\n", registerToRead, registerValue);

    // Monta frame de resposta e a envia
    // : [SlaveAddr][FC=03][ByteCount=01][Hi(Value)][Lo(Value)][LRC][CR][LF]
    txBuffer[0]  = ':';
    txBuffer[1]  = encodeHigh(MY_ADDRESS);
    txBuffer[2]  = encodeLow(MY_ADDRESS);
    txBuffer[3]  = encodeHigh(READ_REGISTER);
    txBuffer[4]  = encodeLow(READ_REGISTER);
    txBuffer[5]  = encodeHigh(1); // byte count field  (high part)
    txBuffer[6]  = encodeLow(1);  // byte count field (low part)
    txBuffer[7]  = encodeHigh(registerValue);
    txBuffer[8]  = encodeLow(registerValue);
    lrc = calculateLRC(txBuffer, 1, 8);
    printf("[DEBUG] processReadRegister LRC calculado = 0x%02X\n", lrc);
    txBuffer[9]  = encodeHigh(lrc);
    txBuffer[10] = encodeLow(lrc);
    txBuffer[11] = 0x0d;
    txBuffer[12] = 0x0a;
    txBuffer[13] = 0; // null to end as string
    sendTxBufferToSerialUSB();
} // processReadRegister

void processWriteRegister() {
    int registerToWrite;
    int registerValue;
    byte lrc;

    printf("[DEBUG] processWriteRegister: mensagem recebida completa: ");
    for (int j = 0; j <= idxRxBuffer; j++) {
        putchar(rxBuffer[j]);
    }
    printf("\n");

    registerToWrite = decode(rxBuffer[5], rxBuffer[6]);
    registerValue   = decode(rxBuffer[7], rxBuffer[8]);
    printf("[DEBUG] processWriteRegister: registerToWrite = %d, registerValue = %d\n",
           registerToWrite, registerValue);

    // Aciona controller porque a arquitetura MVC
    // exige que todas as interacoes se deem atraves do controller.
    int ret = ctl_WriteRegister(registerToWrite, registerValue);
    printf("[DEBUG] ctl_WriteRegister(%d, %d) retornou = %d\n", registerToWrite, registerValue, ret);

    // Monta frame de resposta e a envia
    // : [SlaveAddr][FC=06][RegHi][RegLo][ValHi][ValLo][LRC][CR][LF]
    // :0106011F
    txBuffer[0]  = ':';
    txBuffer[1]  = encodeHigh(MY_ADDRESS);
    txBuffer[2]  = encodeLow(MY_ADDRESS);
    txBuffer[3]  = encodeHigh(WRITE_REGISTER);
    txBuffer[4]  = encodeLow(WRITE_REGISTER);
    txBuffer[5]  = encodeHigh(registerToWrite);
    txBuffer[6]  = encodeLow(registerToWrite);
    txBuffer[7]  = encodeHigh(registerValue);
    txBuffer[8]  = encodeLow(registerValue);
    lrc = calculateLRC(txBuffer, 1, 8);
    printf("[DEBUG] processWriteRegister LRC calculado = 0x%02X\n", lrc);
    txBuffer[9]  = encodeHigh(lrc);
    txBuffer[10] = encodeLow(lrc);
    txBuffer[11] = 0x0d;
    txBuffer[12] = 0x0a;
    txBuffer[13] = 0x00; // null to end as string
    sendTxBufferToSerialUSB();
} // processWriteRegister

void processWriteFile() {
    int i;
    int idxData;
    int values[512];  // até 256 registradores (128 pares X,Y)
    static char texto[1024];
    texto[0] = '\0';
    char tmp[64];
    byte byte_data_for_lrc[MAX_RX_SIZE / 2]; // Para armazenar os bytes decodificados para cálculo do LRC
    int byte_data_idx = 0;

    printf("[DEBUG] processWriteFile: mensagem recebida completa: ");
    for (int j = 0; j <= idxRxBuffer; j++) {
        putchar(rxBuffer[j]);
    }
    printf("\n");

    // --- Decodifica Record Length a partir de rxBuffer[5..8] ---
    int recLen = decode16(rxBuffer[5], rxBuffer[6], rxBuffer[7], rxBuffer[8]);
    printf("[DEBUG] RecordLength declarado = %d\n", recLen);

    // --- Validação de recLen ---
    if (recLen % 2 != 0 || recLen <= 0) {
        printf("[ERRO] RecordLength inválido (não múltiplo de 2 ou <= 0).\n");
        // Enviar uma exceção Modbus aqui seria o correto. Por simplicidade, apenas retorna.
        _state = HUNTING_FOR_START_OF_MESSAGE; // Resetar o estado
        return;
    }

    // Verifica se há ASCII suficiente após recLen
    int bytesEsperados = recLen * 4;  // cada registrador = 2 bytes = 4 ASCII chars
    // idxRxBuffer é o índice do 0x0A (LF). O último dado ASCII é rxBuffer[idxRxBuffer - 3].
    // Note: idxRxBuffer é o índice do 0x0A. A mensagem Modbus ASCII termina em idxRxBuffer - 2 (LRC low byte).
    // O último char antes do LRC é idxRxBuffer - 4.
    int dadosAsciiRecebidos = (idxRxBuffer - 4) - 9 + 1; // Contando os chars do 9 até o último char antes do LRC
    if (dadosAsciiRecebidos < bytesEsperados) {
        printf("[ERRO] Dados ASCII insuficientes: esperados %d, recebidos %d.\n", bytesEsperados, dadosAsciiRecebidos);
        _state = HUNTING_FOR_START_OF_MESSAGE; // Resetar o estado
        return;
    }

    // --- Decodifica os valores (X, Y, X, Y, ...) ---
    idxData = 9;
    for (i = 0; i < recLen; i++) {
        values[i] = decode16(rxBuffer[idxData], rxBuffer[idxData + 1],
                             rxBuffer[idxData + 2], rxBuffer[idxData + 3]);
        idxData += 4;
        printf("[DEBUG] values[%d] = %d\n", i, values[i]);
    }

    // --- Monta string para tpr_storeProgram ---
    int totalPoints = recLen / 2;
    
    ctl_WriteProgram(values, totalPoints);

    // --- Monta a resposta Modbus ASCII (eco dos dados recebidos) ---
    // A resposta deve ser um eco da requisição bem-sucedida.
    // Formato: :[SlaveAddr][FC][RecordLength][Data][LRC][CR][LF]

    txBuffer[0] = ':';
    int current_tx_idx = 1;

    // Adiciona o endereço do escravo (decodificado e depois encodado de volta para ASCII)
    byte_data_for_lrc[byte_data_idx++] = MY_ADDRESS;
    txBuffer[current_tx_idx++] = encodeHigh(MY_ADDRESS);
    txBuffer[current_tx_idx++] = encodeLow(MY_ADDRESS);

    // Adiciona o código de função (decodificado e depois encodado de volta para ASCII)
    byte_data_for_lrc[byte_data_idx++] = WRITE_FILE;
    txBuffer[current_tx_idx++] = encodeHigh(WRITE_FILE);
    txBuffer[current_tx_idx++] = encodeLow(WRITE_FILE);

    // Adiciona o RecordLength (decodificado e depois encodado de volta para ASCII)
    // Este campo RecordLength é de 2 bytes, então precisa ser decodificado como 2 bytes (4 ASCII chars)
    uint16_t decoded_recLen_hi = decode(rxBuffer[5], rxBuffer[6]); // high byte of recLen
    uint16_t decoded_recLen_lo = decode(rxBuffer[7], rxBuffer[8]); // low byte of recLen
    uint16_t decoded_recLen = (decoded_recLen_hi << 8) | decoded_recLen_lo;

    byte_data_for_lrc[byte_data_idx++] = (decoded_recLen >> 8) & 0xFF; // High byte
    byte_data_for_lrc[byte_data_idx++] = decoded_recLen & 0xFF;        // Low byte

    txBuffer[current_tx_idx++] = rxBuffer[5]; // Ecoa os chars ASCII do RecordLength
    txBuffer[current_tx_idx++] = rxBuffer[6];
    txBuffer[current_tx_idx++] = rxBuffer[7];
    txBuffer[current_tx_idx++] = rxBuffer[8];

    // Adiciona os dados (o eco dos valores X, Y, X, Y... em ASCII)
    // A partir de rxBuffer[9] até antes do CR/LF
    // A mensagem recebida tem o LRC nos índices idxRxBuffer - 3 e idxRxBuffer - 2.
    // O último dado ASCII está em idxRxBuffer - 4.
    for (int k = 9; k < (idxRxBuffer - 3); k++) {
        txBuffer[current_tx_idx++] = rxBuffer[k];
        // Para o cálculo do LRC, decodifique cada par de chars ASCII de volta para um byte
        if ((k - 9) % 2 == 0) { // Se for o primeiro char de um par hex
            // Decodifica o par rxBuffer[k] e rxBuffer[k+1] para um byte
            byte decoded_byte = decode(rxBuffer[k], rxBuffer[k+1]);
            byte_data_for_lrc[byte_data_idx++] = decoded_byte;
        }
    }

    // Calcula o LRC da resposta
    // O LRC é calculado sobre os bytes binários da mensagem (endereço, FC, RecordLength, e os dados decodificados)
    byte lrc = calculateLRC(byte_data_for_lrc, 0, byte_data_idx); // Passa os bytes decodificados
    printf("[DEBUG] processWriteFile LRC calculado = 0x%02X\n", lrc);

    // Codifica e adiciona o LRC no final da resposta
    txBuffer[current_tx_idx++] = encodeHigh(lrc);
    txBuffer[current_tx_idx++] = encodeLow(lrc);

    // Adiciona terminadores \r\n e null-terminator
    txBuffer[current_tx_idx++] = 0x0d;
    txBuffer[current_tx_idx++] = 0x0a;
    txBuffer[current_tx_idx++] = 0; // null-terminator para garantir que printf funcione corretamente
    sendTxBufferToSerialUSB();
}//processWriteFile

/************************************************************************
 decodeFunctionCode
 Extrai o function code
 Parametros de entrada:
    nenhum
 Retorno:
    (int) retorna o function code
*************************************************************************/
int decodeFunctionCode() {
    return decode(rxBuffer[3], rxBuffer[4]);
} // extractFunctionCode

/************************************************************************
 processMessage
 Processa uma mensagem ModBus. Inicialmente, verifica o checksum.
 Se estiver correto, aciona a funcao que realiza o processamento
 propriamente dito, de acordo com o function code especificado
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
// void processMessage() {
//     int functionCode = decodeFunctionCode();
//     printf("[DEBUG] processMessage(): FunctionCode = 0x%02X\n", functionCode);
//     if (checkLRC()) {
//         switch (functionCode) {
//             case READ_REGISTER:
//                 processReadRegister();
//                 break;
//             case WRITE_REGISTER:
//                 processWriteRegister();
//                 break;
//             case WRITE_FILE:
//                 processWriteFile();
//                 break;
//             default:
//                 printf("[DEBUG] processMessage: FunctionCode inválido 0x%02X\n", functionCode);
//                 break;
//         }
//     } else {
//         printf("[DEBUG] Ignorando mensagem por LRC inválido\n");
//     }
//     _state = HUNTING_FOR_START_OF_MESSAGE;
// } // processMessage

void processMessage() {
    int functionCode = decodeFunctionCode();
    printf("[DEBUG] processMessage(): FunctionCode = 0x%02X\n", functionCode);
    // Verificando o LRC antes de processar a mensagem
    if (checkLRC()) {
        switch (functionCode) {
            case READ_REGISTER:
                processReadRegister();
                break;
            case WRITE_REGISTER:
                processWriteRegister();
                break;
            case WRITE_FILE:
                processWriteFile();
                break;
            default:
                printf("[DEBUG] processMessage: FunctionCode inválido 0x%02X\n", functionCode);
                printf("[PICO] ERRO: FunctionCode inválido 0x%02X\n", functionCode);
                break;
        }
    } else {
        printf("[DEBUG] Ignorando mensagem por LRC inválido\n");
        printf("[PICO] ERRO: Mensagem ignorada por LRC inválido\n");
    }
    _state = HUNTING_FOR_START_OF_MESSAGE;
} // processMessage

/************************************************************************
 receiveMessage
 Recebe uma mensagem, byte a byte. Notar que, para o multi-tasking
 cooperativo funcionar, cada funcao deve retornar o mais rapidamente possivel.
 Isso até nem seria necessário com o FreeRTOS, mas exemplifica a ideia de
 multitasking cooperativo.
 Assim, a recepção não fica em loop esperando terminar de receber toda a mensagem.
 A mensagem recebida vai sendo armazenada em rxBuffer; idxRxBuffer indica
 em que posição armazenar o caracter recebido. Ao verificar que a msg foi
 completada (recebendo 0x0D, 0x0A), sinaliza que a msg foi
 recebida fazendo _state = MESSAGE_READY.
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void receiveMessage() {
    char ch = MB_NO_CHAR;
    ch = getchar_timeout_us(0);
    if (ch != MB_NO_CHAR) {
        printf("[DEBUG] receiveMessage: leu char 0x%02X ('%c')\n", (uint8_t)ch, (ch >= 32 && ch <= 126) ? ch : '.');
        if (_state == HUNTING_FOR_START_OF_MESSAGE) {
            if (ch == ':') {
                idxRxBuffer = 0;
                rxBuffer[idxRxBuffer] = ch;
                _state = HUNTING_FOR_END_OF_MESSAGE;
                printf("[DEBUG] Encontrou ':' → estado = HUNTING_FOR_END_OF_MESSAGE\n");
            }
        } else if (_state == HUNTING_FOR_END_OF_MESSAGE) {
            idxRxBuffer++;
            if (idxRxBuffer >= MAX_RX_SIZE) {
                printf("[DEBUG] receiveMessage: buffer overflow, resetando estado\n");
                _state = HUNTING_FOR_START_OF_MESSAGE;
                idxRxBuffer = 0;
                return;
            }
            rxBuffer[idxRxBuffer] = ch;
            if (rxBuffer[idxRxBuffer] == 0x0A && rxBuffer[idxRxBuffer - 1] == 0x0D) {
                _state = MESSAGE_READY;
                printf("[DEBUG] find CR LF → estado = MESSAGE_READY (idxRxBuffer=%d)\n", idxRxBuffer);
            }
        }
    }
} // receiveMessage

/************************************************************************
 com_executeCommunication
 Recebeu uma requisicao ModBus e a processa
 Parametros de entrada:
    nenhum
 Retorno:
    nenhum
*************************************************************************/
void com_executeCommunication() {
    receiveMessage();
    if (_state == MESSAGE_READY) {
        printf("[DEBUG] com_executeCommunication(): Mensagem pronta para ser processada\n");
        processMessage();
    }
} // executeCommunication