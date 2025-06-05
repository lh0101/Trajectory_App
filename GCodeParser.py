# Generated from GCode.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,21,120,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,5,0,30,8,0,10,0,12,0,33,9,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,3,2,
        42,8,2,1,3,1,3,1,3,5,3,47,8,3,10,3,12,3,50,9,3,1,3,1,3,1,4,1,4,1,
        4,3,4,57,8,4,1,5,1,5,1,5,1,6,1,6,1,7,1,7,3,7,66,8,7,1,7,1,7,1,8,
        1,8,3,8,72,8,8,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,10,1,10,3,10,83,8,
        10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,3,11,92,8,11,1,11,1,11,1,11,
        5,11,97,8,11,10,11,12,11,100,9,11,1,11,1,11,1,12,1,12,1,12,5,12,
        107,8,12,10,12,12,12,110,9,12,1,13,1,13,1,13,3,13,115,8,13,1,13,
        3,13,118,8,13,1,13,0,0,14,0,2,4,6,8,10,12,14,16,18,20,22,24,26,0,
        1,1,0,10,11,119,0,31,1,0,0,0,2,36,1,0,0,0,4,41,1,0,0,0,6,43,1,0,
        0,0,8,56,1,0,0,0,10,58,1,0,0,0,12,61,1,0,0,0,14,63,1,0,0,0,16,69,
        1,0,0,0,18,75,1,0,0,0,20,78,1,0,0,0,22,87,1,0,0,0,24,103,1,0,0,0,
        26,111,1,0,0,0,28,30,3,4,2,0,29,28,1,0,0,0,30,33,1,0,0,0,31,29,1,
        0,0,0,31,32,1,0,0,0,32,34,1,0,0,0,33,31,1,0,0,0,34,35,3,2,1,0,35,
        1,1,0,0,0,36,37,5,2,0,0,37,3,1,0,0,0,38,42,3,20,10,0,39,42,3,6,3,
        0,40,42,3,22,11,0,41,38,1,0,0,0,41,39,1,0,0,0,41,40,1,0,0,0,42,5,
        1,0,0,0,43,44,3,10,5,0,44,48,3,12,6,0,45,47,3,8,4,0,46,45,1,0,0,
        0,47,50,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,0,49,51,1,0,0,0,50,48,
        1,0,0,0,51,52,5,20,0,0,52,7,1,0,0,0,53,57,3,14,7,0,54,57,3,16,8,
        0,55,57,3,18,9,0,56,53,1,0,0,0,56,54,1,0,0,0,56,55,1,0,0,0,57,9,
        1,0,0,0,58,59,5,6,0,0,59,60,5,11,0,0,60,11,1,0,0,0,61,62,5,1,0,0,
        62,13,1,0,0,0,63,65,5,3,0,0,64,66,5,13,0,0,65,64,1,0,0,0,65,66,1,
        0,0,0,66,67,1,0,0,0,67,68,7,0,0,0,68,15,1,0,0,0,69,71,5,4,0,0,70,
        72,5,13,0,0,71,70,1,0,0,0,71,72,1,0,0,0,72,73,1,0,0,0,73,74,7,0,
        0,0,74,17,1,0,0,0,75,76,5,5,0,0,76,77,5,11,0,0,77,19,1,0,0,0,78,
        79,5,8,0,0,79,80,5,12,0,0,80,82,5,14,0,0,81,83,5,13,0,0,82,81,1,
        0,0,0,82,83,1,0,0,0,83,84,1,0,0,0,84,85,7,0,0,0,85,86,5,20,0,0,86,
        21,1,0,0,0,87,88,5,9,0,0,88,89,5,12,0,0,89,91,5,17,0,0,90,92,3,24,
        12,0,91,90,1,0,0,0,91,92,1,0,0,0,92,93,1,0,0,0,93,94,5,18,0,0,94,
        98,5,15,0,0,95,97,3,4,2,0,96,95,1,0,0,0,97,100,1,0,0,0,98,96,1,0,
        0,0,98,99,1,0,0,0,99,101,1,0,0,0,100,98,1,0,0,0,101,102,5,16,0,0,
        102,23,1,0,0,0,103,108,3,26,13,0,104,105,5,19,0,0,105,107,3,26,13,
        0,106,104,1,0,0,0,107,110,1,0,0,0,108,106,1,0,0,0,108,109,1,0,0,
        0,109,25,1,0,0,0,110,108,1,0,0,0,111,117,5,12,0,0,112,114,5,14,0,
        0,113,115,5,13,0,0,114,113,1,0,0,0,114,115,1,0,0,0,115,116,1,0,0,
        0,116,118,7,0,0,0,117,112,1,0,0,0,117,118,1,0,0,0,118,27,1,0,0,0,
        12,31,41,48,56,65,71,82,91,98,108,114,117
    ]

