import socket
import json
import time
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
autoscaling = client.AutoscalingV1Api()

HOST = '192.168.0.102'  # IP do Notebook B
PORT = 9001

def get_metrics():
    pods = v1.list_namespaced_pod(namespace="default")
    pod_statuses = [pod.status.phase for pod in pods.items]
    total_pods = len(pods.items)
    status_count = {
        "Running": pod_statuses.count("Running"),
        "Pending": pod_statuses.count("Pending"),
        "Failed": pod_statuses.count("Failed"),
    }

    hpa = autoscaling.read_namespaced_horizontal_pod_autoscaler("app-hpa", "default")
    hpa_status = {
        "current_replicas": hpa.status.current_replicas,
        "desired_replicas": hpa.status.desired_replicas,
        "cpu_utilization": hpa.status.current_cpu_utilization_percentage or 0
    }

    return {
        "total_pods": total_pods,
        "status": status_count,
        "hpa": hpa_status
    }

while True:
    try:
        metrics = get_metrics()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(metrics).encode('utf-8'))
        time.sleep(10)
    except Exception as e:
        print(f"[ERRO] {e}")
