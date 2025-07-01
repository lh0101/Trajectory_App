#ifndef __polinomio_h
#define __polinomio_h

// ---- Parâmetros de configuração ----
#define MAX_PROGRAM_LINES 200   
#define N_INTERMEDIARIOS    1      // subdivisões entre cada par de pontos
#define TEMPO_TOTAL       0.5f    // tempo total de toda a trajetória (mudei de 1.0f para 0.5f)
#define PTS_PER_SEG       20      // amostras por segmento

// ---- Cálculo dos tamanhos máximos ----
#define MAX_WP       ((MAX_PROGRAM_LINES - 1) * (N_INTERMEDIARIOS + 1))
// #define MAX_HIST_LEN ((MAX_WP - 1) * PTS_PER_SEG)
#define MAX_HIST_LEN 3000


typedef struct {
	float theta;
} tpr_DataTheta;

extern tpr_DataTheta tpr_programTheta1[MAX_HIST_LEN]; 
extern tpr_DataTheta tpr_programTheta2[MAX_HIST_LEN]; 


extern tpr_DataTheta tpr_getLineTheta1(int line);
extern tpr_DataTheta tpr_getLineTheta2(int line);
extern void tpr_initTheta();
extern void trajetoriaTheta(const float raw_pts[], int raw_count);

#endif