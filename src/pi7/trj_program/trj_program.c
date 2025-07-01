/*
 * Modulo: Programa Trajetoria
 * Armazena o programa da trajetoria a ser executada
 */


#include "trj_program.h"
#include "../polinomio_pc/polinomio.h"
#include <string.h>
#include <stdio.h>

// structure to store NC program
tpr_Data tpr_program[MAX_PROGRAM_LINES];

/*
 * * tpr_storeProgram:
 *   Recebe o "texto" no formato:
 *     "X:<valorX1>,Y:<valorY1>,Z:0;X:<valorX2>,Y:<valorY2>,Z:0;..."
 *   Cada bloco separado por ';' representa um ponto (X, Y).
 *   Armazena em tpr_program[] até MAX_PROGRAM_LINES.
 */

void tpr_storeProgram(char* texto) {
    char* p = texto;
    int idx = 0;

    printf("[DEBUG] tpr_storeProgram: início do processamento\n");

    while (*p != '\0' && idx < MAX_PROGRAM_LINES) {
        char* fimBloco = strchr(p, ';');

        if (fimBloco != NULL) {
            *fimBloco = '\0';  // termina string temporariamente
        }

        printf("[DEBUG] Analisando bloco: \"%s\"\n", p);

        int x_val = 0, y_val = 0;
        int lidos = sscanf(p, "X:%d,Y:%d;", &x_val, &y_val);
        printf("[DEBUG] sscanf → lidos=%d, x=%d, y=%d\n", lidos, x_val, y_val);

        if (lidos >= 2) {
            tpr_program[idx].x = x_val;
            tpr_program[idx].y = y_val;
            printf("[DEBUG] Armazenado em tpr_program[%d] = {x=%d, y=%d}\n", idx, x_val, y_val);
            idx++;
        } else {
            printf("[ERRO] sscanf falhou para bloco \"%s\"\n", p);
        }

        if (fimBloco == NULL) {
            break;
        }

        p = fimBloco + 1;
    }

    printf("[DEBUG] tpr_storeProgram: fim do processamento, total armazenado = %d\n", idx);

    float raw_pts[2 * MAX_PROGRAM_LINES];
    for (int i = 0; i < idx; i++) {
        raw_pts[2*i] = (tpr_program[i].x)/100;
        raw_pts[2*i+1] = (tpr_program[i].y)/100;
    }

    trajetoriaTheta(raw_pts, 2 * idx); //chama funcao do polinomio que transforma lista de pontos em 2 listas de angulos, 1 para cada motor
}



/**
 * tpr_getLine:
 *   Retorna a estrutura tpr_program[line], para consulta externa.
 */
tpr_Data tpr_getLine(int line) {
    if (line < 0 || line >= MAX_PROGRAM_LINES) {
        tpr_Data empty = {0, 0};
        return empty;
    }
    return tpr_program[line];
} // tpr_getLine

void tpr_init(void) {
    int i;
    for (i = 0; i < MAX_PROGRAM_LINES; i++) {
        tpr_program[i].x = 0;
        tpr_program[i].y = 0;
    }
} // tpr_init