import sys
import logging
from typing import List, Dict, Optional

# Standard interview practice: Mention dependencies
# Requires: pip install kubernetes
try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
    KUBERNETES_AVAILABLE = True
except ImportError:
    KUBERNETES_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_cluster_config(kubeconfig_path: Optional[str] = None):
    """
    Loads authentication for the K8s cluster.
    Handles both local kubeconfig and in-cluster config (running inside a pod).
    """
    if not KUBERNETES_AVAILABLE:
        logger.error("The 'kubernetes' library is not installed. Run: pip install kubernetes")
        return False

    try:
        if kubeconfig_path:
            config.load_kube_config(config_file=kubeconfig_path)
            logger.info(f"Loaded kubeconfig from {kubeconfig_path}")
        else:
            # Tries to load in-cluster config first, then default local (~/.kube/config)
            try:
                config.load_incluster_config()
                logger.info("Loaded in-cluster configuration.")
            except config.ConfigException:
                config.load_kube_config()
                logger.info("Loaded default local kubeconfig.")
        return True
    except Exception as e:
        logger.error(f"Failed to load cluster config: {e}")
        return False

def get_unhealthy_nodes() -> List[str]:
    """
    Finds nodes that are NOT in the 'Ready' state.
    Critical for on-prem where hardware failures are common.
    """
    v1 = client.CoreV1Api()
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
    v1 = client.CoreV1Api()
    
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
    v1 = client.CoreV1Api()
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
    if load_cluster_config():
        
        # 2. Infrastructure Layer Check (Nodes)
        print("\n[Checking Nodes...]")
        bad_nodes = get_unhealthy_nodes()
        if not bad_nodes:
            print("All nodes look healthy.")

        # 3. Application Layer Check (Pods in 'default' namespace)
        print("\n[Checking Application Stability...]")
        check_pod_restarts(namespace="default", restart_threshold=3)

        # 4. Storage Layer Check
        print("\n[Checking Storage...]")
        check_pending_pvc()

    else:
        print("Skipping checks due to configuration failure.")
    
    print("\n--- Check Complete ---")
