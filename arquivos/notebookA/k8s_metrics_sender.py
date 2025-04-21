import socket
import time
import subprocess
import json

# IP do Notebook B (receptor)
HOST = '192.168.0.110'  # ⬅️ altere para o IP do notebook B
PORT = 9001

def get_total_pods():
    try:
        output = subprocess.check_output("kubectl get pods --no-headers", shell=True).decode()
        total = len(output.strip().split('\n')) if output.strip() else 0
        return total
    except Exception as e:
        print(f"[ERRO] get_total_pods: {e}")
        return 0

def get_pod_states():
    try:
        output = subprocess.check_output("kubectl get pods -o json", shell=True).decode()
        data = json.loads(output)
        states = {"Running": 0, "Failed": 0, "Pending": 0}
        for item in data["items"]:
            phase = item["status"]["phase"]
            if phase in states:
                states[phase] += 1
        return states
    except Exception as e:
        print(f"[ERRO] get_pod_states: {e}")
        return {"Running": 0, "Failed": 0, "Pending": 0}

def get_cpu_utilization():
    try:
        output = subprocess.check_output("kubectl top pods --no-headers", shell=True).decode()
        lines = output.strip().split("\n")
        total_cpu = 0
        for line in lines:
            parts = line.split()
            if len(parts) >= 2 and parts[1].endswith("m"):
                cpu_val = int(parts[1].replace("m", ""))
                total_cpu += cpu_val
        return total_cpu
    except Exception as e:
        print(f"[ERRO] get_cpu_utilization: {e}")
        return 0

def get_hpa_actions():
    try:
        output = subprocess.check_output("kubectl get hpa -o json", shell=True).decode()
        data = json.loads(output)
        if not data["items"]:
            return {"desiredReplicas": 0, "currentReplicas": 0}
        hpa = data["items"][0]
        return {
            "desiredReplicas": hpa["status"].get("desiredReplicas", 0),
            "currentReplicas": hpa["status"].get("currentReplicas", 0)
        }
    except Exception as e:
        print(f"[ERRO] get_hpa_actions: {e}")
        return {"desiredReplicas": 0, "currentReplicas": 0}

def main():
    print("[DEBUG] Iniciando k8s_metrics_sender.py...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # timeout de 5 segundos para tentar conexão

    try:
        print(f"[DEBUG] Tentando conectar a {HOST}:{PORT}...")
        sock.connect((HOST, PORT))
        print("[DEBUG] Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"[ERRO] Não foi possível conectar ao receptor: {e}")
        return

    while True:
        try:
            print("[DEBUG] Coletando métricas do cluster...")

            total_pods = get_total_pods()
            states = get_pod_states()
            cpu = get_cpu_utilization()
            hpa = get_hpa_actions()

            metrics = {
                "total_pods": total_pods,
                "running": states["Running"],
                "failed": states["Failed"],
                "pending": states["Pending"],
                "cpu_utilization": cpu,
                "hpa_desired_replicas": hpa["desiredReplicas"],
                "hpa_current_replicas": hpa["currentReplicas"]
            }

            print("[DEBUG] Métricas coletadas:", metrics)

            message = json.dumps(metrics)
            sock.sendall(message.encode('utf-8'))
            # print("[DEBUG] Métricas enviadas com sucesso!")

        except Exception as e:
            print(f"[ERRO] Falha ao enviar métricas: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
