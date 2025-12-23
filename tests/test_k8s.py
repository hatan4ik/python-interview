import unittest
import subprocess
from unittest.mock import patch, MagicMock
from devops_toolkit.k8s.operations import check_minikube_running, start_minikube, ensure_namespace

class TestK8sOperations(unittest.TestCase):

    @patch("devops_toolkit.k8s.operations.check_binary_exists")
    @patch("devops_toolkit.k8s.operations.run_command")
    def test_check_minikube_running_true(self, mock_run, mock_check_bin):
        mock_check_bin.return_value = True
        # run_command succeeds
        mock_run.return_value = MagicMock(returncode=0)
        
        self.assertTrue(check_minikube_running())

    @patch("devops_toolkit.k8s.operations.check_binary_exists")
    @patch("devops_toolkit.k8s.operations.run_command")
    def test_check_minikube_running_false(self, mock_run, mock_check_bin):
        mock_check_bin.return_value = True
        # run_command fails
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="minikube status")
        
        self.assertFalse(check_minikube_running())

    @patch("devops_toolkit.k8s.operations.check_minikube_running")
    @patch("devops_toolkit.k8s.operations.run_command")
    def test_start_minikube_already_running(self, mock_run, mock_check_running):
        mock_check_running.return_value = True
        start_minikube()
        # Should NOT call start command
        mock_run.assert_not_called()

    @patch("devops_toolkit.k8s.operations.check_minikube_running")
    @patch("devops_toolkit.k8s.operations.run_command")
    def test_start_minikube_needs_start(self, mock_run, mock_check_running):
        mock_check_running.return_value = False
        start_minikube()
        # Should call start command
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        self.assertIn("minikube start", args[0])

    @patch("devops_toolkit.k8s.operations.run_command")
    def test_ensure_namespace_exists(self, mock_run):
        # First call succeeds (namespace exists)
        mock_run.return_value = MagicMock(returncode=0)
        
        ensure_namespace("existing-ns")
        
        mock_run.assert_called_once()
        # Should verify it's a list call for idempotency check
        self.assertIn("kubectl", mock_run.call_args[0][0])
        self.assertIn("get", mock_run.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
