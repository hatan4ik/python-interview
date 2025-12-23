import logging
from typing import Optional

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
    KUBERNETES_AVAILABLE = True
except ImportError:
    KUBERNETES_AVAILABLE = False

logger = logging.getLogger(__name__)

def load_k8s_config(kubeconfig_path: Optional[str] = None) -> bool:
    """
    Loads authentication for the K8s cluster.
    Handles both local kubeconfig and in-cluster config (running inside a pod).
    
    Returns:
        bool: True if connection successful, False otherwise.
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

def get_core_api() -> Optional['client.CoreV1Api']:
    """Returns an authenticated CoreV1Api client or None."""
    if load_k8s_config():
        return client.CoreV1Api()
    return None

def get_custom_objects_api() -> Optional['client.CustomObjectsApi']:
    """Returns an authenticated CustomObjectsApi client or None."""
    if load_k8s_config():
        return client.CustomObjectsApi()
    return None
