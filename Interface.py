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
import serial
import threading
import time # Adicionado para delays

# =============================
# MODBUS - Envio de programa via COM5 (Raspberry Pi Pico)
# =============================
ser = None # Inicializa ser como None
try:
    ser = serial.Serial(
        port='COM5', # Verifique a porta COM do seu Pico W
        baudrate=115200, # Baudrate padrão
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.1 # Timeout curto para não bloquear muito o readline()
    )
    if not ser.is_open:
        ser.open()
    print("Porta serial aberta com sucesso.")
except serial.SerialException as e:
    messagebox.showerror("Erro de Serial", f"Não foi possível abrir a porta serial: {e}\nVerifique se o Pico W está conectado e a porta está correta.")
    ser = None # Definir ser como None para evitar erros posteriores

def calc_lrc(byte_list):
    """
    Calculates the LRC for Modbus ASCII:
    sums all binary bytes (0x00..0xFF value),
    takes (0xFF - (sum & 0xFF)) + 1, and returns (0..0xFF).
    NOTE: This function expects a list of *ASCII ordinal values* of hexadecimal characters,
    not decoded binary values, to match the Pico W implementation.
    """
    accum = 0
    for b in byte_list:
        accum = (accum + b) & 0xFF
    accum = ((0xFF - accum) + 1) & 0xFF
    return accum

def byte_to_hex2(b):
    """
    Converts an integer 0..255 to two ASCII hex characters (uppercase).
    Ex: 13 -> '0D', 255 -> 'FF'
    """
    return "{:02X}".format(b)

def build_write_register_frame(register, value):
    """
    Builds a Modbus ASCII message for:
    WRITE SINGLE REGISTER (FC = 0x06)
    → : [Slave=0x01][FC=06][RegHi][RegLo][ValHi][ValLo][LRC][CRLF]
    `register` and `value` are integers 0..0xFFFF.
    Returns the complete ASCII string.
    """
    slave = 0x01
    fc = 0x06
    
    # Formats components as hexadecimal strings
    slave_str = byte_to_hex2(slave)
    fc_str = byte_to_hex2(fc)
    
    # User's original logic for reg and val (8-bit as per Modbus.c)
    reg = byte_to_hex2(register & 0xFF)
    val = byte_to_hex2(value & 0xFF)

    # Concatenates the part of the message used for LRC calculation (without the ':')
    lrc_data_str = slave_str + fc_str + reg + val
    
    # Converts each character of the data string to its ASCII ordinal value for LRC calculation
    byte_list_for_lrc = [ord(c) for c in lrc_data_str]
    lrc = calc_lrc(byte_list_for_lrc)

    # Builds the final frame
    frame = ":"
    frame += lrc_data_str # Adds the data part (already in ASCII hex)
    frame += byte_to_hex2(lrc) # Adds the LRC in ASCII hex
    frame += "\r\n"
    return frame

def build_write_file_frame(values):
    """
    Builds a Modbus ASCII message for WRITE FILE (FC = 0x15).
    The structure expected by modbus.c processWriteFile is:
    :[Slave][FC][RecordLength_H1][RecordLength_L1][RecordLength_H2][RecordLength_L2][Data...][LRC][CRLF]
    RecordLength is the number of elements in 'values'. Each element of 'values' is a 16-bit register.
    """
    slave = 0x01
    fc = 0x15
    
    rec_len = len(values) # RecordLength is the number of registers (each value in 'values')
    
    # Formats components as hexadecimal strings
    slave_str = byte_to_hex2(slave)
    fc_str = byte_to_hex2(fc)
    
    rec_len_hi_str = byte_to_hex2((rec_len >> 8) & 0xFF)
    rec_len_lo_str = byte_to_hex2(rec_len & 0xFF)

    data_values_str = ""
    for v in values:
        hi = (v >> 8) & 0xFF
        lo = v & 0xFF
        data_values_str += byte_to_hex2(hi)
        data_values_str += byte_to_hex2(lo)

    # Concatenates the part of the message used for LRC calculation (without the ':')
    lrc_data_str = slave_str + fc_str + \
                   rec_len_hi_str + rec_len_lo_str + \
                   data_values_str
    
    # Converts each character of the data string to its ASCII ordinal value for LRC calculation
    byte_list_for_lrc = [ord(c) for c in lrc_data_str]
    lrc = calc_lrc(byte_list_for_lrc)

    # Builds the final frame
    frame = ":"
    frame += lrc_data_str # Adds the data part (already in ASCII hex)
    frame += byte_to_hex2(lrc) # Adds the LRC in ASCII hex
    frame += "\r\n"
    return frame

