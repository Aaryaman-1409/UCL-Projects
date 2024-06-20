# Generated from command.g4 by ANTLR 4.11.1
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
        4,1,9,108,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,1,0,3,0,19,8,0,1,0,3,0,22,8,0,3,0,24,8,0,1,0,1,0,1,
        1,1,1,1,1,3,1,31,8,1,1,2,1,2,1,2,3,2,36,8,2,1,2,3,2,39,8,2,1,3,5,
        3,42,8,3,10,3,12,3,45,9,3,1,3,1,3,5,3,49,8,3,10,3,12,3,52,9,3,5,
        3,54,8,3,10,3,12,3,57,9,3,1,3,1,3,5,3,61,8,3,10,3,12,3,64,9,3,1,
        3,5,3,67,8,3,10,3,12,3,70,9,3,1,3,5,3,73,8,3,10,3,12,3,76,9,3,1,
        4,1,4,3,4,80,8,4,1,5,1,5,4,5,84,8,5,11,5,12,5,85,1,6,1,6,5,6,90,
        8,6,10,6,12,6,93,9,6,1,6,1,6,1,6,5,6,98,8,6,10,6,12,6,101,9,6,1,
        6,3,6,104,8,6,1,7,1,7,1,7,0,0,8,0,2,4,6,8,10,12,14,0,1,1,0,6,8,117,
        0,23,1,0,0,0,2,27,1,0,0,0,4,32,1,0,0,0,6,43,1,0,0,0,8,79,1,0,0,0,
        10,83,1,0,0,0,12,103,1,0,0,0,14,105,1,0,0,0,16,18,3,6,3,0,17,19,
        3,2,1,0,18,17,1,0,0,0,18,19,1,0,0,0,19,21,1,0,0,0,20,22,3,4,2,0,
        21,20,1,0,0,0,21,22,1,0,0,0,22,24,1,0,0,0,23,16,1,0,0,0,23,24,1,
        0,0,0,24,25,1,0,0,0,25,26,5,0,0,1,26,1,1,0,0,0,27,28,5,1,0,0,28,
        30,3,6,3,0,29,31,3,2,1,0,30,29,1,0,0,0,30,31,1,0,0,0,31,3,1,0,0,
        0,32,33,5,2,0,0,33,35,3,6,3,0,34,36,3,2,1,0,35,34,1,0,0,0,35,36,
        1,0,0,0,36,38,1,0,0,0,37,39,3,4,2,0,38,37,1,0,0,0,38,39,1,0,0,0,
        39,5,1,0,0,0,40,42,5,5,0,0,41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,
        0,0,43,44,1,0,0,0,44,55,1,0,0,0,45,43,1,0,0,0,46,50,3,12,6,0,47,
        49,5,5,0,0,48,47,1,0,0,0,49,52,1,0,0,0,50,48,1,0,0,0,50,51,1,0,0,
        0,51,54,1,0,0,0,52,50,1,0,0,0,53,46,1,0,0,0,54,57,1,0,0,0,55,53,
        1,0,0,0,55,56,1,0,0,0,56,58,1,0,0,0,57,55,1,0,0,0,58,68,3,10,5,0,
        59,61,5,5,0,0,60,59,1,0,0,0,61,64,1,0,0,0,62,60,1,0,0,0,62,63,1,
        0,0,0,63,65,1,0,0,0,64,62,1,0,0,0,65,67,3,8,4,0,66,62,1,0,0,0,67,
        70,1,0,0,0,68,66,1,0,0,0,68,69,1,0,0,0,69,74,1,0,0,0,70,68,1,0,0,
        0,71,73,5,5,0,0,72,71,1,0,0,0,73,76,1,0,0,0,74,72,1,0,0,0,74,75,
        1,0,0,0,75,7,1,0,0,0,76,74,1,0,0,0,77,80,3,12,6,0,78,80,3,10,5,0,
        79,77,1,0,0,0,79,78,1,0,0,0,80,9,1,0,0,0,81,84,3,14,7,0,82,84,5,
        9,0,0,83,81,1,0,0,0,83,82,1,0,0,0,84,85,1,0,0,0,85,83,1,0,0,0,85,
        86,1,0,0,0,86,11,1,0,0,0,87,91,5,3,0,0,88,90,5,5,0,0,89,88,1,0,0,
        0,90,93,1,0,0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,94,1,0,0,0,93,91,
        1,0,0,0,94,104,3,10,5,0,95,99,5,4,0,0,96,98,5,5,0,0,97,96,1,0,0,
        0,98,101,1,0,0,0,99,97,1,0,0,0,99,100,1,0,0,0,100,102,1,0,0,0,101,
        99,1,0,0,0,102,104,3,10,5,0,103,87,1,0,0,0,103,95,1,0,0,0,104,13,
        1,0,0,0,105,106,7,0,0,0,106,15,1,0,0,0,18,18,21,23,30,35,38,43,50,
        55,62,68,74,79,83,85,91,99,103
    ]

