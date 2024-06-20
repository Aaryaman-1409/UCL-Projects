import os
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from src.applications import AppFactory
from src.command_types import stdout_to_str


class TestCd(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("cd")
        self.start_dir = os.getcwd()
        self.dir = TemporaryDirectory(dir=os.getcwd())

    def tearDown(self):
        self.dir.cleanup()
        os.chdir(self.start_dir)

    def test_cd(self):
        stdin, stdout, args = None, [], [self.dir.name]
        self.app.run(stdin, stdout, args)
        assert os.getcwd() == self.dir.name

    def test_cd_blank(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], []
            self.app.run(stdin, stdout, args)

    def test_cd_excessive_args(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], ["dir1", "dir2"]
            self.app.run(stdin, stdout, args)

    def test_cd_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            stdin, stdout, args = None, [], ["random"]
            self.app.run(stdin, stdout, args)


class TestPwd(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("pwd")

    def test_pwd(self):
        stdin, stdout, args = None, [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip()
        self.assertEqual(stdout, os.getcwd())

    def test_pwd_with_args(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], ["random"]
            self.app.run(stdin, stdout, args)


class TestLs(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("ls")
        self.dir = TemporaryDirectory(dir=os.getcwd())
        self.dir2 = TemporaryDirectory(dir=os.getcwd())
        self.file1 = NamedTemporaryFile(mode="r", dir=self.dir.name)
        self.file2 = NamedTemporaryFile(mode="r", dir=self.dir.name)

    def tearDown(self):
        self.file2.close()
        self.file1.close()
        self.dir.cleanup()
        self.dir2.cleanup()

    def test_ls_blank(self):
        stdin, stdout, args = None, [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip().split()
        actual_list = list(
            filter(lambda x: x[0] != ".", list(os.listdir("."))))
        self.assertEqual(stdout, actual_list)

    def test_ls_with_dir(self):
        stdin, stdout, args = None, [], [self.dir.name]
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split())
        actual_files = {os.path.basename(self.file1.name),
                        os.path.basename(self.file2.name)}
        self.assertEqual(stdout, actual_files)

    def test_ls_empty_dir(self):
        stdin, stdout, args = None, [], [self.dir2.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip().split()
        actual_files = []
        self.assertEqual(stdout, actual_files)

    def test_ls_invalid_dir(self):
        with self.assertRaises(FileNotFoundError):
            stdin, stdout, args = None, [], ['random']
            self.app.run(stdin, stdout, args)

    def test_ls_excessive_args(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], ["dir1", "dir2"]
            self.app.run(stdin, stdout, args)


class TestCat(unittest.TestCase):
    def setUp(self):
        self.cat = AppFactory.create("cat")
        self.file1 = NamedTemporaryFile("r+", delete=False)
        self.file1.writelines([str(i) + "\n" for i in range(0, 50)])
        self.file1.close()
        self.file2 = NamedTemporaryFile("r+", delete=False)
        self.file2.writelines([str(i) + "\n" for i in range(50, 100)])
        self.file2.close()

    def tearDown(self):
        os.unlink(self.file1.name)
        os.unlink(self.file2.name)

    def test_cat_file(self):
        stdin, stdout, args = None, [], [self.file1.name]
        self.cat.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        self.assertEqual(stdout, [str(i) for i in range(0, 50)])

    def test_cat_invalid_file(self):
        stdin, stdout, args = None, [], ["random"]
        with self.assertRaises(FileNotFoundError):
            self.cat.run(stdin, stdout, args)

    def test_cat_blank(self):
        stdin, stdout, args = "random", [], []
        self.cat.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")
        self.assertEqual(stdout, ["random"])

    def test_cat_blank_no_stdin(self):
        stdin, stdout, args = None, [], []
        with self.assertRaises(ValueError):
            self.cat.run(stdin, stdout, args)

    def test_cat_multiple_files(self):
        stdin, stdout, args = None, [], [self.file1.name, self.file2.name]
        self.cat.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        self.assertEqual(stdout, [str(i) for i in range(0, 100)])


class TestEcho(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("echo")

    def test_echo_blank(self):
        stdin, stdout, args = None, [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip()
        self.assertEqual(stdout, "")

    def test_echo_one_args(self):
        stdin, stdout, args = None, [], ["test"]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip()
        self.assertEqual(stdout, "test")

    def test_echo_multiple(self):
        stdin, stdout, args = None, [], ["test1", "test2"]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip()
        self.assertEqual(stdout, "test1 test2")


class TestHead(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("head")
        self.file1 = NamedTemporaryFile("r+", delete=False)
        self.file1.writelines([str(i) + "\n" for i in range(0, 100)])
        self.file1.close()

    def tearDown(self):
        os.unlink(self.file1.name)

    def test_head_file_default_lines(self):
        stdin, stdout, args = None, [], [self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(0, 10)])

    def test_head_file_flag_0(self):
        stdin, stdout, args = None, [], ["-n", 0, self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [])

    def test_head_file_flag_nonzero(self):
        stdin, stdout, args = None, [], ["-n", 10, self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(10)])

    def test_head_invalid_file(self):
        stdin, stdout, args = None, [], ["-n", 10, "random"]
        with self.assertRaises(FileNotFoundError):
            self.app.run(stdin, stdout, args)

    def test_head_only_flag(self):
        stdin = "\n".join([str(i) for i in range(0, 100)])
        stdout = []
        args = ["-n", 10]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(10)])

    def test_head_invalid_args(self):
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-d", "10", self.file1.name]
            self.app.run(stdin, stdout, args)
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-d", "10"]
            self.app.run(stdin, stdout, args)
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-n", "10", self.file1.name, "invalid"]
            self.app.run(stdin, stdout, args)

    def test_head_no_args(self):
        stdin = "\n".join([str(i) for i in range(0, 100)])
        stdout, args = [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip().split()
        self.assertEqual(stdout, [str(i) for i in range(0, 10)])

    def test_head_no_args_no_stdin(self):
        stdin, stdout, args = None, [], []
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)


class TestTail(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("tail")
        self.file1 = NamedTemporaryFile("r+", delete=False)
        self.file1.writelines([str(i) + "\n" for i in range(0, 100)])
        self.file1.close()

    def tearDown(self):
        os.unlink(self.file1.name)

    def test_tail_file_default_lines(self):
        stdin, stdout, args = None, [], [self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(90, 100)])

    def test_tail_file_flag_0(self):
        stdin, stdout, args = None, [], ["-n", 0, self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [])

    def test_tail_file_flag_nonzero(self):
        stdin, stdout, args = None, [], ["-n", 10, self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(90, 100)])

    def test_tail_invalid_file(self):
        stdin, stdout, args = None, [], ["-n", 10, "random"]
        with self.assertRaises(FileNotFoundError):
            self.app.run(stdin, stdout, args)

    def test_tail_only_flag(self):
        stdin = "\n".join([str(i) for i in range(0, 100)])
        stdout = []
        args = ["-n", 10]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, [str(i) for i in range(90, 100)])

    def test_tail_invalid_args(self):
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-d", "10", self.file1.name]
            self.app.run(stdin, stdout, args)
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-d", "10"]
            self.app.run(stdin, stdout, args)
        with self.assertRaises(ValueError):
            stdin = None
            stdout = []
            args = ["-n", "10", self.file1.name, "invalid"]
            self.app.run(stdin, stdout, args)

    def test_tail_no_args(self):
        stdin = "\n".join([str(i) for i in range(0, 100)])
        stdout, args = [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip().split()
        self.assertEqual(stdout, [str(i) for i in range(90, 100)])

    def test_tail_no_args_no_stdin(self):
        stdin, stdout, args = None, [], []
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)


class TestGrep(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("grep")
        self.dir1 = TemporaryDirectory(dir=os.getcwd())
        self.dir2 = TemporaryDirectory(dir=os.getcwd())
        self.file1 = NamedTemporaryFile(mode="r+", dir=self.dir1.name)
        self.file2 = NamedTemporaryFile(mode="r+", dir=self.dir2.name)
        self.file1.write("AAA\nAAA\nBBB\n")
        self.file2.write("AAA\nAAA\nBBB\n")
        self.file1.seek(0)
        self.file2.seek(0)

    def tearDown(self):
        self.file1.close()
        self.file2.close()
        self.dir1.cleanup()
        self.dir2.cleanup()

    def test_grep_no_match(self):
        stdin, stdout, args = None, [], ["DDD", self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        self.assertEqual(stdout, [])

    def test_grep_match(self):
        stdin, stdout, args = None, [], ["AAA", self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        self.assertEqual(stdout, ["AAA", "AAA"])

    def test_grep_regex(self):
        stdin, stdout, args = None, [], ["A..", self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        self.assertEqual(stdout, ["AAA", "AAA"])

    def test_grep_multiple_files(self):
        stdin, stdout, args = None, [], ["BBB", self.file1.name,
                                         self.file2.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        expected = [
                   f"{self.file1.name}:BBB",
                   f"{self.file2.name}:BBB"]
        self.assertEqual(stdout, expected)

    def test_grep_no_file(self):
        stdin, stdout, args = "DDD", [], ["DDD"]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[0]
        self.assertEqual(stdout, "DDD")

    def test_grep_invalid_args(self):
        stdin, stdout, args = "DDD", [], []
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)

    def test_grep_invalid_regex(self):
        stdin, stdout, args = None, [], ["*", self.file1.name]
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)


class TestFind(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("find")
        self.dir1 = TemporaryDirectory(dir=os.getcwd())
        self.dir2 = TemporaryDirectory(dir=os.getcwd())
        self.file1 = NamedTemporaryFile(mode="r+",
                                        dir=self.dir1.name,
                                        suffix=".txt",
                                        prefix="random")
        self.file2 = NamedTemporaryFile(mode="r+",
                                        dir=self.dir2.name,
                                        suffix=".txt",
                                        prefix="random")

    def tearDown(self):
        self.file1.close()
        self.file2.close()
        self.dir1.cleanup()
        self.dir2.cleanup()

    def test_no_find_from_current_dir(self):
        stdin, stdout, args = [], [], ["-name", "xyz"]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")
        self.assertEqual(stdout, [''])

    def test_find_from_current_dir(self):
        cwd = os.getcwd()
        stdin, stdout, args = None, [], ["-name", "random"]
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split("\n"))
        expected = set(map(lambda el: el.replace(cwd, '.', 1),
                           [self.file1.name, self.file2.name]))
        self.assertEqual(expected, stdout)

    def test_find_insufficient_args(self):
        stdin, stdout, args = None, [], ["-name"]
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)


class TestSort(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create("sort")
        self.dir = TemporaryDirectory(dir=os.getcwd())
        self.file = NamedTemporaryFile(mode="r+",
                                       dir=self.dir.name,
                                       suffix=".txt",
                                       prefix="file")
        self.file.write("AAA\nAAA\nBBB\n")
        self.file.seek(0)

    def tearDown(self):
        self.file.close()
        self.dir.cleanup()

    def test_sort(self):
        stdin, stdout, args = None, [], [self.file.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        expected = ["AAA", "AAA", "BBB"]
        self.assertEqual(stdout, expected)

    def test_sort_stdin(self):
        stdin, stdout, args = "AAA BBB AAA", [], []
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")
        expected = ["AAA BBB AAA"]
        self.assertEqual(stdout, expected)

    def test_sort_reverse(self):
        stdin, stdout, args = None, [], ["-r", self.file.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split("\n")[:-1]
        expected = ["BBB", "AAA", "AAA"]
        self.assertEqual(stdout, expected)

    def test_sort_wrong_flags(self):
        stdin, stdout, args = None, [], ["-a", "-b"]
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)

    def test_sort_empty_stdin(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], []
            self.app.run(stdin, stdout, args)

    def test_sort_invalid_filename(self):
        stdin, stdout, args = None, [], ["random"]
        with self.assertRaises(FileNotFoundError):
            self.app.run(stdin, stdout, args)


class TestUniq(unittest.TestCase):

    def setUp(self):
        self.app = AppFactory.create('uniq')
        self.file1 = NamedTemporaryFile(mode='r+', dir=os.getcwd())
        lines = ["line1\n", "line1\n", "LINE1\n", "line2\n", "Line2\n"]
        self.file1.writelines(lines)
        self.file1.seek(0)

    def test_uniq_invalid_file(self):
        stdin, stdout, args = None, [], ["random"]
        with self.assertRaises(FileNotFoundError):
            self.app.run(stdin, stdout, args)

    def test_uniq_file_no_flag(self):
        stdin, stdout, args = None, [], [self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split())
        self.assertEqual(stdout, {'line1', 'LINE1', 'line2', 'Line2'})

    def test_uniq_file_flag(self):
        stdin, stdout, args = None, [], ['-i', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split())
        self.assertEqual(stdout, {'line1', 'line2'})

    def test_uniq_stdin(self):
        stdin, stdout, args = "line1\nline1\nline2\nline2\n", [], []
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split())
        self.assertEqual(stdout, {'line1', 'line2'})

    def test_uniq_stdin_and_flag(self):
        stdin, stdout, args = "line1\nLine1\nline2\nLINE2\n", [], ["-i"]
        self.app.run(stdin, stdout, args)
        stdout = set(stdout_to_str(stdout).strip().split())
        self.assertEqual(stdout, {'line1', 'line2'})

    def test_uniq_file_invalid_args(self):
        stdin, stdout, args = None, [], ['-random', self.file1.name]
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)

    def test_uniq_excessive_args(self):
        args = ['-a', '-b', '-c']
        stdin = "line1\nLine1\nline2\nLINE2\n"
        stdout = []
        with self.assertRaises(ValueError):
            self.app.run(stdin, stdout, args)


class TestCut(unittest.TestCase):
    def setUp(self):
        self.app = AppFactory.create('cut')
        self.file1 = NamedTemporaryFile(mode="r+")  # deleted dir
        self.file1.write("123456789\n123456789\n123456789")
        self.file1.seek(0)

    def tearDown(self):
        self.file1.close()

    def test_cut_no_flag(self):
        with self.assertRaises(ValueError):
            stdin, stdout, args = None, [], [self.file1.name]
            self.app.run(stdin, stdout, args)

    def test_cut_arg_and_stdin(self):
        stdin, stdout, args = "test", [], ['-b', '1']
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).strip()
        self.assertEqual(stdout, 't')

    def test_cut_arg(self):
        stdin, stdout, args = None, [], ['-b', '1', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, ["1", "1", "1"])

    def test_cut_range(self):
        stdin, stdout, args = None, [], ['-b', '4-7', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, ["4567", "4567", "4567"])

    def test_cut_right_range(self):
        stdin, stdout, args = None, [], ['-b', '-5', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, ["12345", "12345", "12345"])

    def test_cut_left_range(self):
        stdin, stdout, args = None, [], ['-b', '8-', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, ["89", "89", "89"])

    def test_cut_multiple_range(self):
        stdin, stdout, args = None, [], ['-b', '-3,4-5,9-', self.file1.name]
        self.app.run(stdin, stdout, args)
        stdout = stdout_to_str(stdout).split()
        self.assertEqual(stdout, ["123459", "123459", "123459"])


if __name__ == "__main__":
    unittest.main()