def send_modbus_frame(frame):
    if ser and ser.is_open:
        try:
            print(f"Enviando: {frame.strip()}")
            ser.write(frame.encode('ascii'))
            time.sleep(0.05) # Small delay to ensure message is sent
        except serial.SerialException as e:
            messagebox.showerror("Communication Error", f"Error sending data over serial: {e}")
            log_output.insert(tk.END, f"Communication Error: {e}\n")
            log_output.see(tk.END)
    else:
        messagebox.showwarning("Serial Port Not Open", "Serial port is not open or not initialized.")
        log_output.insert(tk.END, "Error: Serial port not open.\n")
        log_output.see(tk.END)

# `write_register` is kept as it's used to start the program after sending file.
def write_register(register, value):
    """
    Writes a single register via MODBUS (Function Code 0x06),
    sending ASCII frames directly over serial.
    """
    frame = build_write_register_frame(register, value)
    send_modbus_frame(frame)

def write_file_all(values):
    """
    Sends a single Modbus ASCII Write File (FC=0x15) message,
    containing all consecutive registers.
    """
    frame = build_write_file_frame(values)
    send_modbus_frame(frame)

def _envia_programa_em_background(xs, ys):
    """
    Sends the trajectory (xs, ys) via “WRITE FILE” (FC=0x15).
    Each point (X, Y) occupies 2 consecutive registers.
    Z is always 0, so it's not sent as a separate register from G-Code.
    modbus.c expects X,Y pairs.
    Executes in a separate thread to avoid freezing Tkinter.
    """
    total_points = len(xs)

    values = []
    for i in range(total_points):
        x_fixed = int(round(xs[i] * 100))
        y_fixed = int(round(ys[i] * 100))
        values.append(x_fixed & 0xFFFF)
        values.append(y_fixed & 0xFFFF)
    
    write_file_all(values) 
    print("All points sent via WRITE FILE.")

    root.after(100, lambda: btn_enviar_modbus.config(state='normal')) # Re-enables the button after sending

def on_click_enviar():
    """
    Callback for the "Send via MODBUS" button. Disables the button and starts the thread.
    """
    if not ser or not ser.is_open:
        messagebox.showwarning("Serial Error", "Serial port is not open. Cannot send program.")
        return

    if not expected_x or not expected_y:
        messagebox.showwarning("Warning", "No G-Code trajectory interpreted to send.")
        return

    btn_enviar_modbus.config(state='disabled')
    t = threading.Thread(
        target=_envia_programa_em_background,
        args=(expected_x, expected_y),
        daemon=True
    )
    t.start()

# =============================
# Interface Variables and Trajectory (Restored)
# =============================
trajectory_x = [] 
trajectory_y = [] 
expected_x = []
expected_y = []
expected_z = [] 

simulated_position = {'x': 0.0, 'y': 0.0, 'linha': 0}

# Register mapping (Restored)
REG_INICIAR = 1
REG_SUSPENDER = 2
REG_CONTINUAR = 3
REG_ABORTAR = 4
REG_JOGX = 5
REG_JOGY = 6
REG_PASSOX = 7
REG_PASSOY = 8
REG_X = 9
REG_Y = 10
REG_LINHA = 11
REG_PROGRAMA_START = 12

# Global Figure and Axes initialization (MOVED HERE to avoid NameError)
fig1 = Figure(figsize=(5.5, 4.0), dpi=100) 
ax1 = fig1.add_subplot(111)

fig2 = Figure(figsize=(5.5, 4.0), dpi=100) 
ax2 = fig2.add_subplot(111)

# Global Canvas variables (ADDED HERE to avoid NameError)
canvas1 = None
canvas2 = None

def start_program():
    write_register(REG_INICIAR, 1)

def suspend_program():
    write_register(REG_SUSPENDER, 1)

def continue_program():
    write_register(REG_CONTINUAR, 1)

def abort_program():
    write_register(REG_ABORTAR, 1)

