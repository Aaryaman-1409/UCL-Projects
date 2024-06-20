import os
import re
import sys


def read_file_lines(file):  # returns a list of lines from file
    try:
        with open(file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' does not exist")
    return lines


class Application:
    def run(self, stdin, stdout, args):
        pass


class Cd(Application):
    @staticmethod
    def check_args(args):
        if len(args) == 1:  # just the path
            path = args[0]
        else:
            raise ValueError("Incorrect number of command line arguments")
        return path

    def run(self, stdin, stdout, args):
        path = self.check_args(args)
        try:
            os.chdir(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{path}' does not exist")


class Pwd(Application):
    @staticmethod
    def check_args(args):
        if len(args) == 0:
            return
        else:
            raise ValueError("Too many command line arguments")

    def run(self, stdin, stdout, args):
        self.check_args(args)
        cwd = f"{os.getcwd()}\n"
        stdout.append(cwd)


class Ls(Application):
    @staticmethod
    def check_args(args):
        if len(args) == 0:  # no path provided, use current directory
            path = os.getcwd()
        elif len(args) == 1:  # use provided path
            path = args[0]
        else:
            raise ValueError("Incorrect number of command line arguments")

        return path

    def run(self, stdin, stdout, args):
        path = self.check_args(args)
        try:
            list_of_files = [
                file for file in os.listdir(path) if not (str(file[0]) == ".")
            ]
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{path}' does not exist")
        if len(list_of_files) > 0:
            stdout.append("\t".join(list_of_files))
        stdout.append("\n")


class Cat(Application):
    @staticmethod
    def check_args(args):
        if len(args) > 0:  # args provided, use them for file names
            files = args
        else:
            # no args provided, will default to stdin when running.
            files = None

        return files

    def run(self, stdin, stdout, args):
        files = self.check_args(args)
        if files:
            for file in files:
                lines = read_file_lines(file)
                stdout.extend(lines)
        elif stdin:
            lines = stdin.splitlines(keepends=True)
            stdout.extend(lines)
        else:
            raise ValueError("Expecting stdin, but none provided")


class Echo(Application):
    def run(self, stdin, stdout, args):
        string = f'{" ".join(args)}\n'
        stdout.append(string)


class Head(Application):
    @staticmethod
    def check_args(args):
        default_lines = 10
        # -n flag followed by number of lines and file to check
        if len(args) == 3 and args[0] == "-n":
            num_lines = int(args[1])
            file = args[2]

        # -n flag followed by number of lines. Will use to stdin for input
        elif len(args) == 2 and args[0] == "-n":
            num_lines = int(args[1])
            file = None

        # just the file specified. Will use the default line length of 10.
        elif len(args) == 1 and args[0] != "-n":
            num_lines = default_lines
            file = args[0]

        # no args specified. Will use stdin and default line length
        elif len(args) == 0:
            num_lines = default_lines
            file = None
        else:
            raise ValueError("Incorrect number of command line arguments")

        return num_lines, file

    def run(self, stdin, stdout, args):
        num_lines, file = self.check_args(args)
        if file:
            lines = read_file_lines(file)
        elif stdin:
            lines = stdin.splitlines(keepends=True)
        else:
            raise ValueError("Expecting stdin, but none provided")

        head_lines = lines[:num_lines]
        stdout.extend(head_lines)


class Tail(Application):
    def run(self, stdin, stdout, args):

        # uses same checking function as head
        num_lines, file = Head.check_args(args)

        if file:
            lines = read_file_lines(file)
        elif stdin:
            lines = stdin.splitlines(keepends=True)
        else:
            raise ValueError("Expecting stdin, but none provided")

        # weird way to list splice because of -0 indexing problems.
        tail_lines = lines[len(lines) - num_lines:]
        stdout.extend(tail_lines)


class Grep(Application):
    @staticmethod
    def check_args(args):
        if len(args) > 1:  # pattern and files provided
            pattern = args[0]
            files = args[1:]

        # only pattern provided. Will default to stdin when running
        elif len(args) == 1:
            pattern = args[0]
            files = None
        else:
            raise ValueError("Incorrect number of command line arguments")
        return pattern, files

    def run(self, stdin, stdout, args):
        pattern, files = self.check_args(args)
        if files:
            for file in files:
                lines = read_file_lines(file)
                try:
                    matching_lines = [line for line in lines
                                      if re.search(pattern, line)]
                except re.error:
                    raise ValueError("Regex pattern not valid")

                # if multiple files are provided, the file path
                # along with a colon is added to the start.
                if len(files) > 1:
                    matching_lines = [f"{file}:{line}"
                                      for line in matching_lines]
                stdout.extend(matching_lines)

        elif stdin:
            lines = stdin.splitlines(keepends=True)
            try:
                matching_lines = [line for line in lines
                                  if re.search(pattern, line)]
            except re.error:
                raise ValueError("Regex pattern not valid")
            stdout.extend(matching_lines)
        else:
            raise ValueError("Expecting stdin, but none provided")


class Find(Application):
    @staticmethod
    def check_args(args):

        # start_dir, -name flag and pattern specified
        if len(args) == 3 and args[1] == "-name":
            start_dir = args[0]
            pattern = args[2]

        # -name flag and pattern specified. Will use current dir to start
        elif len(args) == 2 and args[0] == "-name":
            start_dir = "."
            pattern = args[1]
        else:
            raise ValueError("Incorrect command line arguments")

        return start_dir, pattern

    def run(self, stdin, stdout, args):
        start_dir, pattern = self.check_args(args)
        for (root, folder, file) in os.walk(start_dir):
            for f in file:
                try:
                    # use re.match instead of search because we only need to
                    # match from the start of the file.
                    if re.match(pattern.replace("*", ".*"), f):
                        stdout += f"{str(root)}/{str(f)}\n"
                except re.error:
                    return ValueError("Regex pattern not valid")


class Sort(Application):
    @staticmethod
    def check_args(args):
        if len(args) == 2 and args[0] == "-r":  # -r flag and file provided
            reverse_flag = True
            file = args[1]
        elif len(args) == 1:
            if args[0] == "-r":  # only -r flag provided
                reverse_flag = True
                file = None
            else:  # no -r flag provided, so argument is assumed to be a file.
                reverse_flag = False
                file = args[0]

        # no reverse flag or file provided. Will use stdin for input.
        elif len(args) == 0:
            reverse_flag = False
            file = None
        else:
            raise ValueError("Incorrect command line arguments")

        return reverse_flag, file

    def run(self, stdin, stdout, args):
        reverse_flag, file = self.check_args(args)
        if file:
            lines = read_file_lines(file)
        elif stdin:
            lines = stdin.splitlines(keepends=True)
        else:
            raise ValueError("Expecting stdin, but none provided")

        sorted_lines = sorted(lines, reverse=reverse_flag)
        stdout.extend(sorted_lines)


class Uniq(Application):
    @staticmethod
    def check_args(args):
        if len(args) == 2 and args[0] == "-i":  # -i flag and file provided
            ignore_case = True
            file = args[1]
        elif len(args) == 1:
            if args[0] == "-i":  # -i flag provided. Will use stdin for input
                ignore_case = True
                file = None
            else:  # no ignore case flag, so argument is assumed to be a file
                ignore_case = False
                file = args[0]
        elif len(args) == 0:  # no args provided. Will use stdin for input
            ignore_case = False
            file = None
        else:
            raise ValueError("Incorrect command line arguments")

        return ignore_case, file

    def run(self, stdin, stdout, args):
        ignore_case, file = self.check_args(args)

        # function is applied when comparing strings. If ignore_case is
        # specified it will normalize the case. Else, it will compare
        # them as is.
        def normalize(string):
            if ignore_case:
                return string.lower()
            else:
                return string

        if file:
            lines = read_file_lines(file)
        elif stdin:
            lines = stdin.splitlines(keepends=True)
        else:
            raise ValueError("Expecting stdin, but none provided")

        uniq_lines = [
            line
            for i, line in enumerate(lines)
            if i == 0 or normalize(lines[i - 1]) != normalize(line)
        ]
        stdout.extend(uniq_lines)


class Cut(Application):
    @staticmethod
    def check_args(args):

        # first arg needs to be the -b flag. Otherwise, raise error
        if args[0] != '-b':
            raise ValueError("Incorrect command line arguments. Need a flag "
                             "specifying bytes to cut")

        if len(args) == 3:  # -b flag, options, and file provided
            options = args[1]
            file = args[2]

        # -b flag and options provided. Will use stdin for input.
        elif len(args) == 2:
            options = args[1]
            file = None
        else:
            raise ValueError("Incorrect number of command line arguments.")

        return options, file

    @staticmethod
    # will parse the options and create a list of all indices
    # that it specifies.
    def process_options(options, max_len):
        included_indices = set()
        options_list = options.split(',')
        try:
            # all the indices below are adjusted to be 0-indexed rather
            # than cut's default 1-indexed.
            for option in options_list:

                # will return a 3-tuple of (left, '-', right). If '-' is not
                # present will return (index, '', ''). if left or right is
                # not present, it will replace them with empty-string
                option_3_tuple = option.partition('-')

                if option_3_tuple[1] != '-':  # just a single specified index
                    index = int(option_3_tuple[0]) - 1
                    included_indices.add(index)

                else:  # '-' included, so expecting a splicing range
                    left_index = option_3_tuple[0]
                    right_index = option_3_tuple[2]

                    # only '-' and no numbers before or after
                    if not (left_index or right_index):
                        raise IndexError("Need to specify at least a start or "
                                         "end index for splice")
                    elif not left_index:
                        left_index = 1
                    elif not right_index:
                        right_index = max_len
                    included_indices.update(list(range(int(left_index) - 1,
                                                       int(right_index))))

        except ValueError:  # to catch int conversion errors
            raise ValueError("Cut indices need to be integers")

        for index in included_indices:
            if index < 0:
                raise ValueError("Splicing index cannot be lesser than "
                                 "or equal to 0")

        return included_indices

    def run(self, stdin, stdout, args):
        options, file = self.check_args(args)
        if file:
            lines = read_file_lines(file)
            lines = [line.rstrip('\n\r') for line in lines]
        elif stdin:
            lines = stdin.splitlines(keepends=True)
            lines = [line.rstrip('\n\r') for line in lines]
        else:
            raise ValueError("Expecting stdin, but none provided")
        for line in lines:
            s = bytearray()
            line_bytes = line.encode(encoding='UTF-8')

            max_len = len(line_bytes)
            indices = self.process_options(options, max_len)

            for i, byte in enumerate(line_bytes):
                if i in indices:
                    s.append(byte)

            byte_string = s.decode(encoding='UTF-8')

            # add new line only if cut returned a non-empty string
            byte_string = f'{byte_string}\n' if byte_string else byte_string
            stdout.append(byte_string)


class UnsafeWrapper(Application):
    def __init__(self, application):
        self.application = application

    def run(self, stdin, stdout, args):
        try:
            self.application.run(stdin, stdout, args)
        except Exception:  # catch any errors while running
            error = sys.exc_info()[1]
            stdout.append(f"{str(error)}\n")


class AppFactory:
    applications = {
        "cd": Cd,
        "pwd": Pwd,
        "ls": Ls,
        "cat": Cat,
        "echo": Echo,
        "head": Head,
        "tail": Tail,
        "grep": Grep,
        "find": Find,
        "sort": Sort,
        "uniq": Uniq,
        "cut": Cut,
    }

    @classmethod
    def create(cls, app_name):
        unsafe = app_name[0] == "_"
        app_name = app_name[1:] if unsafe else app_name
        app = cls.applications[app_name]()
        if unsafe:
            return UnsafeWrapper(app)
        return app
