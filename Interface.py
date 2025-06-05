import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from antlr4 import InputStream, CommonTokenStream
from GCodeLexer import GCodeLexer
from GCodeParser import GCodeParser
from GCodeInterpreter import GCodeInterpreter
from antlr4.tree.Tree import ParseTreeWalker
import numpy as np

trajectory_x = []
trajectory_y = []
expected_x = []
expected_y = []
simulated_position = {'x': 0.0, 'y': 0.0, 'linha': 0}

def write_register(register, value):
    print(f"[MODBUS] Escrever reg {register} com valor {value}")

def start_program():
    write_register(0, 1)

def suspend_program():
    write_register(1, 1)

def continue_program():
    write_register(2, 1)

def abort_program():
    write_register(3, 1)

def jog_x(direction):
    try:
        step = float(entry_step.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido para o passo.")
        return
    write_register(6, step)
    write_register(4, -1 if direction == 'left' else 1)
    simulated_position['x'] += -step if direction == 'left' else step
    update_position_display()

def jog_y(direction):
    try:
        step = float(entry_step.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido para o passo.")
        return
    write_register(7, step)
    write_register(5, -1 if direction == 'down' else 1)
    simulated_position['y'] += step if direction == 'up' else -step
    update_position_display()

def update_position_display():
    x = simulated_position['x']
    y = simulated_position['y']
    linha = simulated_position['linha']
    lbl_x_val.config(text=f"{x:.2f}")
    lbl_y_val.config(text=f"{y:.2f}")
    lbl_linha_val.config(text=f"{linha}")
    trajectory_x.append(x)
    trajectory_y.append(y)
    plot_trajectory()

def reset_drawing():
    global trajectory_x, trajectory_y
    trajectory_x = []
    trajectory_y = []
    plot_trajectory()

def plot_trajectory():
    ax1.clear()
    ax1.plot(trajectory_x, trajectory_y, marker='o', color='blue')
    ax1.set_title("Trajetória Manual (X vs Y)")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.grid(True)
    canvas1.draw()

def plot_expected_trajectory():
    ax2.clear()
    ax2.plot(expected_x, expected_y, marker='x', color='green')
    ax2.set_title("Trajetória G-Code Esperada")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.grid(True)
    canvas2.draw()

def interpretar_gcode():
    global expected_x, expected_y
    code = gcode_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Aviso", "Insira algum código G para interpretar.")
        return
    try:
        input_stream = InputStream(code)
        lexer = GCodeLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = GCodeParser(token_stream)
        tree = parser.program()
        interpreter = GCodeInterpreter(circ_interpol_steps=50, linear_interpol_steps=20, name="traj")
        walker = ParseTreeWalker()
        walker.walk(interpreter, tree)
        expected_x = interpreter.move_sequence['x']
        expected_y = interpreter.move_sequence['y']
        plot_expected_trajectory()
    except Exception as e:
        messagebox.showerror("Erro na interpretação", str(e))

# Interface
root = tk.Tk()
root.title("Interface PI-7")

intro = tk.Label(root, text=(
    "Controles:\n"
    "- Teclas de seta movimentam o robô (← → ↑ ↓)\n"
    "- Botões executam comandos de controle do programa\n"
    "- Campo 'Passo' define a distância dos movimentos Jog (usar ponto '.' como separador decimal)\n"
    "\n"
    "Modos de Operação:\n"
    "1. Modo Manual: use botões e setas para mover o sistema\n"
    "2. Modo Código G: escreva um código G e visualize a trajetória resultante\n"
    "\n"
    "Instruções G-Code disponíveis:\n"
    "- G00 X__ Y__: movimento rápido até X,Y\n"
    "- G01 X__ Y__: interpolação linear até X,Y\n"
    "- G02/G03 X__ Y__ I__ J__: interpolação circular até X,Y com centro em (Xc, Yc),\n"
    "  definido por I = Xc - X_ini, J = Yc - Y_ini\n"
    "- G04 P__: espera de P milissegundos\n"
), justify="left", font=("Arial", 10), anchor='w')
intro.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='w')

frame_cmd = tk.Frame(root)
frame_cmd.grid(row=1, column=0, padx=20, pady=10, sticky='nw')
tk.Button(frame_cmd, text="Iniciar", width=12, command=start_program).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_cmd, text="Suspender", width=12, command=suspend_program).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_cmd, text="Continuar", width=12, command=continue_program).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_cmd, text="Abortar", width=12, command=abort_program).grid(row=1, column=1, padx=5, pady=5)

frame_jog = tk.Frame(root)
frame_jog.grid(row=2, column=0, padx=20, pady=10, sticky='nw')
tk.Label(frame_jog, text="Passo:").grid(row=0, column=0)
entry_step = tk.Entry(frame_jog, width=6)
entry_step.insert(0, "1")
entry_step.grid(row=0, column=1)
tk.Button(frame_jog, text="↑", width=5, command=lambda: jog_y('up')).grid(row=1, column=1, pady=2)
tk.Button(frame_jog, text="←", width=5, command=lambda: jog_x('left')).grid(row=2, column=0, pady=2)
tk.Button(frame_jog, text="→", width=5, command=lambda: jog_x('right')).grid(row=2, column=2, pady=2)
tk.Button(frame_jog, text="↓", width=5, command=lambda: jog_y('down')).grid(row=3, column=1, pady=2)

frame_pos = tk.Frame(root)
frame_pos.grid(row=3, column=0, padx=20, pady=10, sticky='nw')
tk.Label(frame_pos, text="Posição X:").grid(row=0, column=0)
lbl_x_val = tk.Label(frame_pos, text="--")
lbl_x_val.grid(row=0, column=1)
tk.Label(frame_pos, text="Posição Y:").grid(row=1, column=0)
lbl_y_val = tk.Label(frame_pos, text="--")
lbl_y_val.grid(row=1, column=1)
tk.Label(frame_pos, text="Linha Atual:").grid(row=2, column=0)
lbl_linha_val = tk.Label(frame_pos, text="--")
lbl_linha_val.grid(row=2, column=1)

fig1 = Figure(figsize=(4, 4))
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().grid(row=1, column=1, rowspan=3, padx=10, pady=10)
tk.Button(root, text="Reset Trajetória Manual", command=reset_drawing).grid(row=4, column=1, pady=5)

# SEÇÃO CÓDIGO G
frame_gcode = tk.Frame(root)
frame_gcode.grid(row=0, column=2, padx=10, pady=10, sticky='nw')
tk.Label(frame_gcode, text="Código G:").pack(anchor='w')
gcode_input = scrolledtext.ScrolledText(frame_gcode, width=50, height=10)
gcode_input.pack()
tk.Button(frame_gcode, text="Interpretar Código G", command=interpretar_gcode).pack(pady=5)

fig2 = Figure(figsize=(4, 4))
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().grid(row=1, column=2, rowspan=3, padx=10, pady=10)

# Binds
root.bind('<Left>', lambda e: jog_x('left'))
root.bind('<Right>', lambda e: jog_x('right'))
root.bind('<Up>', lambda e: jog_y('up'))
root.bind('<Down>', lambda e: jog_y('down'))

root.mainloop()