def jog_x(direction):
    try:
        step = float(entry_step.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido para o passo.")
        return
    
    write_register(REG_PASSOX, int(round(step * 100))) 
    write_register(REG_JOGX, 0xFFFF if direction == 'left' else 1)
    
    simulated_position['x'] += -step if direction == 'left' else step
    update_position_display()

def jog_y(direction):
    try:
        step = float(entry_step.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira um número válido para o passo.")
        return

    write_register(REG_PASSOY, int(round(step * 100)))
    write_register(REG_JOGY, 0xFFFF if direction == 'down' else 1)
    
    simulated_position['y'] += step if direction == 'up' else -step
    update_position_display()

def update_position_display():
    x = simulated_position['x']
    y = simulated_position['y']
    linha = simulated_position['linha']
    lbl_x_val.config(text=f"{x:.2f}")
    lbl_y_val.config(text=f"{y:.2f}")
    lbl_linha_val.config(text=f"{linha}")
    
    # FIX: Ensure trajectory points are added and plot is updated for Jog movements
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
    ax1.plot(trajectory_x, trajectory_y, marker='o', color='white') # Line color
    ax1.set_title("Trajetória Manual (X vs Y)", color='white') # Title color
    ax1.set_xlabel("X (unidades)", color='white') # X-axis label color
    ax1.set_ylabel("Y (unidades)", color='white') # Y-axis label color
    ax1.tick_params(axis='x', colors='white') # X-axis tick color
    ax1.tick_params(axis='y', colors='white') # Y-axis tick color
    ax1.set_facecolor("#34495E") # Plot background color
    fig1.set_facecolor("#2C3E50") # Figure background color
    ax1.grid(True, color='gray', linestyle='--') # Grid color
    ax1.set_aspect('equal', adjustable='box') # Keep plot square

    # Adicione estas duas linhas para travar o tamanho do gráfico:
    ax1.set_xlim(-5, 5)  # Defina os limites mínimos e máximos para o eixo X
    ax1.set_ylim(-5, 5)  # Defina os limites mínimos e máximos para o eixo Y
    
    # FIX: Ensure canvas1 is available and draw it
    if canvas1:
        canvas1.draw()

def plot_expected_trajectory():
    ax2.clear()
    ax2.plot(expected_x, expected_y, marker='x', color='yellow') # Line color
    ax2.set_title("Trajetória G-Code Esperada", color='white') # Title color
    ax2.set_xlabel("X (unidades)", color='white') # X-axis label color
    ax2.set_ylabel("Y (unidades)", color='white') # Y-axis label color
    ax2.tick_params(axis='x', colors='white') # X-axis tick color
    ax2.tick_params(axis='y', colors='white') # Y-axis tick color
    ax2.set_facecolor("#34495E") # Plot background color
    fig2.set_facecolor("#2C3E50") # Figure background color
    ax2.grid(True, color='gray', linestyle='--') # Grid color
    ax2.set_aspect('equal', adjustable='box') # Keep plot square
    # FIX: Ensure canvas2 is available and draw it
    if canvas2:
        canvas2.draw() 

def interpretar_gcode():
    """
    Reads text from the scrolledtext widget, interprets it via ANTLR,
    fills expected_x, expected_y, and expected_z,
    and draws the expected trajectory on the second graph.
    """
    global expected_x, expected_y, expected_z
    code = gcode_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Warning", "Enter some G-code to interpret.")
        return
    try:
        input_stream = InputStream(code)
        lexer = GCodeLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = GCodeParser(token_stream)
        tree = parser.program()
        interpreter = GCodeInterpreter(circ_interpol_steps=20, linear_interpol_steps=10, name="traj")
        walker = ParseTreeWalker()
        walker.walk(interpreter, tree)

        expected_x = interpreter.move_sequence['x']
        expected_y = interpreter.move_sequence['y']
        expected_z = [0] * len(expected_x) 

        plot_expected_trajectory()
        messagebox.showinfo("Success", "G-Code interpreted successfully!")
    except Exception as e:
        messagebox.showerror("Interpretation Error", str(e))

# =============================
# Serial Listener Thread (Lógica do log revertida)
# =============================
stop_serial_thread = False

def serial_reader_thread():
    """
    Reads from the serial port continuously and processes messages.
    """
    while not stop_serial_thread and ser and ser.is_open:
        try:
            line = ser.readline().decode('ascii').strip()
            
            # Condição para imprimir no terminal
            if line and not line.startswith("[DEBUG] receiveMessage: leu char 0xFE ('.')"):
                print(f"{line}") 
                root.after(0, lambda msg=line: log_output.insert(tk.END, msg + "\n"))
            # Condição para exibir na interface (APENAS mensagens [PICO])
                if line.startswith("[PICO]"): 
                # Add separator after [PICO] message
                    root.after(0, lambda: log_output.insert(tk.END, "="*40 + "\n")) 
                root.after(0, lambda: log_output.see(tk.END)) # Scrolls to the end
        except serial.SerialException as e:
            root.after(0, lambda: log_output.insert(tk.END, f"Serial read error: {e}\n"))
            root.after(0, lambda: log_output.see(tk.END))
            break # Exits the loop on serial error
        except UnicodeDecodeError:
            # Handles potential decoding errors (e.g., junk data)
            pass
        time.sleep(0.01) # Small delay to avoid busy-waiting

def start_serial_thread():
    global stop_serial_thread
    if ser and ser.is_open:
        stop_serial_thread = False
        thread = threading.Thread(target=serial_reader_thread, daemon=True)
        thread.start()
        print("Serial reader thread started.")
    else:
        print("Serial port not open, cannot start reader thread.")

def on_closing():
    global stop_serial_thread
    stop_serial_thread = True
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")
    root.destroy()

# =============================
# Tkinter GUI
# =============================

# Colors for the dark/modern theme
BG_DARK = "#2C3E50"      # Dark Grayish Blue
BG_MEDIUM = "#34495E"    # Slightly lighter than dark for frames
BG_LIGHT = "#ECF0F1"     # Light gray for text on light elements
TEXT_COLOR = "#ECF0F1"   # Standard text color (almost white)
ACCENT_BLUE = "#3498DB"  # Vibrant blue for buttons
ACCENT_GREEN = "#2ECC71" # Emerald green for buttons
ACCENT_RED = "#E74C3C"   # Red for abort/reset

root = tk.Tk()
root.title("Interface PI-7 - G-Code Visualizer")
root.protocol("WM_DELETE_WINDOW", on_closing) # Handles window close event
root.configure(bg=BG_DARK) # Sets main window background

# Font configuration (Aumentado para 10 no código G e Log Serial)
FONT_TITLE = ("Arial", 12, "bold")
FONT_LABEL = ("Arial", 10)
FONT_BUTTON = ("Arial", 10, "bold")
FONT_MONO = ("Consolas", 10) # Increased from 8 to 10

# --- Layout Configuration ---
# Column 0: Intro/Instructions, Command Buttons, Jog Controls, Position Display (stacked vertically)
# Column 1: G-Code Input and Serial Log (stacked vertically)
# Column 2: Plots (stacked vertically)

# Configure main window columns to expand
root.grid_columnconfigure(0, weight=1) # Intro/Commands/Jog/Pos
root.grid_columnconfigure(1, weight=1) # G-Code/Log
root.grid_columnconfigure(2, weight=2) # Plots (more weight)

# Configure main window rows to expand (adjusted to accommodate more elements in Column 0)
root.grid_rowconfigure(0, weight=0) # Intro (fixed, minimized)
root.grid_rowconfigure(1, weight=0) # Command Buttons (fixed)
root.grid_rowconfigure(2, weight=0) # Jog Controls (fixed)
root.grid_rowconfigure(3, weight=1) # Position Display (expands with G-Code/Log/Plots)


# --- Introduction Frame (Column 0, Row 0) ---
intro_frame = tk.Frame(root, bg=BG_DARK, padx=10, pady=5) 
intro_frame.grid(row=0, column=0, sticky='new') # Sticky 'new' to minimize vertical expansion

intro = tk.Label(intro_frame, text=(
    "Modo Código G:\n"
    "Escreva um código G e visualize a trajetória resultante.\n"
    "\n"
    "Controles:\n"
    "- Teclas de seta movimentam o robô (← → ↑ ↓)\n"
    "- Botões executam comandos de controle do programa\n"
    "- Campo 'Passo' define a distância dos movimentos Jog (usar ponto '.' como separador decimal)\n"
    "\n"
    "Instruções G-Code disponíveis:\n"
    "- G00 X__ Y__: movimento rápido até X,Y\n"
    "- G01 X__ Y__: interpolação linear até X,Y\n"
    "- G02/G03 X__ Y__ I__ J__: interpolação circular até X,Y com centro em (Xc, Yc),\n"
    "  definido por I = Xc - X_ini, J = Yc - Y_ini\n"
    "- G04 P__: espera de P milissegundos\n"
), justify="left", font=FONT_LABEL, fg=TEXT_COLOR, bg=BG_DARK)
intro.pack(anchor='nw', fill='x', expand=False) # Do not expand vertically


# --- Command Buttons Frame (Column 0, Row 1) ---
frame_cmd = tk.LabelFrame(root, text="Comandos de Programa", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_TITLE, padx=10, pady=5, relief=tk.RIDGE, bd=2)
frame_cmd.grid(row=1, column=0, padx=10, pady=5, sticky='new') # Below intro, fixed at top

btn_style = {'width': 12, 'font': FONT_BUTTON, 'fg': TEXT_COLOR, 'bd': 0, 'relief': tk.FLAT, 'activebackground': ACCENT_BLUE, 'activeforeground': BG_LIGHT}
tk.Button(frame_cmd, text="Iniciar", command=start_program, bg=ACCENT_GREEN, **btn_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_cmd, text="Suspender", command=suspend_program, bg=ACCENT_BLUE, **btn_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_cmd, text="Continuar", command=continue_program, bg=ACCENT_GREEN, **btn_style).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_cmd, text="Abortar", command=abort_program, bg=ACCENT_RED, **btn_style).grid(row=1, column=1, padx=5, pady=5)

# --- Jog Controls Frame (Column 0, Row 2) ---
frame_jog = tk.LabelFrame(root, text="Controle Jog", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_TITLE, padx=10, pady=5, relief=tk.RIDGE, bd=2)
frame_jog.grid(row=2, column=0, padx=10, pady=5, sticky='new') # Below commands, fixed at top
tk.Label(frame_jog, text="Passo:", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL).grid(row=0, column=0, pady=5)
entry_step = tk.Entry(frame_jog, width=6, bg=BG_LIGHT, fg=BG_DARK, font=FONT_LABEL, justify='center')
entry_step.insert(0, "1")
entry_step.grid(row=0, column=1, pady=5)
jog_btn_style = {'width': 5, 'font': FONT_BUTTON, 'fg': TEXT_COLOR, 'bg': ACCENT_BLUE, 'bd': 0, 'relief': tk.FLAT, 'activebackground': ACCENT_BLUE, 'activeforeground': BG_LIGHT}
tk.Button(frame_jog, text="↑", command=lambda: jog_y('up'), **jog_btn_style).grid(row=1, column=1, pady=2)
tk.Button(frame_jog, text="←", command=lambda: jog_x('left'), **jog_btn_style).grid(row=2, column=0, pady=2)
tk.Button(frame_jog, text="→", command=lambda: jog_x('right'), **jog_btn_style).grid(row=2, column=2, pady=2)
tk.Button(frame_jog, text="↓", command=lambda: jog_y('down'), **jog_btn_style).grid(row=3, column=1, pady=2)


# --- Position Display Frame (Column 0, Row 3) ---
frame_pos = tk.LabelFrame(root, text="Posição Atual", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_TITLE, padx=10, pady=5, relief=tk.RIDGE, bd=2)
frame_pos.grid(row=3, column=0, padx=10, pady=5, sticky='nsew') # Below Jog, expands
tk.Label(frame_pos, text="Posição X:", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL).grid(row=0, column=0, sticky='w')
lbl_x_val = tk.Label(frame_pos, text="--", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL)
lbl_x_val.grid(row=0, column=1, sticky='w')
tk.Label(frame_pos, text="Posição Y:", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL).grid(row=1, column=0, sticky='w')
lbl_y_val = tk.Label(frame_pos, text="--", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL)
lbl_y_val.grid(row=1, column=1, sticky='w')
tk.Label(frame_pos, text="Linha Atual:", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL).grid(row=2, column=0, sticky='w')
lbl_linha_val = tk.Label(frame_pos, text="--", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL)
lbl_linha_val.grid(row=2, column=1, sticky='w')
# Update initial position display
update_position_display()


# --- G-Code Input Frame (Column 1, Row 0) ---
frame_gcode = tk.LabelFrame(root, text="Código G", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_TITLE, padx=10, pady=5, relief=tk.RIDGE, bd=2)
frame_gcode.grid(row=0, column=1, padx=10, pady=10, sticky='nsew') # Top-right of Intro

tk.Label(frame_gcode, text="Insira seu Código G:", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_LABEL).pack(anchor='w', pady=2)
gcode_input = scrolledtext.ScrolledText(frame_gcode, width=40, height=8, bg=BG_LIGHT, fg=BG_DARK, font=FONT_MONO, wrap=tk.WORD) # Reduced height, Font increased
gcode_input.pack(fill='both', expand=True)

btn_gcode_style = {'width': 18, 'font': FONT_BUTTON, 'fg': TEXT_COLOR, 'bd': 0, 'relief': tk.FLAT, 'activebackground': ACCENT_BLUE, 'activeforeground': BG_LIGHT}
tk.Button(frame_gcode, text="Interpretar Código G", command=interpretar_gcode, bg=ACCENT_GREEN, **btn_gcode_style).pack(pady=5, fill='x')
btn_enviar_modbus = tk.Button(frame_gcode, text="Enviar via MODBUS", command=on_click_enviar, bg=ACCENT_BLUE, **btn_gcode_style)
btn_enviar_modbus.pack(pady=5, fill='x')


# --- Serial Log Display Frame (Column 1, Row 1, spans remaining rows in column 1) ---
frame_log = tk.LabelFrame(root, text="Log de Comunicação Serial", bg=BG_MEDIUM, fg=TEXT_COLOR, font=FONT_TITLE, padx=10, pady=5, relief=tk.RIDGE, bd=2)
frame_log.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky='nsew') # Below G-Code input, spans remaining rows

