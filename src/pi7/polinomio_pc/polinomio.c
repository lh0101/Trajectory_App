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


// ---- Parâmetros fixos do robô ----
static const float motor1_pos[2] = { 0.0f,   0.285f  };
static const float motor2_pos[2] = { 0.038f, 0.285f  };
static const float raio_eixo     = 0.015f;

// ---- Buffers estáticos ----
static float waypoints[MAX_WP][2];
static float hist_t[MAX_HIST_LEN];
tpr_DataTheta tpr_programTheta1[MAX_HIST_LEN];
// static float hist_phi1    [MAX_HIST_LEN];
// // static float hist_phi1_v  [MAX_HIST_LEN];
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

// resolve sistema 3×3 (float)
static int solve3(float A[3][3], float b[3], float x[3]) {
    float M[3][4];
    for (int i = 0; i < 3; i++) {
        M[i][0] = A[i][0];
        M[i][1] = A[i][1];
        M[i][2] = A[i][2];
        M[i][3] = b[i];
    }
    for (int i = 0; i < 3; i++) {
        int maxR = i;
        for (int k = i+1; k < 3; k++)
            if (fabsf(M[k][i]) > fabsf(M[maxR][i]))
                maxR = k;
        if (fabsf(M[maxR][i]) < 1e-6f) return -1;
        if (maxR != i) {
            for (int j = i; j < 4; j++) {
                float t = M[i][j];
                M[i][j] = M[maxR][j];
                M[maxR][j] = t;
            }
        }
        float div = M[i][i];
        for (int j = i; j < 4; j++)
            M[i][j] /= div;
        for (int k = i+1; k < 3; k++) {
            float f = M[k][i];
            for (int j = i; j < 4; j++)
                M[k][j] -= f * M[i][j];
        }
    }
    for (int i = 2; i >= 0; i--) {
        float s = M[i][3];
        for (int j = i+1; j < 3; j++)
            s -= M[i][j] * x[j];
        x[i] = s;
    }
    return 0;
}

// coef. de polinômio quintico
static void calcular_coef_quintico(float pi, float pf, float T, float c[6]) {
    if (T <= 1e-6f) {
        c[0] = pi;
        for (int i = 1; i < 6; i++) c[i] = 0.0f;
        return;
    }
    c[0] = pi;  c[1] = c[2] = 0.0f;
    float ds = pf - pi;
    float T2 = T*T, T3 = T2*T, T4 = T3*T, T5 = T4*T;
    float A[3][3] = {
        { T3,   T4,    T5 },
        { 3*T2, 4*T3,  5*T4 },
        { 6*T,  12*T2, 20*T3 }
    };
    float b[3] = { ds, 0.0f, 0.0f };
    float x[3];
    if (solve3(A, b, x) == 0) {
        c[3] = x[0];
        c[4] = x[1];
        c[5] = x[2];
    } else {
        if (fabsf(ds) < 1e-6f) {
            c[3] = c[4] = c[5] = 0.0f;
        } else {
            c[1] = ds/T;
            c[2] = c[3] = c[4] = c[5] = 0.0f;
        }
    }
}

// avalia quintico: posição, vel., acel.
static void avaliar_quintico(const float c[6], float t,
                             float *pos, float *vel, float *acc) {
    float t2 = t*t, t3 = t2*t, t4 = t3*t, t5 = t4*t;
    *pos = c[0] + c[1]*t + c[2]*t2 + c[3]*t3 + c[4]*t4 + c[5]*t5;
    *vel =      c[1] + 2*c[2]*t + 3*c[3]*t2 + 4*c[4]*t3 + 5*c[5]*t4;
    *acc =         2*c[2] + 6*c[3]*t +12*c[4]*t2 +20*c[5]*t3;
}

// cinematica direta de cabos
static void cinematica_direta_cabos(float L1, float L2,
                                    const float m1[2], const float m2[2],
                                    float *xp, float *yp) {
    float dx = m2[0] - m1[0], dy = m2[1] - m1[1];
    float d  = hypot_approx(dx, dy);
    if (d > L1+L2 || d < fabsf(L1-L2)) {
        *xp = *yp = 0;
        return;
    }
    float a = (L1*L1 - L2*L2 + d*d)/(2*d);
    float h2 = L1*L1 - a*a;
    float h  = (h2>0?sqrt_approx(h2):0);
    float xm = m1[0] + a*dx/d;
    float ym = m1[1] + a*dy/d;
    float rx =  dy*(h/d);
    float ry =  dx*(h/d);
    // escolhe y menor
    if (ym-rx < ym+rx) {
        *xp = xm + ry;
        *yp = ym - rx;
    } else {
        *xp = xm - ry;
        *yp = ym + rx;
    }
}

