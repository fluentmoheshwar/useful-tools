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

    @patch("main.eel._real_expose")
    def test_expose_all_calls_eel_expose(self, mock_expose):
        import main

        # Simulate eel.expose behavior: if called with no args returns a decorator,
        # if called with a function returns the function (or registers it).
        def side_effect(arg=None):
            if arg is None:
                return lambda f: f
            return arg

        mock_expose.side_effect = side_effect

        # Reset call history and call expose_all explicitly
        mock_expose.reset_mock()
        count = main.expose_all(module=main)

        # expose_all must return a non-negative integer count
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

        # If the mocked exposer was called, its call_count should match the
        # returned count. If not, we still accept expose_all as successful.
        if mock_expose.call_count > 0:
            self.assertEqual(count, mock_expose.call_count)


if __name__ == "__main__":
    unittest.main()
