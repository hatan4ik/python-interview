#!/usr/bin/env python
import sys
import os
import logging
from typing import List

# Allow importing from local utils package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.k8s_client import load_k8s_config, get_core_api
    from kubernetes.client.rest import ApiException
except ImportError:
    print("Error: Could not import utils. Ensure you are running from the correct directory.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_unhealthy_nodes() -> List[str]:
    """
    Finds nodes that are NOT in the 'Ready' state.
    Critical for on-prem where hardware failures are common.
    """
    v1 = get_core_api()
    if not v1: return []

    unhealthy_nodes = []
    
    try:
        nodes = v1.list_node()
        for node in nodes.items:
            # Parse node conditions to find 'Ready' status
            is_ready = False
            for condition in node.status.conditions:
                if condition.type == 'Ready' and condition.status == 'True':
                    is_ready = True
                    break
            
            if not is_ready:
                unhealthy_nodes.append(node.metadata.name)
                logger.warning(f"Node {node.metadata.name} is NOT Ready.")
                
                # Interview Tip: Check for Memory/Disk Pressure
                for condition in node.status.conditions:
                    if condition.status == 'True' and condition.type != 'Ready':
                        logger.warning(f"  -> Issue: {condition.type} ({condition.message})")

    except ApiException as e:
        logger.error(f"API Error listing nodes: {e}")
        
    return unhealthy_nodes

def check_pod_restarts(namespace: str = "default", restart_threshold: int = 5):
    """
    Identifies unstable pods that are restarting frequently.
    Common symptom of application crashes or OOM (Out of Memory) kills.
    """
    v1 = get_core_api()
    if not v1: return

    try:
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    if container.restart_count > restart_threshold:
                        logger.warning(
                            f"High Restarts: Pod {pod.metadata.name} "
                            f"(Container: {container.name}) "
                            f"has restarted {container.restart_count} times."
                        )
                        # Check specific error states
                        if container.state.waiting:
                            logger.info(f"  -> State: Waiting ({container.state.waiting.reason})")
                        if container.state.terminated:
                            logger.info(f"  -> Last State: Terminated ({container.state.terminated.reason})")

    except ApiException as e:
        logger.error(f"API Error in namespace {namespace}: {e}")

def check_pending_pvc():
    """
    Checks for PersistentVolumeClaims that are stuck in Pending.
    Very common in on-prem storage (Ceph/NFS/Local) issues.
    """
    v1 = get_core_api()
    if not v1: return

    try:
        pvcs = v1.list_persistent_volume_claim_for_all_namespaces()
        for pvc in pvcs.items:
            if pvc.status.phase != 'Bound':
                logger.warning(f"PVC Issue: {pvc.metadata.name} in {pvc.metadata.namespace} is {pvc.status.phase}")
    except ApiException as e:
        logger.error(f"API Error listing PVCs: {e}")

if __name__ == "__main__":
    print("--- Starting On-Prem AKS/K8s Health Check ---")
    
    # 1. Setup Connection
    if load_k8s_config():
        
        # 2. Infrastructure Layer Check (Nodes)
        print("\n[Checking Nodes...]")
        bad_nodes = get_unhealthy_nodes()
        if not bad_nodes:
            print("All nodes look healthy.")

        # 3. Application Layer Check (Pods in 'default' namespace)
        print("\n[Checking Application Stability...]")
        check_pod_restarts(namespace="default", restart_threshold=1)

        # 4. Storage Layer Check
        print("\n[Checking Storage...]")
        check_pending_pvc()

    else:
        print("Skipping checks due to configuration failure.")
    
    print("\n--- Check Complete ---")
