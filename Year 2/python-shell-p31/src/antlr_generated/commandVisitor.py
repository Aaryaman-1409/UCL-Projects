# Generated from command.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .commandParser import commandParser
else:
    from commandParser import commandParser

# This class defines a complete generic visitor for a parse tree produced by commandParser.

class commandVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by commandParser#command.
    def visitCommand(self, ctx:commandParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#pipe.
    def visitPipe(self, ctx:commandParser.PipeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#sequence.
    def visitSequence(self, ctx:commandParser.SequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#call.
    def visitCall(self, ctx:commandParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#atom.
    def visitAtom(self, ctx:commandParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#argument.
    def visitArgument(self, ctx:commandParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#redirection.
    def visitRedirection(self, ctx:commandParser.RedirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by commandParser#quoted.
    def visitQuoted(self, ctx:commandParser.QuotedContext):
        return self.visitChildren(ctx)



del commandParser