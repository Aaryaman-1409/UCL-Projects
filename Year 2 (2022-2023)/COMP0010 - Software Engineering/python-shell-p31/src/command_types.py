from applications import AppFactory


def stdout_to_str(stdout):
    s = ""
    for strs in stdout:
        s += strs
    return s


def read_from_file(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find the file: {filename}")


class Command:
    def eval(self, stdin=None, stdout=None):
        return


class Call(Command):
    def __init__(self, app_name, args, redirect_stdin, redirect_stdout):
        self.app = AppFactory.create(app_name)
        self.args = args or []
        self.redirect_stdin = read_from_file(redirect_stdin) \
            if redirect_stdin else None
        self.redirect_stdout = redirect_stdout or None

    def eval(self, stdin=None, stdout=None):
        output = []

        # order of preference. Stdin in bash prefers redirection to other
        # forms of stdin or stdout (pipe, sequence)
        app_stdin = self.redirect_stdin or stdin or None
        app_stdout = stdout if stdout is not None else output

        # Execute the app
        self.app.run(app_stdin, app_stdout, self.args)

        # a redirection file is provided
        if self.redirect_stdout is not None:
            with open(self.redirect_stdout, "w") as f:
                f.write(stdout_to_str(output))

        # a stdout was not provided by a pipe or sequence etc.
        # In that case just print the output.
        elif stdout is None:
            print(stdout_to_str(output))


class Pipe(Command):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, stdin=None, stdout=None):
        content_list = []

        # passes list as stdout to it's left hand side
        self.left.eval(stdin, content_list)

        # reads the list and passes it in as stdin to the right hand sie
        new_input = stdout_to_str(content_list) or None
        self.right.eval(new_input, stdout)


class Sequence(Command):
    def __init__(self, initial_command):
        self.commands = [initial_command]

    def add_command(self, command):
        self.commands.append(command)

    def eval(self, stdin=None, stdout=None):
        for command in self.commands:
            command.eval(stdout=stdout)