class GCodeParser ( Parser ):

    grammarFileName = "GCode.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'M30'", "<INVALID>", "<INVALID>", 
                     "'P'", "'N'", "'T'", "'VAR'", "'FUNC'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'-'", "'='", "'{'", "'}'", 
                     "'('", "')'", "','" ]

    symbolicNames = [ "<INVALID>", "GCODE", "M30", "DIR", "DELTA", "P", 
                      "N", "T", "VAR", "FUNC", "FLOAT", "INT", "ID", "MINUS", 
                      "ASSIGN", "LBRACE", "RBRACE", "LPAREN", "RPAREN", 
                      "COMMA", "LINE_END", "WS" ]

    RULE_program = 0
    RULE_programEnd = 1
    RULE_declaration = 2
    RULE_statement = 3
    RULE_detail = 4
    RULE_lineNumber = 5
    RULE_codFunc = 6
    RULE_coord = 7
    RULE_delta_center = 8
    RULE_stop_ms = 9
    RULE_variable = 10
    RULE_function = 11
    RULE_parameterList = 12
    RULE_parameter = 13

    ruleNames =  [ "program", "programEnd", "declaration", "statement", 
                   "detail", "lineNumber", "codFunc", "coord", "delta_center", 
                   "stop_ms", "variable", "function", "parameterList", "parameter" ]

    EOF = Token.EOF
    GCODE=1
    M30=2
    DIR=3
    DELTA=4
    P=5
    N=6
    T=7
    VAR=8
    FUNC=9
    FLOAT=10
    INT=11
    ID=12
    MINUS=13
    ASSIGN=14
    LBRACE=15
    RBRACE=16
    LPAREN=17
    RPAREN=18
    COMMA=19
    LINE_END=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def programEnd(self):
            return self.getTypedRuleContext(GCodeParser.ProgramEndContext,0)


        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(GCodeParser.DeclarationContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = GCodeParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 832) != 0):
                self.state = 28
                self.declaration()
                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 34
            self.programEnd()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramEndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def M30(self):
            return self.getToken(GCodeParser.M30, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_programEnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgramEnd" ):
                listener.enterProgramEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgramEnd" ):
                listener.exitProgramEnd(self)




    def programEnd(self):

        localctx = GCodeParser.ProgramEndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_programEnd)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(GCodeParser.M30)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variable(self):
            return self.getTypedRuleContext(GCodeParser.VariableContext,0)


        def statement(self):
            return self.getTypedRuleContext(GCodeParser.StatementContext,0)


        def function(self):
            return self.getTypedRuleContext(GCodeParser.FunctionContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)




    def declaration(self):

        localctx = GCodeParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_declaration)
        try:
            self.state = 41
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 38
                self.variable()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 39
                self.statement()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 40
                self.function()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lineNumber(self):
            return self.getTypedRuleContext(GCodeParser.LineNumberContext,0)


        def codFunc(self):
            return self.getTypedRuleContext(GCodeParser.CodFuncContext,0)


        def LINE_END(self):
            return self.getToken(GCodeParser.LINE_END, 0)

        def detail(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.DetailContext)
            else:
                return self.getTypedRuleContext(GCodeParser.DetailContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = GCodeParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.lineNumber()
            self.state = 44
            self.codFunc()
            self.state = 48
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 56) != 0):
                self.state = 45
                self.detail()
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 51
            self.match(GCodeParser.LINE_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DetailContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def coord(self):
            return self.getTypedRuleContext(GCodeParser.CoordContext,0)


        def delta_center(self):
            return self.getTypedRuleContext(GCodeParser.Delta_centerContext,0)


        def stop_ms(self):
            return self.getTypedRuleContext(GCodeParser.Stop_msContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_detail

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDetail" ):
                listener.enterDetail(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDetail" ):
                listener.exitDetail(self)




    def detail(self):

        localctx = GCodeParser.DetailContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_detail)
        try:
            self.state = 56
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.coord()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 54
                self.delta_center()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 55
                self.stop_ms()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def N(self):
            return self.getToken(GCodeParser.N, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_lineNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)




    def lineNumber(self):

        localctx = GCodeParser.LineNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_lineNumber)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.match(GCodeParser.N)
            self.state = 59
            self.match(GCodeParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CodFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GCODE(self):
            return self.getToken(GCodeParser.GCODE, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_codFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCodFunc" ):
                listener.enterCodFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCodFunc" ):
                listener.exitCodFunc(self)




    def codFunc(self):

        localctx = GCodeParser.CodFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_codFunc)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(GCodeParser.GCODE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CoordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIR(self):
            return self.getToken(GCodeParser.DIR, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def MINUS(self):
            return self.getToken(GCodeParser.MINUS, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_coord

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoord" ):
                listener.enterCoord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoord" ):
                listener.exitCoord(self)




    def coord(self):

        localctx = GCodeParser.CoordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_coord)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(GCodeParser.DIR)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 64
                self.match(GCodeParser.MINUS)


            self.state = 67
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Delta_centerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DELTA(self):
            return self.getToken(GCodeParser.DELTA, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def MINUS(self):
            return self.getToken(GCodeParser.MINUS, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_delta_center

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDelta_center" ):
                listener.enterDelta_center(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDelta_center" ):
                listener.exitDelta_center(self)




    def delta_center(self):

        localctx = GCodeParser.Delta_centerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_delta_center)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(GCodeParser.DELTA)
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 70
                self.match(GCodeParser.MINUS)


            self.state = 73
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Stop_msContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def P(self):
            return self.getToken(GCodeParser.P, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_stop_ms

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStop_ms" ):
                listener.enterStop_ms(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStop_ms" ):
                listener.exitStop_ms(self)




    def stop_ms(self):

        localctx = GCodeParser.Stop_msContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_stop_ms)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(GCodeParser.P)
            self.state = 76
            self.match(GCodeParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAR(self):
            return self.getToken(GCodeParser.VAR, 0)

        def ID(self):
            return self.getToken(GCodeParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(GCodeParser.ASSIGN, 0)

        def LINE_END(self):
            return self.getToken(GCodeParser.LINE_END, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def MINUS(self):
            return self.getToken(GCodeParser.MINUS, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)




    def variable(self):

        localctx = GCodeParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_variable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self.match(GCodeParser.VAR)
            self.state = 79
            self.match(GCodeParser.ID)
            self.state = 80
            self.match(GCodeParser.ASSIGN)
            self.state = 82
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==13:
                self.state = 81
                self.match(GCodeParser.MINUS)


            self.state = 84
            _la = self._input.LA(1)
            if not(_la==10 or _la==11):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 85
            self.match(GCodeParser.LINE_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNC(self):
            return self.getToken(GCodeParser.FUNC, 0)

        def ID(self):
            return self.getToken(GCodeParser.ID, 0)

        def LPAREN(self):
            return self.getToken(GCodeParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(GCodeParser.RPAREN, 0)

        def LBRACE(self):
            return self.getToken(GCodeParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(GCodeParser.RBRACE, 0)

        def parameterList(self):
            return self.getTypedRuleContext(GCodeParser.ParameterListContext,0)


        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(GCodeParser.DeclarationContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)




    def function(self):

        localctx = GCodeParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(GCodeParser.FUNC)
            self.state = 88
            self.match(GCodeParser.ID)
            self.state = 89
            self.match(GCodeParser.LPAREN)
            self.state = 91
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 90
                self.parameterList()


            self.state = 93
            self.match(GCodeParser.RPAREN)
            self.state = 94
            self.match(GCodeParser.LBRACE)
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 832) != 0):
                self.state = 95
                self.declaration()
                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 101
            self.match(GCodeParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.ParameterContext)
            else:
                return self.getTypedRuleContext(GCodeParser.ParameterContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(GCodeParser.COMMA)
            else:
                return self.getToken(GCodeParser.COMMA, i)

        def getRuleIndex(self):
            return GCodeParser.RULE_parameterList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterList" ):
                listener.enterParameterList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterList" ):
                listener.exitParameterList(self)




    def parameterList(self):

        localctx = GCodeParser.ParameterListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_parameterList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.parameter()
            self.state = 108
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 104
                self.match(GCodeParser.COMMA)
                self.state = 105
                self.parameter()
                self.state = 110
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(GCodeParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(GCodeParser.ASSIGN, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def MINUS(self):
            return self.getToken(GCodeParser.MINUS, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_parameter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameter" ):
                listener.enterParameter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameter" ):
                listener.exitParameter(self)




    def parameter(self):

        localctx = GCodeParser.ParameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_parameter)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.match(GCodeParser.ID)
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 112
                self.match(GCodeParser.ASSIGN)
                self.state = 114
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==13:
                    self.state = 113
                    self.match(GCodeParser.MINUS)


                self.state = 116
                _la = self._input.LA(1)
                if not(_la==10 or _la==11):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