log_output = scrolledtext.ScrolledText(frame_log, width=40, height=12, wrap=tk.WORD, font=FONT_MONO, bg=BG_DARK, fg=TEXT_COLOR, insertbackground=TEXT_COLOR) # Adjusted width/height, Font increased
log_output.pack(expand=True, fill='both', padx=5, pady=5)


# --- Plots Frame (Column 2, spans all rows) ---
plots_frame = tk.Frame(root, bg=BG_DARK)
plots_frame.grid(row=0, column=2, rowspan=4, sticky='nsew', padx=10, pady=10) # Spans all rows in column 2
plots_frame.grid_columnconfigure(0, weight=1) 
plots_frame.grid_rowconfigure(0, weight=1) # Top plot row (now G-Code)
plots_frame.grid_rowconfigure(1, weight=1) # Bottom plot row (now Manual)
plots_frame.grid_rowconfigure(2, weight=0) # Button row (fixed height)


# Invert the order of plots: fig2 (G-Code) on top, fig1 (Manual) on bottom
# These canvas objects are now globally available.
canvas2 = FigureCanvasTkAgg(fig2, master=plots_frame)
canvas2_widget = canvas2.get_tk_widget()
canvas2_widget.grid(row=0, column=0, padx=5, pady=5, sticky='nsew') # Now at row 0

canvas1 = FigureCanvasTkAgg(fig1, master=plots_frame)
canvas1_widget = canvas1.get_tk_widget()
canvas1_widget.grid(row=1, column=0, padx=5, pady=5, sticky='nsew') # Now at row 1

btn_plot_reset_style = {'width': 18, 'font': FONT_BUTTON, 'fg': TEXT_COLOR, 'bd': 0, 'relief': tk.FLAT, 'activebackground': ACCENT_RED, 'activeforeground': BG_LIGHT}
tk.Button(plots_frame, text="Reset Trajetória Manual", command=reset_drawing, bg=ACCENT_RED, **btn_plot_reset_style).grid(row=2, column=0, pady=5, sticky='ew')

# =============================
# Keyboard binds (Restored)
# =============================
root.bind('<Left>', lambda e: jog_x('left'))
root.bind('<Right>', lambda e: jog_x('right'))
root.bind('<Up>', lambda e: jog_y('up'))
root.bind('<Down>', lambda e: jog_y('down'))


# Inicia a thread de leitura serial quando a GUI inicia
start_serial_thread()

# Initial plot draws (important after canvas creation)
plot_trajectory()
plot_expected_trajectory()

root.mainloop()
