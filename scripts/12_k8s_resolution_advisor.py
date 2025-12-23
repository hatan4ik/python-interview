#!/usr/bin/env python
import sys
import os

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
logger = setup_logger("Advisor")


def print_solution(title: str, description: str, commands: List[str]):
    """Pretty prints a resolution block."""
    print(f"\n🚨 \033[1mISSUE DETECTED: {title}\033[0m")
    print(f"   {description}")
    print(f"   \033[94m🛠  SUGGESTED FIX ACTIONS:\033[0m")
    for cmd in commands:
        print(f"     $ {cmd}")
    print("-" * 60)

def analyze_pods(namespace="default"):
    """Analyzes pods for common failure states and suggests fixes."""
    v1 = get_core_api()
    if not v1: return

    try:
        pods = v1.list_namespaced_pod(namespace)
        for pod in pods.items:
            name = pod.metadata.name
            
            # 1. Check for Container Statuses
            if not pod.status.container_statuses:
                continue
                
            for container in pod.status.container_statuses:
                state = container.state
                
                # CASE A: OOMKilled (Out of Memory)
                if state.terminated and state.terminated.reason == "OOMKilled":
                    print_solution(
                        f"Pod '{name}' was OOMKilled",
                        f"The container '{container.name}' consumed more memory than its limit allowed.",
                        [
                            f"kubectl describe pod {name} -n {namespace}  # Check 'Last State'",
                            f"kubectl edit pod {name} -n {namespace}      # Increase 'resources.limits.memory'",
                            f"# Check current usage (requires metrics-server):",
                            f"kubectl top pod {name} -n {namespace}"
                        ]
                    )

                # CASE B: CrashLoopBackOff (App crashing)
                elif state.waiting and state.waiting.reason == "CrashLoopBackOff":
                    print_solution(
                        f"Pod '{name}' is in CrashLoopBackOff",
                        f"The application in container '{container.name}' is starting but crashing immediately.",
                        [
                            f"kubectl logs {name} -c {container.name} -n {namespace} --previous  # View crash logs",
                            f"kubectl get events -n {namespace} --field-selector involvedObject.name={name} --sort-by='.lastTimestamp'",
                            f"# Debug interactively if logs are empty:",
                            f"kubectl run debug-{name} -it --rm --image={container.image} -- /bin/sh"
                        ]
                    )

                # CASE C: ImagePullBackOff (Registry/Image issues)
                elif state.waiting and state.waiting.reason in ["ImagePullBackOff", "ErrImagePull"]:
                    print_solution(
                        f"Pod '{name}' cannot pull image",
                        f"Failed to pull image '{container.image}'. Could be a typo, auth issue, or network.",
                        [
                            f"kubectl describe pod {name} -n {namespace}  # Look at 'Events' at the bottom",
                            f"# Verify the image exists manually:",
                            f"docker pull {container.image}",
                            f"# Check if an ImagePullSecret is needed:",
                            f"kubectl get secrets -n {namespace}"
                        ]
                    )

    except ApiException as e:
        logger.error(f"Error scanning pods: {e}")

def analyze_pvcs(namespace="default"):
    """Checks for Stuck PVCs."""
    v1 = get_core_api()
    if not v1: return

    try:
        pvcs = v1.list_namespaced_persistent_volume_claim(namespace)
        for pvc in pvcs.items:
            if pvc.status.phase == "Pending":
                sc = pvc.spec.storage_class_name
                print_solution(
                    f"PVC '{pvc.metadata.name}' is Stuck (Pending)",
                    f"It is requesting StorageClass '{sc}', but the volume is not being provisioned.",
                    [
                        f"kubectl describe pvc {pvc.metadata.name} -n {namespace}  # Check 'Events' for provider errors",
                        f"kubectl get sc  # Verify if StorageClass '{sc}' actually exists",
                        f"kubectl get pv  # Check if a matching PV exists (if manual binding)",
                    ]
                )
    except ApiException as e:
        logger.error(f"Error scanning PVCs: {e}")

def analyze_services(namespace="default"):
    """Checks for Services that don't point to any Pods."""
    v1 = get_core_api()
    if not v1: return

    try:
        services = v1.list_namespaced_service(namespace)
        pods = v1.list_namespaced_pod(namespace)
        
        for svc in services.items:
            if svc.spec.selector:
                # Match service selector labels to pods
                selector = svc.spec.selector
                matching_pods = 0
                for pod in pods.items:
                    if pod.metadata.labels and all(item in pod.metadata.labels.items() for item in selector.items()):
                        matching_pods += 1
                
                if matching_pods == 0:
                    formatted_selector = ",".join([f"{k}={v}" for k, v in selector.items()])
                    print_solution(
                        f"Service '{svc.metadata.name}' has NO Endpoints",
                        f"The Service is selecting for labels '{formatted_selector}', but NO running pods match this.",
                        [
                            f"kubectl get pods -n {namespace} --show-labels  # Compare your pod labels",
                            f"kubectl describe service {svc.metadata.name} -n {namespace}  # Verify 'Endpoints' is 'none'",
                            f"kubectl edit service {svc.metadata.name} -n {namespace}  # Fix the selector"
                        ]
                    )

    except ApiException as e:
        logger.error(f"Error scanning Services: {e}")

def main() -> int:
    if not load_k8s_config():
        print("❌ Failed to load kubeconfig.")
        return 1

    print("🤖 \033[1mK8s Resolution Advisor: Scanning Cluster...\033[0m")
    print("-" * 60)
    
    analyze_pods()
    analyze_pvcs()
    analyze_services()
    
    print("\n✅ Scan Complete.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