void trajetoriaTheta(const float raw_pts[], int raw_count) {
    printf("[DEBUG] trajetoriaTheta: início com %d valores brutos\n", raw_count);

    int num_raw = raw_count/2;
    int wp = 0;

    for (int i = 0; i < num_raw-1 && wp < MAX_WP; i++) {
        float x0 = raw_pts[2*i]   *0.0001f;
        float y0 = raw_pts[2*i+1] *0.0001f;
        float x1 = raw_pts[2*i+2] *0.0001f;
        float y1 = raw_pts[2*i+3] *0.0001f;

        printf("[DEBUG] Interpolando entre ponto %d e %d: (%.4f, %.4f) → (%.4f, %.4f)\n", i, i+1, x0, y0, x1, y1);

        int start = (i==0 ? 0 : 1);
        for (int j = start; j <= N_INTERMEDIARIOS && wp < MAX_WP; j++) {
            float t = (float)j / N_INTERMEDIARIOS;
            waypoints[wp][0] = x0 + (x1 - x0) * t;
            waypoints[wp][1] = y0 + (y1 - y0) * t;
            printf("[DEBUG]   waypoint[%d] = (%.4f, %.4f)\n", wp, waypoints[wp][0], waypoints[wp][1]);
            wp++;
        }
    }

    printf("[DEBUG] Total de waypoints gerados: %d\n", wp);

    int n_seg = wp - 1;
    float t_seg = TEMPO_TOTAL / n_seg;
    int idx = 0;

    for (int i = 0; i < n_seg && idx < MAX_HIST_LEN; i++) {
        float p0x = waypoints[i][0], p0y = waypoints[i][1];
        float p1x = waypoints[i+1][0], p1y = waypoints[i+1][1];

        float L10 = hypot_approx(p0x - motor1_pos[0], p0y - motor1_pos[1]);
        float L20 = hypot_approx(p0x - motor2_pos[0], p0y - motor2_pos[1]);
        float L11 = hypot_approx(p1x - motor1_pos[0], p1y - motor1_pos[1]);
        float L21 = hypot_approx(p1x - motor2_pos[0], p1y - motor2_pos[1]);

        float cL1[6], cL2[6];
        calcular_coef_quintico(L10, L11, t_seg, cL1);
        calcular_coef_quintico(L20, L21, t_seg, cL2);

        for (int j = 0; j < PTS_PER_SEG && idx < MAX_HIST_LEN; j++) {
            float tt = t_seg * j / (PTS_PER_SEG-1);
            hist_t[idx] = (i * t_seg) + tt;
            float l1, v1, a1, l2, v2, a2;
            avaliar_quintico(cL1, tt, &l1, &v1, &a1);
            avaliar_quintico(cL2, tt, &l2, &v2, &a2);
            tpr_programTheta1[idx].theta = l1 / raio_eixo;
            tpr_programTheta2[idx].theta = l2 / raio_eixo;

            printf("[DEBUG]   ponto %d: t=%.3f θ1=%.3f θ2=%.3f\n", idx, hist_t[idx], tpr_programTheta1[idx].theta, tpr_programTheta2[idx].theta);

            float xp, yp;
            cinematica_direta_cabos(l1, l2, motor1_pos, motor2_pos, &xp, &yp);
            hist_x[idx] = xp;
            hist_y[idx] = yp;
            idx++;
        }
    }

    printf("[DEBUG] trajetoriaTheta: total de pontos gerados = %d\n", idx);
}

/**
 * tpr_getLineTheta:
 *   Retorna a estrutura tpr_program[line], para consulta externa.
 */
tpr_DataTheta tpr_getLineTheta1(int line) {
    if (line < 0 || line >= MAX_HIST_LEN) {
        tpr_DataTheta empty = {0};
        return empty;
    }
    return tpr_programTheta1[line];
} // tpr_getLine

tpr_DataTheta tpr_getLineTheta2(int line) {
    if (line < 0 || line >= MAX_HIST_LEN) {
        tpr_DataTheta empty = {0};
        return empty;
    }
    return tpr_programTheta2[line];
} // tpr_getLine


/**
 * tpr_init:
 *   Inicializa toda a matriz tpr_program[] a zeros.
 */
void tpr_initTheta(void) {
    int i;
    for (i = 0; i < MAX_HIST_LEN; i++) {
        tpr_programTheta1[i].theta = 0;
        tpr_programTheta2[i].theta = 0;
    }
} // tpr_init

// // --------------------------------------------------------------------------------
// // main(): exemplo de uso
// // --------------------------------------------------------------------------------
// int main(void) {
//     // Preenche raw_pts dinamicamente para ter 30 pontos
//     static float raw_pts[RAW_PTS_COUNT];
//     for (int i = 0; i < RAW_PTS_COUNT/2; i++) {
//         raw_pts[2*i]   = i * 500.0f;              // x = 0, 500, 1000, ...
//         raw_pts[2*i+1] = (29 - i) * 500.0f;       // y = 14500, 14000, ...
//     }

//     int raw_count = RAW_PTS_COUNT;  // número de valores em raw_pts
//     int out_len;

//     // Gera a trajetória
//     trajetoria(raw_pts, raw_count, &out_len);

//     // Agora out_len diz quantos pontos há em hist_phi1 / hist_phi2
//     for (int i = 0; i < out_len; i++) {
//         // Aqui você pode:
//         // - Mapear hist_phi1[i] / hist_phi2[i] para DAC/PWM
//         // - Enviar via comunicação serial para debug
//         // - Etc.
//         // Exemplo de debug (supondo printf disponível):
//         // printf("t=%.3f φ1=%.3f φ2=%.3f\n",
//         //        hist_t[i], hist_phi1[i], hist_phi2[i]);
//         ;
//     }

//     while (1) {
//         // loop infinito típico de firmware
//     }

//     return 0;
// }
