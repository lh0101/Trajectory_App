from antlr4 import *
import numpy as np
from GCodeLexer import GCodeLexer
from GCodeParser import GCodeParser
from GCodeInterpreter import GCodeInterpreter
from antlr4.tree.Tree import ParseTreeWalker


# Lê o arquivo de entrada G-code
input_stream = FileStream("programa.gcode")

# Passa pelo lexer (tokenização)
lexer = GCodeLexer(input_stream)
token_stream = CommonTokenStream(lexer)

# Passa pelo parser (estrutura sintática)
parser = GCodeParser(token_stream)
tree = parser.program()  # começa pela regra 'program'

# Imprime a árvore sintática
print(tree.toStringTree(recog=parser))
interpreter = GCodeInterpreter(circ_interpol_steps=50, linear_interpol_steps=20, name="traj_triang")
walker = ParseTreeWalker()
walker.walk(interpreter, tree)

#obtém move_sequence do interpretador:
x = np.array(interpreter.move_sequence['x'])
y = np.array(interpreter.move_sequence['y'])

print(f"steps em x: {len(x)}")
print(f"steps em y: {len(y)}")



