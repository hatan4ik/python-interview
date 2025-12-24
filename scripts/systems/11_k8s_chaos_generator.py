#!/usr/bin/env python
import sys
import os
import random
import time

# Add src to path so we can import devops_toolkit without installing it
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(SRC_PATH)

try:
    from devops_toolkit.k8s.client import load_k8s_config, get_core_api
    from devops_toolkit.utils.logging import setup_logger
    from kubernetes.client.rest import ApiException
except ImportError as e:
    print(f"Error: Could not import devops_toolkit. {e}")
    sys.exit(1)

# Centralized Logging
logger = setup_logger("ChaosMonkey")

def inject_crashloop(namespace="default"):
    """Creates a Pod that exits immediately, causing a CrashLoopBackOff."""
    name = "chaos-crashloop"
    manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name, "labels": {"app": "chaos"}},
        "spec": {
            "restartPolicy": "Always",
            "containers": [{
                "name": "crasher",
                "image": "busybox",
                "command": ["/bin/sh", "-c", "echo 'Critical Failure!'; sleep 2; exit 1"]
            }]
        }
    }
    _apply_manifest(namespace, manifest, "CrashLoopBackOff Pod")

def inject_oom_killed(namespace="default"):
    """Creates a Pod with low memory limits that tries to allocate too much RAM."""
    name = "chaos-oom"
    manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name, "labels": {"app": "chaos"}},
        "spec": {
            "restartPolicy": "Always",
            "containers": [{
                "name": "memory-hog",
                "image": "python:3.9-alpine",
                "resources": {"limits": {"memory": "50Mi"}},  # Strict limit
                # Python one-liner to eat 100MB RAM
                "command": ["python", "-c", "x = ' ' * (1024 * 1024 * 100); import time; time.sleep(3600)"]
            }]
        }
    }
    _apply_manifest(namespace, manifest, "OOMKilled Pod (Memory Pressure)")

def inject_image_pull_error(namespace="default"):
    """Creates a Pod trying to pull a non-existent image."""
    name = "chaos-bad-image"
    manifest = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name, "labels": {"app": "chaos"}},
        "spec": {
            "containers": [{
                "name": "ghost",
                "image": "verisign/secret-repo:does-not-exist",  # 404 Not Found
                "command": ["sleep", "3600"]
            }]
        }
    }
    _apply_manifest(namespace, manifest, "ImagePullBackOff Pod")

def inject_stuck_pvc(namespace="default"):
    """Creates a PVC requesting a non-existent StorageClass."""
    name = "chaos-stuck-pvc"
    manifest = {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {"name": name, "labels": {"app": "chaos"}},
        "spec": {
            "storageClassName": "aws-efs-broken-class", # Doesn't exist
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": "5Gi"}}
        }
    }
    try:
        v1 = get_core_api()
        if not v1: return
        v1.create_namespaced_persistent_volume_claim(namespace, manifest)
        logger.info(f"✅ Created Stuck PVC: {name} (Will remain Pending)")
    except ApiException as e:
        if e.status == 409:
            logger.info(f"⚠️  Stuck PVC '{name}' already exists. Skipping.")
        else:
            logger.warning(f"Failed to create PVC: {e.reason}")

def inject_broken_service(namespace="default"):
    """Creates a Service that points to NO pods (Endpoint failure)."""
    name = "chaos-broken-svc"
    manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name, "labels": {"app": "chaos"}},
        "spec": {
            "selector": {"app": "this-label-does-not-exist"}, # Points to nothing
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": 8080}]
        }
    }
    try:
        v1 = get_core_api()
        if not v1: return
        v1.create_namespaced_service(namespace, manifest)
        logger.info(f"✅ Created Broken Service: {name} (Has no Endpoints)")
    except ApiException as e:
        if e.status == 409:
            logger.info(f"⚠️  Broken Service '{name}' already exists. Skipping.")
        else:
            logger.warning(f"Failed to create Service: {e.reason}")

def _apply_manifest(namespace, manifest, description):
    v1 = get_core_api()
    if not v1: return
    try:
        v1.create_namespaced_pod(namespace, manifest)
        logger.info(f"✅ Created {description}: {manifest['metadata']['name']}")
    except ApiException as e:
        if e.status == 409:
            logger.info(f"⚠️  {description} already exists. Skipping.")
        else:
            logger.error(f"❌ Failed to create {description}: {e.reason}")

def cleanup_chaos(namespace="default"):
    """Deletes all resources labeled 'app=chaos'."""
    logger.info("🧹 Cleaning up Chaos resources...")
    v1 = get_core_api()
    if not v1: return
    
    # Delete Pods
    pods = v1.list_namespaced_pod(namespace, label_selector="app=chaos")
    for pod in pods.items:
        v1.delete_namespaced_pod(pod.metadata.name, namespace)
        logger.info(f"   Deleted Pod: {pod.metadata.name}")

    # Delete PVCs
    pvcs = v1.list_namespaced_persistent_volume_claim(namespace, label_selector="app=chaos")
    for pvc in pvcs.items:
        v1.delete_namespaced_persistent_volume_claim(pvc.metadata.name, namespace)
        logger.info(f"   Deleted PVC: {pvc.metadata.name}")
        
    # Delete Services
    svcs = v1.list_namespaced_service(namespace, label_selector="app=chaos")
    for svc in svcs.items:
        v1.delete_namespaced_service(svc.metadata.name, namespace)
        logger.info(f"   Deleted Service: {svc.metadata.name}")

def main() -> int:
    parser = argparse.ArgumentParser(description="K8s Chaos Generator for Interview Prep")
    parser.add_argument("--mode", choices=["all", "crash", "oom", "pvc", "image", "service", "clean"], default="all", help="Type of chaos to inject")
    args = parser.parse_args()

    if not load_k8s_config():
        return 1

    if args.mode == "clean":
        cleanup_chaos()
    else:
        print("🔥 Injecting Chaos into Cluster... (Ctrl+C to stop, run --mode clean to fix)")
        if args.mode in ["all", "crash"]:
            inject_crashloop()
        if args.mode in ["all", "oom"]:
            inject_oom_killed()
        if args.mode in ["all", "image"]:
            inject_image_pull_error()
        if args.mode in ["all", "pvc"]:
            inject_stuck_pvc()
        if args.mode in ["all", "service"]:
            inject_broken_service()
        
        print("\n⚠️  Chaos Injected! Run 'kubectl get all' or use your debug script to find the issues.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
