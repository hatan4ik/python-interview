#!/usr/bin/env python
import sys
import os
import time
from pprint import pformat

# Add src to path so we can import devops_toolkit without installing it
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(SRC_PATH)

try:
    from devops_toolkit.k8s.client import load_k8s_config, get_custom_objects_api
    from devops_toolkit.utils.logging import setup_logger
    from kubernetes.client.rest import ApiException
except ImportError as e:
    print(f"Error: Could not import devops_toolkit. {e}")
    sys.exit(1)

# Centralized Logging
logger = setup_logger("FluxManager")

# Flux CRD Constants
GROUP = "source.toolkit.fluxcd.io"
VERSION = "v1"
PLURAL_GIT = "gitrepositories"

GROUP_KUST = "kustomize.toolkit.fluxcd.io"
PLURAL_KUST = "kustomizations"

def list_git_repositories(namespace: str = ""):
    """
    Lists all GitRepository objects in the cluster.
    Equivalent to: flux get sources git
    """
    api = get_custom_objects_api()
    if not api: return
    
    try:
        if namespace:
            # Namespaced list
            response = api.list_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace=namespace, plural=PLURAL_GIT
            )
        else:
            # Cluster-wide list
            response = api.list_cluster_custom_object(
                group=GROUP, version=VERSION, plural=PLURAL_GIT
            )
            
        logger.info(f"--- Found {len(response.get('items', []))} GitRepositories ---")
        for item in response.get("items", []):
            metadata = item.get("metadata", {})
            spec = item.get("spec", {})
            status = item.get("status", {})
            
            name = metadata.get("name")
            ns = metadata.get("namespace")
            url = spec.get("url")
            ready = "Unknown"
            
            # Parse Status Conditions
            for cond in status.get("conditions", []):
                if cond.get("type") == "Ready":
                    ready = cond.get("status")
            
            print(f"[{ns}] {name} -> {url} (Ready: {ready})")
            
    except ApiException as e:
        logger.error(f"Failed to list GitRepositories: {e}")

def reconcile_kustomization(name: str, namespace: str):
    """
    Forces a Flux Kustomization to sync immediately.
    
    How it works:
    Flux watches for changes to the 'reconcile.fluxcd.io/requestedAt' annotation.
    Updating this timestamp triggers the controller to run immediately.
    """
    api = get_custom_objects_api()
    if not api: return
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # JSON Merge Patch payload
    patch_body = {
        "metadata": {
            "annotations": {
                "reconcile.fluxcd.io/requestedAt": timestamp
            }
        }
    }
    
    logger.info(f"🔄 Triggering reconcile for Kustomization '{name}' in '{namespace}'...")
    
    try:
        api.patch_namespaced_custom_object(
            group=GROUP_KUST,
            version="v1",
            namespace=namespace,
            plural=PLURAL_KUST,
            name=name,
            body=patch_body
        )
        logger.info("✅ Reconcile triggered successfully.")
        
    except ApiException as e:
        logger.error(f"Failed to patch Kustomization: {e}")

def suspend_kustomization(name: str, namespace: str, suspend: bool = True):
    """
    Suspends or Resumes a Kustomization.
    Useful for "Emergency Stop" buttons in custom dashboards.
    """
    api = get_custom_objects_api()
    if not api: return
    
    action = "Suspending" if suspend else "Resuming"
    logger.info(f"⏯  {action} Kustomization '{name}'...")
    
    patch_body = {
        "spec": {
            "suspend": suspend
        }
    }
    
    try:
        api.patch_namespaced_custom_object(
            group=GROUP_KUST,
            version="v1",
            namespace=namespace,
            plural=PLURAL_KUST,
            name=name,
            body=patch_body
        )
        logger.info(f"✅ Successfully {action.lower()} '{name}'.")
        
    except ApiException as e:
        logger.error(f"Failed to update suspend state: {e}")

if __name__ == "__main__":
    if not load_k8s_config():
        logger.error("Could not load Kubeconfig.")
        exit(1)

    print("\n--- 1. Listing Sources ---")
    try:
        list_git_repositories()
    except Exception as e:
        logger.error(f"Error connecting to Kubernetes: {e}")
        print("\n\033[91mCheck if your cluster (Minikube) is running!\033[0m")
    
    # Example Usage (Commented out to prevent accidental writes on run)
    # print("\n--- 2. Triggering Sync ---")
    # reconcile_kustomization("podinfo", "flux-system")
    
    # print("\n--- 3. Emergency Suspend ---")
    # suspend_kustomization("podinfo", "flux-system", suspend=True)
