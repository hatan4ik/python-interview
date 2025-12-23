import logging
import subprocess
import time
from typing import Optional
from devops_toolkit.system import run_command, check_binary_exists

logger = logging.getLogger(__name__)

def check_minikube_running() -> bool:
    """Checks if Minikube is currently running."""
    if not check_binary_exists("minikube"):
        return False
    try:
        run_command("minikube status", check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_minikube(memory: int = 4096, cpus: int = 2, driver: str = "docker"):
    """Starts Minikube if it's not already running."""
    if check_minikube_running():
        logger.info("✅ Minikube is already running.")
        return

    logger.info("🚀 Minikube is NOT running. Starting it now...")
    cmd = f"minikube start --memory={memory} --cpus={cpus} --driver={driver}"
    run_command(cmd, shell=True)
    logger.info("✅ Minikube started successfully.")

def ensure_namespace(namespace: str):
    """Idempotently creates a Kubernetes namespace."""
    logger.info(f"Ensuring namespace '{namespace}' exists...")
    # Check if exists first to avoid noisy 'already exists' errors if we were just to create
    try:
        run_command(f"kubectl get namespace {namespace}", check=True, capture_output=True)
        logger.debug(f"Namespace '{namespace}' already exists.")
    except subprocess.CalledProcessError:
        logger.info(f"Creating namespace '{namespace}'...")
        run_command(f"kubectl create namespace {namespace}", shell=True)

def wait_for_deployment(deployment_name: str, namespace: str, timeout: int = 300):
    """Waits for a deployment to be available."""
    logger.info(f"⏳ Waiting for deployment/{deployment_name} in '{namespace}'...")
    run_command(
        f"kubectl wait --for=condition=available deployment/{deployment_name} -n {namespace} --timeout={timeout}s",
        shell=True
    )
