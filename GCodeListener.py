# Generated from GCode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GCodeParser import GCodeParser
else:
    from GCodeParser import GCodeParser

# This class defines a complete listener for a parse tree produced by GCodeParser.
class GCodeListener(ParseTreeListener):

    # Enter a parse tree produced by GCodeParser#program.
    def enterProgram(self, ctx:GCodeParser.ProgramContext):
        pass

    # Exit a parse tree produced by GCodeParser#program.
    def exitProgram(self, ctx:GCodeParser.ProgramContext):
        pass


    # Enter a parse tree produced by GCodeParser#programEnd.
    def enterProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        pass

    # Exit a parse tree produced by GCodeParser#programEnd.
    def exitProgramEnd(self, ctx:GCodeParser.ProgramEndContext):
        pass


    # Enter a parse tree produced by GCodeParser#declaration.
    def enterDeclaration(self, ctx:GCodeParser.DeclarationContext):
        pass

    # Exit a parse tree produced by GCodeParser#declaration.
    def exitDeclaration(self, ctx:GCodeParser.DeclarationContext):
        pass


    # Enter a parse tree produced by GCodeParser#statement.
    def enterStatement(self, ctx:GCodeParser.StatementContext):
        pass

    # Exit a parse tree produced by GCodeParser#statement.
    def exitStatement(self, ctx:GCodeParser.StatementContext):
        pass


    # Enter a parse tree produced by GCodeParser#detail.
    def enterDetail(self, ctx:GCodeParser.DetailContext):
        pass

    # Exit a parse tree produced by GCodeParser#detail.
    def exitDetail(self, ctx:GCodeParser.DetailContext):
        pass


    # Enter a parse tree produced by GCodeParser#lineNumber.
    def enterLineNumber(self, ctx:GCodeParser.LineNumberContext):
        pass

    # Exit a parse tree produced by GCodeParser#lineNumber.
    def exitLineNumber(self, ctx:GCodeParser.LineNumberContext):
        pass


    # Enter a parse tree produced by GCodeParser#codFunc.
    def enterCodFunc(self, ctx:GCodeParser.CodFuncContext):
        pass

    # Exit a parse tree produced by GCodeParser#codFunc.
    def exitCodFunc(self, ctx:GCodeParser.CodFuncContext):
        pass


    # Enter a parse tree produced by GCodeParser#coord.
    def enterCoord(self, ctx:GCodeParser.CoordContext):
        pass

    # Exit a parse tree produced by GCodeParser#coord.
    def exitCoord(self, ctx:GCodeParser.CoordContext):
        pass


    # Enter a parse tree produced by GCodeParser#delta_center.
    def enterDelta_center(self, ctx:GCodeParser.Delta_centerContext):
        pass

    # Exit a parse tree produced by GCodeParser#delta_center.
    def exitDelta_center(self, ctx:GCodeParser.Delta_centerContext):
        pass


    # Enter a parse tree produced by GCodeParser#stop_ms.
    def enterStop_ms(self, ctx:GCodeParser.Stop_msContext):
        pass

    # Exit a parse tree produced by GCodeParser#stop_ms.
    def exitStop_ms(self, ctx:GCodeParser.Stop_msContext):
        pass


    # Enter a parse tree produced by GCodeParser#variable.
    def enterVariable(self, ctx:GCodeParser.VariableContext):
        pass

    # Exit a parse tree produced by GCodeParser#variable.
    def exitVariable(self, ctx:GCodeParser.VariableContext):
        pass


    # Enter a parse tree produced by GCodeParser#function.
    def enterFunction(self, ctx:GCodeParser.FunctionContext):
        pass

    # Exit a parse tree produced by GCodeParser#function.
    def exitFunction(self, ctx:GCodeParser.FunctionContext):
        pass


    # Enter a parse tree produced by GCodeParser#parameterList.
    def enterParameterList(self, ctx:GCodeParser.ParameterListContext):
        pass

    # Exit a parse tree produced by GCodeParser#parameterList.
    def exitParameterList(self, ctx:GCodeParser.ParameterListContext):
        pass


    # Enter a parse tree produced by GCodeParser#parameter.
    def enterParameter(self, ctx:GCodeParser.ParameterContext):
        pass

    # Exit a parse tree produced by GCodeParser#parameter.
    def exitParameter(self, ctx:GCodeParser.ParameterContext):
        pass



del GCodeParser