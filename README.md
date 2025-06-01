# Projeto PI-7 - Subgrupo de Trajetória e Programação

Este repositório contém os códigos, gramática ANTLR e interpretador relacionados ao **subgrupo de Trajetória** do projeto **PI-7 (PMR3420 - Projeto Integrado 7)** da Escola Politécnica da USP.

## 📌 Visão Geral

O projeto PI-7 propõe o desenvolvimento de uma máquina com **dois eixos com controle de trajetória em tempo real**, baseada em arquivos de entrada no formato **G-code**. O sistema completo é composto por:

- Interpretador de G-code no PC (Python + ANTLR)
- Gerador de trajetória no Raspberry Pi Pico W (FreeRTOS em C)
- Controle PID em tempo real no microcontrolador PIC
- Mecanismo físico com motores e encoders

## 🔧 Estrutura deste Subgrupo

Este repositório trata das **etapas iniciais do processamento do G-code**:

- Definição da gramática do G-code (`GCode.g4`)
- Geração de Lexer e Parser via ANTLR
- Implementação do interpretador e visualizador de trajetória (`GCodeInterpreter.py`)
- Exportação da trajetória em coordenadas (`x`, `y`) para posterior envio ao Raspberry Pi via protocolo MODBUS

## 📂 Arquivos principais

- `GCode.g4`: Gramática ANTLR para interpretação de comandos G-code (G00 a G04, M30)
- `GCodeInterpreter.py`: Interpretador que realiza interpolação linear e circular, além de preview e exportação da trajetória
- `main.py`: Script de entrada para execução do parser e do interpretador
- `programa.gcode`: Exemplo de arquivo G-code para testes

## ✅ Comandos G implementados

| Comando | Ação                                 | Parâmetros esperados               |
|---------|--------------------------------------|------------------------------------|
| `G00`   | Movimento rápido (posição absoluta)  | `X`, `Y`                           |
| `G01`   | Interpolação linear                  | `X`, `Y`                           |
| `G02`   | Interpolação circular CW             | `X`, `Y`, `I`, `J`                 |
| `G03`   | Interpolação circular CCW            | `X`, `Y`, `I`, `J`                 |
| `G04`   | Pausa (delay)                        | `P` (tempo em milissegundos)      |
| `M30`   | Fim do programa                      | -                                  |

### 🧭 Significado dos parâmetros

- `X`, `Y`: coordenadas finais do movimento
- `I`, `J`: deslocamento até o centro do arco (coordenadas relativas ao ponto inicial)
- `P`: tempo de espera em milissegundos (usado em `G04`)

## 🧰 Requisitos

- Python 3.10+
- ANTLR 4.13.2
- Pacotes Python:
  - `antlr4-python3-runtime`
  - `numpy`
  - `matplotlib`

## ⚙️ Como executar

1. Gere os arquivos do ANTLR:

```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 GCode.g4
```

2. Execute o interpretador:

```bash
python main.py
```

3. A execução:

- Interpreta o G-code
- Gera um gráfico de preview da trajetória
- Cria um arquivo `.gif` com a trajetória animada

## 📈 Exemplo de saída

- Preview gráfico: Trajetória em `x` e `y`
- Arquivo `.gif` salvo automaticamente ao final da execução (`Trajetória.gif` por padrão)

## 🔄 Próximas Etapas

- [ ] Implementar protocolo MODBUS para envio ao Raspberry Pi Pico W
- [ ] Traduzir trajetória em `x`, `y` para tamanhos de cordas (modelo mecânico)
- [ ] Gerar comandos PWM a partir da sequência de posições
- [ ] Integrar com o gerador de trajetória em FreeRTOS (Raspberry Pi)

## 📚 Referências

- Apostila ANTLR 2025 — Prof. Jun Okamoto Jr.
- Apostila MODBUS 2025 — Prof. Jun Okamoto Jr.
- [ANTLR - Site Oficial](https://www.antlr.org/)
- [Tutorial ANTLR com Python](https://yetanotherprogrammingblog.medium.com/antlr-with-python-974c756bdb1b)

---

Desenvolvido como parte do curso **PMR3420 - Projeto Integrado 7** – Escola Politécnica da Universidade de São Paulo (2025).
