/*
 * Exemplo completo: geração de trajetória com 30 pontos brutos
 * Adaptado para rodar em PIC16F (float, buffers estáticos, sem malloc)
 */

#include <stdint.h>
#include <stdbool.h>
#include "polinomio.h"
#include <stdio.h> 
#include <math.h>    // para fabsf() – muitas toolchains embedded fornecem
                     // essas funções em software; se não, escreva alternativas


// ---- Parâmetros fixos do robô ----  AQUI FAREMOS AS PRINCIPAIS MUDANCAS
static  float motor1_pos[2] = { 0.19f,   0.16f  }; // colocar um no menos e redfinir onde comeca nosso sistema de coordenadas???
static  float motor2_pos[2] = { -0.19f,  0.16f  };
static  float raio_eixo     = 0.02f;

// ---- Buffers estáticos ----
static float waypoints[MAX_WP][2];
static float hist_t[MAX_HIST_LEN];
tpr_DataTheta tpr_programTheta1[MAX_HIST_LEN];
// static float hist_phi1    [MAX_HIST_LEN];
// // static float hist_phi1_v  -[MAX_HIST_LEN];
// // static float hist_phi1_a  [MAX_HIST_LEN];
// static float hist_phi2    [MAX_HIST_LEN];
tpr_DataTheta tpr_programTheta2[MAX_HIST_LEN];
// static float hist_phi2_v  [MAX_HIST_LEN];
// static float hist_phi2_a  [MAX_HIST_LEN];
static float hist_x[MAX_HIST_LEN];
static float hist_y[MAX_HIST_LEN];

// Aproximação de sqrt (Babylonian)
static float sqrt_approx(float v) {
    if (v <= 0.0f) return 0.0f;
    float x = v;
    for (int i = 0; i < 4; i++)
        x = 0.5f * (x + v / x);
    return x;
}

// hipotenusa aproximada
static float hypot_approx(float dx, float dy) {
    return sqrt_approx(dx*dx + dy*dy);
}


void trajetoriaTheta(const float raw_pts[], int raw_count) {
    int num_raw = raw_count / 2;           // número de pares (x,y)
    int idx     = 0;                       // índice de saída
    const float scale = 0.001f;           
    
    // DEBUG: verifique o que está chegando
    printf("DEBUG antes do loop: raw_count=%d, num_raw=%d, MAX_HIST_LEN=%d\n",
           raw_count, num_raw, MAX_HIST_LEN);

    // --- 1) Ponto inicial ---
    float x0 = raw_pts[0] * scale;
    float y0 = raw_pts[1] * scale;

    motor1_pos[0] += x0;
    motor1_pos[1] += y0;
    motor2_pos[0] += x0;
    motor2_pos[1] += y0;

    float Lant1 = hypot_approx(x0 - motor1_pos[0],
                               y0 - motor1_pos[1]);
    float Lant2 = hypot_approx(x0 - motor2_pos[0],
                               y0 - motor2_pos[1]);

    // --- 2) passo de tempo uniforme ---
    float dt = (num_raw > 1) ? (TEMPO_TOTAL / (num_raw - 1)) : 0.0f;

    // DEBUG: mostre dt também
    printf("DEBUG dt calculado = %.6f\n", dt);

    for (int i = 0; i < num_raw && idx < MAX_HIST_LEN; i++) {
        // DEBUG: sinal de entrada no for
        printf(">> entrou no for com i=%d idx=%d\n", i, idx);

        if (2*i + 1 >= raw_count) {
            printf("!!! Índice inválido raw_pts[%d] (raw_count=%d)\n", 2*i+1, raw_count);
        break;
        }        

        // 2.1) escala do ponto bruto
        float xcurr = raw_pts[2*i]     * scale;
        float ycurr = raw_pts[2*i + 1] * scale;

        // printf("DEBUG idx=%d: x=%.4f y=%.4f\n",
        //        idx,
        //        xcurr, ycurr);

        // 2.2) vetores até cada motor
        float dx1 = xcurr - motor1_pos[0];
        float dy1 = ycurr - motor1_pos[1];
        float dx2 = xcurr - motor2_pos[0];
        float dy2 = ycurr - motor2_pos[1];

        printf("DEBUG teste dx\n");

        // 2.3) comprimentos atuais
        float Lcurr1 = hypot_approx(dx1, dy1);
        float Lcurr2 = hypot_approx(dx2, dy2);

        printf("DEBUG teste lcurr\n");

        // 2.4) variações
        float l1 = Lcurr1 - Lant1;
        float l2 = Lcurr2 - Lant2;

        // printf("DEBUG |L1=%.4f\n", Lcurr1);
        // printf("DEBUG |L2=%.4f \n", Lcurr2);
        // printf("DEBUG |lant1=%.4f \n",Lant1);
        // printf("DEBUG |lant2=%.4f\n", Lant2);
        // printf("DEBUG |delta1=%.4f \n",l1);
        // printf("DEBUG |delta2=%.4f\n", l2);

        // 2.5) atualiza referência
        Lant1 = Lcurr1;
        Lant2 = Lcurr2;

        // 2.6) ângulos
        float theta1 = -100*l1 / raio_eixo;
        float theta2 = 100*l2 / raio_eixo;
        tpr_programTheta1[idx].theta = theta1;
        tpr_programTheta2[idx].theta = theta2;

        // DEBUG: valores internos
        printf("DEBUG  TETHA1=%.4f TETHA2=%.4f\n", theta1, theta2);

        idx++;
    }

    // DEBUG: se nunca entrou, informe
    if (num_raw <= 0) {
        printf("DEBUG aviso: num_raw=%d, nenhum ponto para processar!\n", num_raw);
    } else if (idx == 0) {
        printf("DEBUG aviso: iterator entrou mas idx permaneceu 0 (talvez MAX_HIST_LEN=0?)\n");
    }

}

tpr_DataTheta tpr_getLineTheta1(int line) {
    if (line < 0 || line >= MAX_HIST_LEN) {
        tpr_DataTheta empty = {0};
        return empty;
    }
    return tpr_programTheta1[line];
} 

tpr_DataTheta tpr_getLineTheta2(int line) {
    if (line < 0 || line >= MAX_HIST_LEN) {
        tpr_DataTheta empty = {0};
        return empty;
    }
    return tpr_programTheta2[line];
} 
void tpr_initTheta(void) {
    int i;
    for (i = 0; i < MAX_HIST_LEN; i++) {
        tpr_programTheta1[i].theta = 0;
        tpr_programTheta2[i].theta = 0;
    }
} 