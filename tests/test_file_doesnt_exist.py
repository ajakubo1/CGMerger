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

    def path_exists_wrapper(self, **kwargs):
        def real_path_exists(path: str):
            return kwargs.get(path, False)

        return real_path_exists

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.exists")
    def test_default_output_file_doesnt_exist(self, path_exists, parser):
        path_exists.return_value = False
        args_mock = self.get_default_args()
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        with self.assertRaisesRegex(
            TestException, 'No "codingame.volatile.py" file present in '
        ):
            main()

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.exists")
    def test_custom_output_file_doesnt_exist(self, path_exists, parser):
        path_exists.return_value = False
        args_mock = self.get_default_args()
        args_mock.output = "very_custom_file.py"
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        with self.assertRaisesRegex(
            TestException, f'No "{args_mock.output}" file present in '
        ):
            main()

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.isfile")
    @patch("cgmerger.cgmerge.os.path.isdir")
    def test_default_workdir_doesnt_exist(self, is_dir, path_exists, parser):
        path_exists.return_value = True
        is_dir.return_value = False
        args_mock = self.get_default_args()
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        with self.assertRaisesRegex(
            TestException, 'No "codingame/" directory present in '
        ):
            main()

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.isfile")
    @patch("cgmerger.cgmerge.os.path.isdir")
    def test_custom_workdir_doesnt_exist(self, is_dir, path_exists, parser):
        path_exists.return_value = True
        is_dir.return_value = False
        args_mock = self.get_default_args()
        args_mock.workdir = "very_custom_folder/"
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        with self.assertRaisesRegex(
            TestException, f'No "{args_mock.workdir}" directory present in '
        ):
            main()

    @patch("cgmerger.cgmerge.parser")
    @patch("cgmerger.cgmerge.os.path.isfile")
    @patch("cgmerger.cgmerge.os.path.isdir")
    @patch("cgmerger.cgmerge.os.listdir")
    @patch("cgmerger.cgmerge.open")
    def test_create_default_output(self, open, listdir, is_dir, path_exists, parser):
        path_exists.return_value = True
        is_dir.return_value = True
        listdir.return_value = []
        args_mock = self.get_default_args()
        parser.error = self.raise_exception
        parser.parse_args.return_value = args_mock
        main()
        open.assert_called_once_with("codingame.volatile.py", "w")