class commandParser ( Parser ):

    grammarFileName = "command.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'|'", "';'", "'<'", "'>'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "WHITE_SPACE", "SINGLE_QUOTES", "BACK_QUOTES", 
                      "DOUBLE_QUOTES", "TEXT" ]

    RULE_command = 0
    RULE_pipe = 1
    RULE_sequence = 2
    RULE_call = 3
    RULE_atom = 4
    RULE_argument = 5
    RULE_redirection = 6
    RULE_quoted = 7

    ruleNames =  [ "command", "pipe", "sequence", "call", "atom", "argument", 
                   "redirection", "quoted" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    WHITE_SPACE=5
    SINGLE_QUOTES=6
    BACK_QUOTES=7
    DOUBLE_QUOTES=8
    TEXT=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class CommandContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(commandParser.EOF, 0)

        def call(self):
            return self.getTypedRuleContext(commandParser.CallContext,0)


        def sequence(self):
            return self.getTypedRuleContext(commandParser.SequenceContext,0)


        def pipe(self):
            return self.getTypedRuleContext(commandParser.PipeContext,0)


        def getRuleIndex(self):
            return commandParser.RULE_command

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCommand" ):
                listener.enterCommand(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCommand" ):
                listener.exitCommand(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommand" ):
                return visitor.visitCommand(self)
            else:
                return visitor.visitChildren(self)




    def command(self):

        localctx = commandParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_command)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 1016) != 0:
                self.state = 16
                self.call()
                self.state = 18
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 17
                    self.pipe()


                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==2:
                    self.state = 20
                    self.sequence()




            self.state = 25
            self.match(commandParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PipeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def call(self):
            return self.getTypedRuleContext(commandParser.CallContext,0)


        def pipe(self):
            return self.getTypedRuleContext(commandParser.PipeContext,0)


        def getRuleIndex(self):
            return commandParser.RULE_pipe

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipe" ):
                listener.enterPipe(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipe" ):
                listener.exitPipe(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPipe" ):
                return visitor.visitPipe(self)
            else:
                return visitor.visitChildren(self)




    def pipe(self):

        localctx = commandParser.PipeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_pipe)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.match(commandParser.T__0)
            self.state = 28
            self.call()
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 29
                self.pipe()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def call(self):
            return self.getTypedRuleContext(commandParser.CallContext,0)


        def sequence(self):
            return self.getTypedRuleContext(commandParser.SequenceContext,0)


        def pipe(self):
            return self.getTypedRuleContext(commandParser.PipeContext,0)


        def getRuleIndex(self):
            return commandParser.RULE_sequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSequence" ):
                listener.enterSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSequence" ):
                listener.exitSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSequence" ):
                return visitor.visitSequence(self)
            else:
                return visitor.visitChildren(self)




    def sequence(self):

        localctx = commandParser.SequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(commandParser.T__1)

            self.state = 33
            self.call()
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1:
                self.state = 34
                self.pipe()


            self.state = 38
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 37
                self.sequence()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self):
            return self.getTypedRuleContext(commandParser.ArgumentContext,0)


        def WHITE_SPACE(self, i:int=None):
            if i is None:
                return self.getTokens(commandParser.WHITE_SPACE)
            else:
                return self.getToken(commandParser.WHITE_SPACE, i)

        def redirection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(commandParser.RedirectionContext)
            else:
                return self.getTypedRuleContext(commandParser.RedirectionContext,i)


        def atom(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(commandParser.AtomContext)
            else:
                return self.getTypedRuleContext(commandParser.AtomContext,i)


        def getRuleIndex(self):
            return commandParser.RULE_call

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCall" ):
                listener.enterCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCall" ):
                listener.exitCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCall" ):
                return visitor.visitCall(self)
            else:
                return visitor.visitChildren(self)




    def call(self):

        localctx = commandParser.CallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_call)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 40
                self.match(commandParser.WHITE_SPACE)
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3 or _la==4:
                self.state = 46
                self.redirection()
                self.state = 50
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 47
                    self.match(commandParser.WHITE_SPACE)
                    self.state = 52
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 58
            self.argument()
            self.state = 68
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 62
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==5:
                        self.state = 59
                        self.match(commandParser.WHITE_SPACE)
                        self.state = 64
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 65
                    self.atom() 
                self.state = 70
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 71
                self.match(commandParser.WHITE_SPACE)
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def redirection(self):
            return self.getTypedRuleContext(commandParser.RedirectionContext,0)


        def argument(self):
            return self.getTypedRuleContext(commandParser.ArgumentContext,0)


        def getRuleIndex(self):
            return commandParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = commandParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_atom)
        try:
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 77
                self.redirection()
                pass
            elif token in [6, 7, 8, 9]:
                self.enterOuterAlt(localctx, 2)
                self.state = 78
                self.argument()
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


    class ArgumentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def quoted(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(commandParser.QuotedContext)
            else:
                return self.getTypedRuleContext(commandParser.QuotedContext,i)


        def TEXT(self, i:int=None):
            if i is None:
                return self.getTokens(commandParser.TEXT)
            else:
                return self.getToken(commandParser.TEXT, i)

        def getRuleIndex(self):
            return commandParser.RULE_argument

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgument" ):
                listener.enterArgument(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgument" ):
                listener.exitArgument(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgument" ):
                return visitor.visitArgument(self)
            else:
                return visitor.visitChildren(self)




    def argument(self):

        localctx = commandParser.ArgumentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_argument)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 83
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [6, 7, 8]:
                        self.state = 81
                        self.quoted()
                        pass
                    elif token in [9]:
                        self.state = 82
                        self.match(commandParser.TEXT)
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 85 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RedirectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argument(self):
            return self.getTypedRuleContext(commandParser.ArgumentContext,0)


        def WHITE_SPACE(self, i:int=None):
            if i is None:
                return self.getTokens(commandParser.WHITE_SPACE)
            else:
                return self.getToken(commandParser.WHITE_SPACE, i)

        def getRuleIndex(self):
            return commandParser.RULE_redirection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRedirection" ):
                listener.enterRedirection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRedirection" ):
                listener.exitRedirection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRedirection" ):
                return visitor.visitRedirection(self)
            else:
                return visitor.visitChildren(self)




    def redirection(self):

        localctx = commandParser.RedirectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_redirection)
        self._la = 0 # Token type
        try:
            self.state = 103
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 87
                self.match(commandParser.T__2)
                self.state = 91
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 88
                    self.match(commandParser.WHITE_SPACE)
                    self.state = 93
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 94
                self.argument()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 95
                self.match(commandParser.T__3)
                self.state = 99
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==5:
                    self.state = 96
                    self.match(commandParser.WHITE_SPACE)
                    self.state = 101
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 102
                self.argument()
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


    class QuotedContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SINGLE_QUOTES(self):
            return self.getToken(commandParser.SINGLE_QUOTES, 0)

        def DOUBLE_QUOTES(self):
            return self.getToken(commandParser.DOUBLE_QUOTES, 0)

        def BACK_QUOTES(self):
            return self.getToken(commandParser.BACK_QUOTES, 0)

        def getRuleIndex(self):
            return commandParser.RULE_quoted

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuoted" ):
                listener.enterQuoted(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuoted" ):
                listener.exitQuoted(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuoted" ):
                return visitor.visitQuoted(self)
            else:
                return visitor.visitChildren(self)




    def quoted(self):

        localctx = commandParser.QuotedContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_quoted)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0):
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





