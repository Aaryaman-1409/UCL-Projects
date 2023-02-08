# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .commandParser import commandParser
else:
    from commandParser import commandParser

# This class defines a complete listener for a parse tree produced by commandParser.
class commandListener(ParseTreeListener):

    # Enter a parse tree produced by commandParser#command.
    def enterCommand(self, ctx:commandParser.CommandContext):
        pass

    # Exit a parse tree produced by commandParser#command.
    def exitCommand(self, ctx:commandParser.CommandContext):
        pass


    # Enter a parse tree produced by commandParser#pipe.
    def enterPipe(self, ctx:commandParser.PipeContext):
        pass

    # Exit a parse tree produced by commandParser#pipe.
    def exitPipe(self, ctx:commandParser.PipeContext):
        pass


    # Enter a parse tree produced by commandParser#sequence.
    def enterSequence(self, ctx:commandParser.SequenceContext):
        pass

    # Exit a parse tree produced by commandParser#sequence.
    def exitSequence(self, ctx:commandParser.SequenceContext):
        pass


    # Enter a parse tree produced by commandParser#call.
    def enterCall(self, ctx:commandParser.CallContext):
        pass

    # Exit a parse tree produced by commandParser#call.
    def exitCall(self, ctx:commandParser.CallContext):
        pass


    # Enter a parse tree produced by commandParser#atom.
    def enterAtom(self, ctx:commandParser.AtomContext):
        pass

    # Exit a parse tree produced by commandParser#atom.
    def exitAtom(self, ctx:commandParser.AtomContext):
        pass


    # Enter a parse tree produced by commandParser#argument.
    def enterArgument(self, ctx:commandParser.ArgumentContext):
        pass

    # Exit a parse tree produced by commandParser#argument.
    def exitArgument(self, ctx:commandParser.ArgumentContext):
        pass


    # Enter a parse tree produced by commandParser#redirection.
    def enterRedirection(self, ctx:commandParser.RedirectionContext):
        pass

    # Exit a parse tree produced by commandParser#redirection.
    def exitRedirection(self, ctx:commandParser.RedirectionContext):
        pass


    # Enter a parse tree produced by commandParser#quoted.
    def enterQuoted(self, ctx:commandParser.QuotedContext):
        pass

    # Exit a parse tree produced by commandParser#quoted.
    def exitQuoted(self, ctx:commandParser.QuotedContext):
        pass



del commandParser