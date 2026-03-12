import unittest
from unittest.mock import patch, MagicMock


class RunCommandTests(unittest.TestCase):
    @patch("subprocess.run")
    def test_list_uses_shell_false(self, mock_run):
        from main import run_command

        cp = MagicMock()
        cp.returncode = 0
        cp.stdout = "ok"
        mock_run.return_value = cp

        res = run_command(["echo", "hi"], capture_output=True)

        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], ["echo", "hi"])
        self.assertFalse(kwargs.get("shell"))
        self.assertEqual(res.stdout, "ok")

    @patch("subprocess.run")
    def test_string_needs_shell_on_envvar(self, mock_run):
        from main import run_command

        cp = MagicMock()
        cp.returncode = 0
        mock_run.return_value = cp

        res = run_command("echo %PATH%", capture_output=True)

        mock_run.assert_called_once()
        _, kwargs = mock_run.call_args
        self.assertTrue(kwargs.get("shell"))

    def test_invalid_inputs(self):
        from main import run_command

        with self.assertRaises(ValueError):
            run_command("")

        with self.assertRaises(TypeError):
            run_command(123)

        with self.assertRaises(TypeError):
            run_command([1, 2])


if __name__ == "__main__":
    unittest.main()
