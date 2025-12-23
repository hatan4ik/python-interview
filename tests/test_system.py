import subprocess
import unittest
from unittest.mock import patch, MagicMock
from devops_toolkit.system import run_command, check_binary_exists

class TestSystemOperations(unittest.TestCase):

    @patch("devops_toolkit.system.shutil.which")
    def test_check_binary_exists(self, mock_which):
        mock_which.return_value = "/usr/bin/kubectl"
        self.assertTrue(check_binary_exists("kubectl"))

        mock_which.return_value = None
        self.assertFalse(check_binary_exists("missing_tool"))

    @patch("devops_toolkit.system.subprocess.run")
    def test_run_command_success(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ls", "-l"], returncode=0, stdout="file.txt\n", stderr=""
        )

        result = run_command(["ls", "-l"], capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "file.txt\n")
        
        # Verify call arguments
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(kwargs["shell"], False)
        self.assertEqual(kwargs["check"], True)

    @patch("devops_toolkit.system.subprocess.run")
    def test_run_command_failure(self, mock_run):
        # Simulate a command failure
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="ls -z", stderr="invalid option"
        )

        with self.assertRaises(subprocess.CalledProcessError):
            run_command("ls -z", shell=True)

    @patch("devops_toolkit.system.subprocess.run")
    def test_run_command_no_check(self, mock_run):
        # Simulate failure but with check=False
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="ls -z", stderr="invalid option"
        )
        
        # Should return the exception object instead of raising it
        result = run_command("ls -z", shell=True, check=False)
        self.assertIsInstance(result, subprocess.CalledProcessError)

if __name__ == "__main__":
    unittest.main()
