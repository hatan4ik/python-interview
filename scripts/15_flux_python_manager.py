#!/usr/bin/env python
"""
Flux CD Python Manager (The "Engineering" Way)

In an interview, you might be asked: "How do you automate Flux without shelling out to the CLI?"

Answer: "Flux resources are just Kubernetes Custom Resource Definitions (CRDs). 
We can use the standard Kubernetes Python client to Create, Read, Update, and Delete them."

This script demonstrates:
1. Listing all Flux GitRepositories.
2. Triggering a Reconciliation (Force Sync) via Annotation patching.
3. Suspending a Kustomization programmatically.
"""

import sys
import logging
import datetime
from typing import Dict, Any

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
except ImportError:
    print("Error: 'kubernetes' library missing. Install via: pip install kubernetes")
    exit(1)

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FluxManager")

# Flux CRD Constants
GROUP = "source.toolkit.fluxcd.io"
VERSION = "v1"
PLURAL_GIT = "gitrepositories"

GROUP_KUST = "kustomize.toolkit.fluxcd.io"
PLURAL_KUST = "kustomizations"

def load_k8s_config():
    """Authenticates with the cluster."""
    try:
        config.load_kube_config() # Local ~/.kube/config
        return True
    except Exception:
        try:
            config.load_incluster_config() # Inside a Pod
            return True
        except Exception:
            return False

def list_git_repositories(namespace: str = ""):
    """
    Lists all GitRepository objects in the cluster.
    Equivalent to: flux get sources git
    """
    api = client.CustomObjectsApi()
    
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
    api = client.CustomObjectsApi()
    
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
    api = client.CustomObjectsApi()
    
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
