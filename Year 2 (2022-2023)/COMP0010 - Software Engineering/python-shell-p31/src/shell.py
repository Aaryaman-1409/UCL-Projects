import os
import pwd
import socket
import sys

import antlr4

from antlr_generated.commandLexer import commandLexer
from antlr_generated.commandParser import commandParser
from parse_string import ParseString


def run(command_str, output=None):
    parser = commandParser(
        antlr4.CommonTokenStream(commandLexer(antlr4.InputStream(command_str)))
    )
    tree = parser.command()
    command = tree.accept(ParseString())
    command.eval(None, output)


if __name__ == "__main__":  # pragma: no cover
    args_len = len(sys.argv) - 1
    if args_len == 0:
        while True:
            prompt_username = (
                f'{pwd.getpwuid(os.getuid())[0]}@'
                f'{socket.gethostname().split(".")[0]}'
            )
            print(f"{prompt_username} {os.getcwd()} $ ", end="")
            command_string = input()
            run(command_string)
    elif args_len == 2 and sys.argv[1] == "-c":
        run(sys.argv[2])
    else:
        raise ValueError("Incorrect number of command line arguments")
