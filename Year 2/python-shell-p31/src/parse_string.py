import re
from glob import glob

import antlr4

from antlr_generated.commandLexer import commandLexer
from antlr_generated.commandParser import commandParser
from antlr_generated.commandVisitor import commandVisitor
from command_types import Command, Call, Pipe, Sequence


def evaluate_sub_shell_command(command):
    parser = commandParser(
        antlr4.CommonTokenStream(commandLexer(antlr4.InputStream(command)))
    )
    tree = parser.command()
    sub_shell_command = tree.accept(ParseString())
    stdout = []
    sub_shell_command.eval(None, stdout)
    return "".join(stdout).strip()


class ParseString(commandVisitor):
    # We use the word node to refer to antlr generated contexts
    # in the functions below

    def visitCommand(self, node):
        call = self.visitCall(node.call())
        if node.pipe():
            pipe_command = self.visitPipe(call, node.pipe())
            command = pipe_command
        elif node.sequence():
            sequence_command = Sequence(call)
            self.visitSequence(sequence_command, node.sequence())
            command = sequence_command
        else:
            command = call
        return command

    def visitCall(self, node):
        args = []
        stdin, stdout = [], []

        if node is None:
            return Command()

        self.visitArgument(node.argument(), args)
        if len(args) == 0:
            return Command()

        self.visitAtom(node.atom(), args, stdin, stdout)

        for redirections in node.redirection():
            self.visitRedirection(redirections, stdin, stdout)

        if len(stdin) > 1 or len(stdout) > 1:
            raise ValueError("Only one file can be specified for redirections")

        app_name = args.pop(0)

        # setting stdin and stdout to None if they are empty
        stdin = stdin[0] if stdin else None
        stdout = stdout[0] if stdout else None

        return Call(app_name, args, stdin, stdout)

    def visitPipe(self, command, node):
        # sets left and right hand side of pipe to command
        pipe = Pipe(command, self.visitCall(node.call()))
        if node.pipe():
            # recursively sets left and right hand side of pipe.
            return self.visitPipe(pipe, node.pipe())
        else:
            return pipe

    def visitSequence(self, sequence, node):
        sub_command = self.visitCall(node.call())
        if node.pipe():
            sub_command = self.visitPipe(sub_command, node.pipe())
        sequence.add_command(sub_command)
        if node.sequence():
            self.visitSequence(sequence, node.sequence())

    def visitAtom(self, node, args, stdin, stdout):
        redirections = list(filter(lambda x: x.redirection(), node))
        arguments = list(filter(lambda x: x.argument(), node))

        if redirections:
            for redirection in redirections:
                self.visitRedirection(redirection.redirection(), stdin, stdout)

        for child in arguments:
            self.visitArgument(child.argument(), args)

    # This visits a single argument. Thus, there will be no whitespace
    # unless it is inside a quote
    def visitArgument(self, node, args):
        if node is None:
            return

        new_args = [""]

        # To understand implementation, consider the example:
        # echo `echo a b`"c a", which will make new_args equal to ['a', 'bc a']
        for child in node.getChildren():
            if type(child) is commandParser.QuotedContext:
                quoted_list = self.visitQuoted(child)

                # merge string of last new_arg with first string
                # of returned list
                new_args[-1] += quoted_list[0]

                # In the case of backquotes, which can return a multi-element
                # list, extend new_args with the rest of returned list.
                new_args.extend(quoted_list[1:])
            else:
                globbed_list = [child.getText()]
                arg = globbed_list[0]
                if "*" in arg:
                    globbed = list(glob(arg))

                    # replace glob with globbed list if globbed paths exist.
                    # Else, the list will just be left with the original glob.
                    if globbed:
                        globbed_list[0:1] = globbed

                # Similar to quoted version. Merge first element with the last
                # element of new_args, and extend the rest.
                new_args[-1] += globbed_list[0]
                new_args.extend(globbed_list[1:])

        # add the new args to the existing set of args
        args.extend(new_args)

    def visitRedirection(self, node, stdin, stdout):
        sign = node.getChild(0).getText()
        filename = node.argument().getText()
        if sign == "<":
            stdin.append(filename)
        elif sign == ">":
            stdout.append(filename)

    def visitQuoted(self, node):
        if node.SINGLE_QUOTES():
            return [str(node.SINGLE_QUOTES())[1:-1]]

        elif node.BACK_QUOTES():
            backquoted_cmd = str(node.BACK_QUOTES())[1:-1]
            new_args = evaluate_sub_shell_command(backquoted_cmd)
            new_args = new_args.replace("\n", " ")
            new_args = new_args.strip()
            return new_args.split(" ")

        elif node.DOUBLE_QUOTES():
            double_quoted = str(node.DOUBLE_QUOTES())[1:-1]
            backquoted_strings = re.findall("`[^`]*`", double_quoted)
            if len(backquoted_strings) > 0:
                for backquoted in backquoted_strings:
                    sub_command = backquoted[1:-1]
                    new_args = evaluate_sub_shell_command(sub_command)
                    double_quoted = double_quoted.replace(backquoted,
                                                          new_args, 1)

            return [double_quoted]
