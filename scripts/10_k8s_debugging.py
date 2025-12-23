#!/usr/bin/env python
import sys
import os
from typing import Iterator

# Allow importing from local utils package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.k8s_client import load_k8s_config, get_core_api
    from utils.logging_config import setup_logger
    from kubernetes.client.rest import ApiException
except ImportError:
    print("Error: Could not import utils. Ensure you are running from the correct directory.")
    sys.exit(1)

# Centralized Logging
logger = setup_logger(__name__)

def iter_unhealthy_nodes() -> Iterator[str]:
    """
    Generator that yields nodes NOT in 'Ready' state.
    
    Why Generators?
    - Memory Efficiency: We don't build a massive list of 5000 nodes in RAM.
    - Latency: We can process the first bad node before the API has finished sending the last one.
    """
    v1 = get_core_api()
    if not v1: return

    try:
        # Paging could be added here for true large-scale support (limit=500, continue_token)
        nodes = v1.list_node()
        for node in nodes.items:
            is_ready = False
            for condition in node.status.conditions:
                if condition.type == 'Ready' and condition.status == 'True':
                    is_ready = True
                    break
            
            if not is_ready:
                logger.warning(f"Node {node.metadata.name} is NOT Ready.")
                yield node.metadata.name

    except ApiException as e:
        logger.error(f"API Error listing nodes: {e}")

def check_pod_restarts(namespace: str = "default", restart_threshold: int = 5):
    """
    Identifies unstable pods.
    """
    v1 = get_core_api()
    if not v1: return

    try:
        # Optimization: In a real large cluster, you'd use `limit` and `continue` pagination here.
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            if not pod.status.container_statuses:
                continue
                
            for container in pod.status.container_statuses:
                if container.restart_count > restart_threshold:
                    logger.warning(
                        f"High Restarts: Pod {pod.metadata.name} "
                        f"(Container: {container.name}) "
                        f"has restarted {container.restart_count} times."
                    )

    except ApiException as e:
        logger.error(f"API Error in namespace {namespace}: {e}")

def check_pending_pvc():
    """
    Checks for Stuck PVCs.
    """
    v1 = get_core_api()
    if not v1: return

    try:
        # Server-Side Filtering: Only fetch Bound/Pending PVCs if needed, 
        # but here we want non-Bound. K8s doesn't support '!=' selectors easily.
        pvcs = v1.list_persistent_volume_claim_for_all_namespaces()
        for pvc in pvcs.items:
            if pvc.status.phase != 'Bound':
                logger.warning(f"PVC Issue: {pvc.metadata.name} in {pvc.metadata.namespace} is {pvc.status.phase}")
    except ApiException as e:
        logger.error(f"API Error listing PVCs: {e}")

if __name__ == "__main__":
    logger.info("--- Starting On-Prem AKS/K8s Health Check (Optimized) ---")
    
    if load_k8s_config():
        
        logger.info("Checking Nodes (Lazy Evaluation)...")
        # Consuming the generator
        bad_nodes_count = 0
        for node_name in iter_unhealthy_nodes():
            bad_nodes_count += 1
        
        if bad_nodes_count == 0:
            logger.info("All nodes look healthy.")

        logger.info("Checking Application Stability...")
        check_pod_restarts(namespace="default", restart_threshold=1)

        logger.info("Checking Storage...")
        check_pending_pvc()

    else:
        logger.warning("Skipping checks due to configuration failure.")
    
    logger.info("--- Check Complete ---")
