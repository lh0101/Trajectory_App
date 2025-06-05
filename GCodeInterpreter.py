from GCodeParser import GCodeParser
from GCodeListener import GCodeListener
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

get_value = lambda val: float((val.FLOAT() or val.INT()).getText()) if val else None


class GCodeInterpreter(GCodeListener):
    def __init__(self, circ_interpol_steps=100, linear_interpol_steps=100, name="Trajetória"):
        super().__init__()
        self.name = name
        self.circ_steps = circ_interpol_steps
        self.lin_steps = linear_interpol_steps
        self.move_sequence = {'x':[0], 'y':[0]}
        self.previous_position = (0, 0)  # Initialize previous position (X, Y)
        

    def exitDeclaration(self, ctx:GCodeParser.DeclarationContext):
        print("Finished processing declaration:", ctx.getText())
        return super().exitDeclaration(ctx)
    
    def exitStatement(self, ctx:GCodeParser.StatementContext):
        function_code = ctx.codFunc().getText()
        if ctx.codFunc() == None\
        or function_code[0]!='G'\
        or len(function_code)!=3:
            raise Exception(f"No valid function code found in statement: {ctx.getText()}")
        else:
            print("Processing function code:", function_code)
            exec_func = int(function_code[1:])
            if exec_func == 0:
                self.position(ctx)
            elif exec_func == 1:
                self.lin_interpol(ctx)
            elif exec_func == 2:
                self.circ_interpol_cw(ctx)
            elif exec_func == 3:
                self.circ_interpol_ccw(ctx)
            elif exec_func == 4:
                self.delay(ctx)
            else:
                raise Exception(f"Unknown function code: {exec_func}")

    def validate_circFunc(self, X, Y, Xc, Yc, R):
        R_pt_fim = np.sqrt((X-Xc)**2+(Y-Yc)**2)
        if np.isclose(R, R_pt_fim, atol=1e-6):
            return True 
        else:
            raise Exception(f"The circular interpolation command is invalid: starting radius={R}; ending radius={R_pt_fim}") 

    def extract_circ_details(self, details):
        X = Y = dxc = dyc = None
        for detail in details: # X e Y esperados -> posições finais do arco
            if detail.coord():
                coord = detail.coord()
                if coord.DIR().getText() == 'X':
                    X = -get_value(coord) if coord.MINUS() else get_value(coord)
                elif coord.DIR().getText() == 'Y':
                    Y = -get_value(coord) if coord.MINUS() else get_value(coord)
            elif detail.delta_center():
                delta = detail.delta_center()
                if delta.DELTA().getText() == 'I':
                    dxc = -get_value(delta) if delta.MINUS() else get_value(delta)
                elif delta.DELTA().getText() == 'J':
                    dyc = -get_value(delta) if delta.MINUS() else get_value(delta)
        if dxc is not None and dyc is not None:
            Xc = self.previous_position[0] + dxc
            Yc = self.previous_position[1] + dyc
            R = np.sqrt(dxc**2 + dyc**2)
            ang_inicial = np.arctan2(self.previous_position[1] - Yc, self.previous_position[0] - Xc)
            ang_final = np.arctan2(Y-Yc, X-Xc)
            if self.validate_circFunc(X, Y, Xc, Yc, R):
                return Xc, Yc, R, ang_final, ang_inicial
        else:
            raise Exception(f"Missing delta to center for circular interpolation in: {[detail for detail in details]}")
        
    def extract_lin_details(self, details): 
        X = Y = None
        for detail in details: # X e Y esperados -> são a posição final
            if detail.coord():
                coord = detail.coord()
            else: 
                continue
            if coord.DIR().getText() == 'X':
                X = -get_value(coord) if coord.MINUS() else get_value(coord)
            elif coord.DIR().getText() == 'Y':
                Y = -get_value(coord) if coord.MINUS() else get_value(coord)
        return X, Y


    def lin_interpol(self, ctx:GCodeParser.StatementContext):
        print("Generating linearly interpolated points...")
        details = list(ctx.detail())
        X, Y = self.extract_lin_details(details)
        if X is not None and Y is not None:
            # Implement the linear interpolation logic here
            if X == self.previous_position[0]:
                y = np.linspace(self.previous_position[1], Y, self.lin_steps)
                x = np.full(len(y), X)
            else:
                tg = (Y - self.previous_position[1])/(X - self.previous_position[0])
                x = np.linspace(self.previous_position[0], X, self.lin_steps)
                y = self.previous_position[1] + tg * (x - self.previous_position[0])
            self.move_sequence['x'].extend(x)
            self.move_sequence['y'].extend(y)
            self.previous_position = (X, Y)
            print(f"Setting to position: X={x[-1]}, Y={y[-1]}")
        else:
            raise Exception(f"Missing coordinates for linear interpolation in: {ctx.getText()}")

    def position(self, ctx:GCodeParser.StatementContext): 
        print("Positioning...")
        # o objetivo desta função é apenas mover o dispositivo para uma posição especifica sem se preocupar com trajetória
        details = list(ctx.detail())
        X, Y = self.extract_lin_details(details)
        if X is not None and Y is not None:
            # Implement the movement logic here - esta logica de movimento é simples e não é realizada por meio de interpolação em etapas
            self.move_sequence['x'].append(X)
            self.move_sequence['y'].append(Y)
            # new position is set to (X, Y)
            self.previous_position = (X, Y)
            print(f"Setting to position: X={X}, Y={Y}")
        else:
            raise Exception(f"Missing coordinates for position in: {ctx.getText()}" )

    def circ_interpol_cw(self, ctx:GCodeParser.StatementContext):
        print("Generating clockwise interpolated points...")
        details = list(ctx.detail()) 
        Xc, Yc, R, ang_final, ang_inicial   = self.extract_circ_details(details)
        if Xc is not None and Yc is not None and ang_final is not None and ang_inicial is not None:
            # circular clockwise interpol function
            if ang_final >= ang_inicial:
                ang_final -= 2*np.pi
            delta_ang = ang_final - ang_inicial
            steps = max(2, int(abs(self.circ_steps * delta_ang / (2*np.pi))))
            angs = np.linspace(ang_inicial, ang_final, steps)
            y = Yc + R*np.sin(angs)
            x = Xc + R*np.cos(angs)
            self.move_sequence['x'].extend(x)
            self.move_sequence['y'].extend(y)
            self.previous_position = (x[-1], y[-1])
            print(f"Setting to calculated position: X={x[-1]}, Y={y[-1]}")
            # calcular posição baseado em Xc, Yc, e theta e colocar no previous position 
        else:
            raise Exception(f"Missing coordinates or angle for circular interpolation in: {ctx.getText()}")

    def circ_interpol_ccw(self, ctx:GCodeParser.StatementContext):
        print("Generating counter-clockwise interpolated points...")
        details = list(ctx.detail())
        Xc, Yc, R, ang_final, ang_inicial   = self.extract_circ_details(details)
        if Xc is not None and Yc is not None and ang_final is not None and ang_inicial is not None:
            # circular conter-clockwise interpol function
            if ang_final < ang_inicial:
                ang_final += 2*np.pi
            delta_ang = ang_final - ang_inicial
            steps = max(2, int(abs(self.circ_steps * delta_ang / (2*np.pi))))
            angs = np.linspace(ang_inicial, ang_final, steps)
            y = Yc + R*np.sin(angs)
            x = Xc + R*np.cos(angs)
            self.move_sequence['x'].extend(x)
            self.move_sequence['y'].extend(y)
            self.previous_position = (x[-1], y[-1])
            print(f"Setting to calculated position: X={x[-1]}, Y={y[-1]}")
            # calcular posição baseado em Xc, Yc, e theta e colocar no previous position 
        else:
            raise Exception(f"Missing coordinates or angle for circular interpolation in: {ctx.getText()}")
    
    def delay(self, ctx:GCodeParser.StatementContext):
        details = list(ctx.detail())
        delay_time = None
        for detail in details:
            if detail.stop_ms():
                delay_time = get_value(detail.stop_ms())
        if delay_time:
            print(f"Delaying for {delay_time} milliseconds")
            # Implement the delay logic here
        else:
            raise Exception(f"Missing delay time in: {ctx.getText()}")

    def preview_movement(self):
        x = self.move_sequence['x']
        y = self.move_sequence['y']

        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='x', linestyle='-', color='red', markersize=4, linewidth=1)
        plt.title("Preview da trajetória")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis('equal')
        plt.grid(True)
        plt.show()
        input("Pressione Enter para encerrar...")

    def enterProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        print("Programa finalizado com M30")
        # Aqui você pode chamar o preview se quiser exibir ao final automaticamente
        # self.preview_movement()
        # self.generate_gif()
        # print("Program ended")

    def generate_gif(self):
        filename=f"{self.name}.gif"
        x_data = self.move_sequence['x']
        y_data = self.move_sequence['y']
        
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(min(x_data)-10, max(x_data)+10)
        ax.set_ylim(min(y_data)-10, max(y_data)+10)
        ax.set_title("Animação da Trajetória")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)
        ax.set_aspect('equal')

        line, = ax.plot([], [], marker='x', linestyle='-', color='red', markersize=4, linewidth=1)

        def update(frame):
            line.set_data(x_data[:frame], y_data[:frame])
            return line,

        ani = FuncAnimation(fig, update, frames=len(x_data), interval=50, blit=True)
        ani.save(filename, writer=PillowWriter(fps=20))
        print(f"GIF salvo como {filename}")



class TranslatorMechanism(GCodeInterpreter): # classe responsável por receber o dicionário de movimentos move_sequence = {'x':[...], 'y':[...]}
    # transforma move_sequence numa sequencia de tamanhos das cordas posicionadas em pontos fixos definidos
    # o tamanho das coordas e posição definida para os pontos onde estão os motores irão definir todo o resto do programa pensado em GCode
    # aqui podemos implementar as funções que tranformam os tamanhos de cordas em rotações de pwm a partir do valor salvo de tamanho de corda anterior
    # esta parte terá comunicação com controle?
    ...