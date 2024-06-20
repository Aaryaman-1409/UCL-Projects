import os
import unittest
from tempfile import NamedTemporaryFile

from src.shell import run
from src.command_types import stdout_to_str


class TestShellApp(unittest.TestCase):
    def test_blank(self):
        stdout = []
        run("", stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual("", out)

    def test_invalid_application(self):
        stdout = []
        with self.assertRaises(Exception):
            run("random", stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual("", out)


class TestQuoting(unittest.TestCase):
    def test_quoted_single(self):
        text = "\"''\""
        stdout = []
        run(f'echo {text}', stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, "''")

    def test_double_quoted_single(self):
        text = "\"\""
        stdout = []
        run(f'echo {text}', stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, "")


class TestCmdSubstitution(unittest.TestCase):
    def simple_cmd_substitution(self):
        cmd = "echo `echo test`"
        stdout = []
        run(cmd, stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, "test")

    def test_cmd_substitution_with_double_quotes(self):
        text = "\"`echo test` abc\""
        stdout = []
        run(f'echo {text}', stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, "test abc")


class TestRedirection(unittest.TestCase):
    def test_redirection_output(self):
        text = 'test'
        file1 = NamedTemporaryFile(mode="r+", dir=os.getcwd())
        run(f"echo {text} > {file1.name}")
        out = file1.readlines()[0].strip()
        self.assertEqual(out, text)
        file1.close()

    def test_redirection_input(self):
        text = "test"
        file = NamedTemporaryFile("r+", dir=os.getcwd())
        file.write(text)
        file.seek(0)
        stdout = []
        run(f"cat < {file.name}", output=stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, text)
        file.close()

    def test_redirection_input_before_call(self):
        text = "test"
        file = NamedTemporaryFile("r+", dir=os.getcwd())
        file.write(text)
        file.seek(0)
        stdout = []
        run(f"< {file.name} cat", output=stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, text)
        file.close()

    def test_multiple_redirections_output(self):
        with self.assertRaises(ValueError):
            run("echo test > file1.txt > file2.txt > file3.txt")

    def test_multiple_redirections_input(self):
        with self.assertRaises(ValueError):
            run("cat < file1.txt < file2.txt < file3.txt")

    def test_redirection_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            run("cat < random.txt")


class TestCommands(unittest.TestCase):
    def test_sequence(self):
        stdout = []
        run("echo 'test'; echo test1; echo test2", stdout)
        out = stdout_to_str(stdout).strip().split()
        self.assertEqual(out, ['test', 'test1', 'test2'])

    def test_pipe(self):
        cmdline = "echo abc | cat"
        stdout = []
        run(cmdline, output=stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, "abc")

    def test_sequence_with_pipe(self):
        stdout = []
        run("echo test; echo abc | cat", stdout)
        out = stdout_to_str(stdout).strip().split()
        self.assertEqual(out, ['test', 'abc'])


class TestGlobbing(unittest.TestCase):
    def test_globbing(self):
        file = NamedTemporaryFile('r+', dir=os.getcwd(), suffix='.test')
        file.write('test1')
        file.seek(0)
        stdout = []
        run("cat *.test", output=stdout)
        file.close()
        out = stdout_to_str(stdout)
        self.assertEqual(out, 'test1')


class TestUnsafe(unittest.TestCase):
    def test_unsafe_wrapper(self):
        stdout = []
        path = "random"
        run(f"_cd {path}", stdout)
        out = stdout_to_str(stdout).strip()
        self.assertEqual(out, f"File '{path}' does not exist")

    def test_unsafe_sequence(self):
        stdout = []
        path = "random"
        run(f"_cat {path}; echo text2", stdout)
        out = stdout_to_str(stdout).strip().split("\n")
        self.assertEqual(out, [f"File '{path}' does not exist", "text2"])


if __name__ == "__main__":
    unittest.main()
