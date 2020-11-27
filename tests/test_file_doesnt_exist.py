import unittest
from unittest.mock import patch, Mock
from cgmerger.cgmerge import main


class TestException(Exception):
    pass


class FileDoesntExist(unittest.TestCase):
    def raise_exception(self, message):
        raise TestException(message)

    def get_default_args(self):
        args_mock = Mock()
        args_mock.file_regex = None
        args_mock.exclude_line_regex = None
        args_mock.output = None
        args_mock.workdir = None
        args_mock.header = None
        args_mock.footer = None
        args_mock.comment = None
        args_mock.order = None
        args_mock.write = False
        return args_mock

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.exists")
    def test_default_output_file_doesnt_exist(self, path_exists, parser):
        path_exists.return_value = False
        args_mock = self.get_default_args()
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        with self.assertRaises(
            TestException, msg='No "codingame.volatile.py" file present in '
        ):
            main()
