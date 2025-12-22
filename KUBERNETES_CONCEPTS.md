# Kubernetes Networking & Access Patterns for Interviews

## 1. The "Permanent Port Forwarding" Myth
In Kubernetes, `kubectl port-forward` is **strictly for debugging**. It is not designed to be a permanent solution for accessing applications. It creates a secure tunnel from your local machine directly to a Pod or Service within the cluster.

If you are asked "How do I set up permanent port forwarding?", the correct engineering answer is: **"We don't. We use Services and Ingress to expose applications."**

## 2. Best Practices for Accessing Apps

### A. Local Development (Minikube)
1.  **`minikube service` (Easiest)**
    *   Opens the service in your default browser and creates a temporary tunnel.
    *   Command: `minikube service <service-name> -n <namespace>`
2.  **`minikube tunnel` (Simulates Cloud LoadBalancer)**
    *   Runs as a daemon on your host. It assigns an "External IP" to services of type `LoadBalancer`.
    *   Command: `sudo minikube tunnel` (keep running in a separate terminal).
3.  **Ingress Addon (Production-like)**
    *   Enable: `minikube addons enable ingress`
    *   Allows you to use hostnames (e.g., `booking.local`) mapped to Minikube's IP.

### B. On-Premises / Production (Real Cluster)
1.  **Ingress (The Standard)**
    *   **What is it?** An HTTP/HTTPS router (like Nginx, Traefik, HAProxy) that sits at the edge of the cluster.
    *   **Why use it?** Single IP address for multiple services, SSL termination, path-based routing.
    *   **Setup:** Deploy an Ingress Controller. Point your DNS/Load Balancer to the Ingress Controller nodes.
2.  **Service Type: LoadBalancer (with MetalLB)**
    *   On AWS/GCP, this automatically gives you a Cloud IP.
    *   **On-Prem:** Cloud providers aren't available. You must install **MetalLB** (or similar). It talks to your routers via BGP or ARP to assign "real" LAN IPs to your services.
3.  **Service Type: NodePort**
    *   **What is it?** Opens a specific port (range 30000-32767) on **every** node in the cluster.
    *   **Pros:** Simple, always works.
    *   **Cons:** Ugly ports (e.g., `http://node-ip:31542`), security risk if not firewalled.

### Summary Table: What to Use?

| Scenario | Recommended Approach | Why? |
| :--- | :--- | :--- |
| **Quick Debugging** | `kubectl port-forward` | Secure, instant, no config changes needed. |
| **Local Dev (Minikube)** | `minikube service` or `tunnel` | Mimics real access without complexity. |
| **On-Prem Production** | **Ingress Controller** | Efficient resource usage, proper HTTP routing, SSL management. |
| **On-Prem TCP/UDP** | **MetalLB (LoadBalancer)** | For non-HTTP traffic (DBs, custom protocols). |

## 3. "Hacking" Port Forwarding (If you absolutely must)
If you just want `port-forward` to run in the background without locking your terminal (not recommended for production):

```bash
# Run in background with nohup (Linux/macOS)
nohup kubectl port-forward svc/guestbook-ui -n guestbook 8181:80 > /dev/null 2>&1 &

# Explanation:
# nohup    -> "No Hang Up". Keeps running if you close the terminal.
# &        -> Runs the command in the background immediately.
# > /dev/null -> Discards output (logs).
```

To stop it later:
```bash
# Find the process ID (PID)
ps aux | grep port-forward
# Kill it
kill <PID>
```
