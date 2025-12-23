#!/usr/bin/env python
"""
Global Environment Bootstrapper.

This script acts as the "One-Click Setup" for the entire interview environment.
It orchestrates:
1. Minikube Infrastructure (CPU/RAM checks).
2. GitOps Tooling (ArgoCD).
3. GitOps Tooling (FluxCD).

Engineering Principle: "Idempotency". You can run this script 10 times, 
and it will only do the work that is missing.
"""

import subprocess
import sys
import os
import shutil
import time
import logging

# Allow importing from local utils package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.logging_config import setup_logger
except ImportError:
    print("Error: Could not import utils. Ensure you are running from the correct directory.")
    sys.exit(1)

# Configure Logging
logger = setup_logger("Bootstrap")

def check_command(cmd: str):
    """Verifies that a required binary is installed."""
    if not shutil.which(cmd):
        logger.error(f"❌ Critical Error: '{cmd}' is not installed.")
        logger.info(f"Please install '{cmd}' and try again.")
        sys.exit(1)

def run_cmd(cmd: str, check=True):
    """Runs a shell command."""
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        logger.error(f"Failed to execute: {cmd}")
        if check:
            sys.exit(1)

def check_minikube_status():
    """Checks if Minikube is running, starts it if not."""
    logger.info("🔍 Checking Minikube status...")
    
    try:
        # Check if running
        subprocess.run("minikube status", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("✅ Minikube is already running.")
    except subprocess.CalledProcessError:
        logger.info("🚀 Minikube is NOT running. Starting it now...")
        # Start with enough resources for both Argo and Flux
        run_cmd("minikube start --memory=4096 --cpus=2 --driver=docker")
        logger.info("✅ Minikube started successfully.")

def run_setup_script(script_name: str):
    """Executes another Python setup script in the same directory."""
    logger.info(f"👉 triggering {script_name}...")
    try:
        # Assumes the script is in the same directory
        script_path = f"scripts/{script_name}"
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError:
        logger.error(f"❌ {script_name} failed.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n--- 🛠  INTERVIEW ENVIRONMENT BOOTSTRAPPER 🛠  ---\n")

    # 1. Prerequisite Checks
    check_command("minikube")
    check_command("kubectl")
    check_command("python3")

    # 2. Infrastructure Layer
    check_minikube_status()

    # 3. Application Layer (GitOps)
    print("\n[ Installing ArgoCD ]")
    run_setup_script("13_gitops_setup.py")

    print("\n[ Installing FluxCD ]")
    run_setup_script("14_fluxcd_setup.py")

    print("\n" + "="*60)
    print("✅✅✅  COMPLETE ENVIRONMENT READY  ✅✅✅")
    print("="*60)
    print("1. Cluster:       Running (Minikube)")
    print("2. ArgoCD:        Installed (Namespace: argocd)")
    print("3. FluxCD:        Installed (Namespace: flux-system)")
    print("\nRun 'python3 scripts/10_k8s_debugging.py' to verify health.")
    print("="*60 + "\n")
