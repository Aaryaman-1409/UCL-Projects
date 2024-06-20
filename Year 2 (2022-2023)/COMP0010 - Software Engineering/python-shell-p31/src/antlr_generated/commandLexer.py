# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,9,64,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,
        5,1,5,4,5,32,8,5,11,5,12,5,33,1,5,1,5,1,6,1,6,4,6,40,8,6,11,6,12,
        6,41,1,6,1,6,1,7,1,7,1,7,4,7,49,8,7,11,7,12,7,50,5,7,53,8,7,10,7,
        12,7,56,9,7,1,7,1,7,1,8,4,8,61,8,8,11,8,12,8,62,0,0,9,1,1,3,2,5,
        3,7,4,9,5,11,6,13,7,15,8,17,9,1,0,5,2,0,9,9,32,32,2,0,10,10,39,39,
        2,0,10,10,96,96,3,0,10,10,34,34,96,96,8,0,9,10,32,32,34,34,39,39,
        59,60,62,62,96,96,124,124,69,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,
        0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,
        17,1,0,0,0,1,19,1,0,0,0,3,21,1,0,0,0,5,23,1,0,0,0,7,25,1,0,0,0,9,
        27,1,0,0,0,11,29,1,0,0,0,13,37,1,0,0,0,15,45,1,0,0,0,17,60,1,0,0,
        0,19,20,5,124,0,0,20,2,1,0,0,0,21,22,5,59,0,0,22,4,1,0,0,0,23,24,
        5,60,0,0,24,6,1,0,0,0,25,26,5,62,0,0,26,8,1,0,0,0,27,28,7,0,0,0,
        28,10,1,0,0,0,29,31,5,39,0,0,30,32,8,1,0,0,31,30,1,0,0,0,32,33,1,
        0,0,0,33,31,1,0,0,0,33,34,1,0,0,0,34,35,1,0,0,0,35,36,5,39,0,0,36,
        12,1,0,0,0,37,39,5,96,0,0,38,40,8,2,0,0,39,38,1,0,0,0,40,41,1,0,
        0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,43,1,0,0,0,43,44,5,96,0,0,44,
        14,1,0,0,0,45,54,5,34,0,0,46,53,3,13,6,0,47,49,8,3,0,0,48,47,1,0,
        0,0,49,50,1,0,0,0,50,48,1,0,0,0,50,51,1,0,0,0,51,53,1,0,0,0,52,46,
        1,0,0,0,52,48,1,0,0,0,53,56,1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,
        55,57,1,0,0,0,56,54,1,0,0,0,57,58,5,34,0,0,58,16,1,0,0,0,59,61,8,
        4,0,0,60,59,1,0,0,0,61,62,1,0,0,0,62,60,1,0,0,0,62,63,1,0,0,0,63,
        18,1,0,0,0,7,0,33,41,50,52,54,62,0
    ]

class commandLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    WHITE_SPACE = 5
    SINGLE_QUOTES = 6
    BACK_QUOTES = 7
    DOUBLE_QUOTES = 8
    TEXT = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'|'", "';'", "'<'", "'>'" ]

    symbolicNames = [ "<INVALID>",
            "WHITE_SPACE", "SINGLE_QUOTES", "BACK_QUOTES", "DOUBLE_QUOTES", 
            "TEXT" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "WHITE_SPACE", "SINGLE_QUOTES", 
                  "BACK_QUOTES", "DOUBLE_QUOTES", "TEXT" ]

    grammarFileName = "command.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


