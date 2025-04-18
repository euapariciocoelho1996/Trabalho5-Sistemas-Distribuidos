import socket
import json
import threading
from flask import Flask
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define as métricas Prometheus
total_pods = Gauge("k8s_total_pods", "Número total de pods")
cpu_utilization = Gauge("k8s_cpu_utilization", "Uso médio de CPU (%)")
pod_running = Gauge("k8s_pods_running", "Número de pods em execução")
pod_failed = Gauge("k8s_pods_failed", "Número de pods com falha")
pod_pending = Gauge("k8s_pods_pending", "Número de pods pendentes")
desired_replicas = Gauge("k8s_hpa_desired_replicas", "Réplicas desejadas pelo HPA")

# Função para escutar conexões socket
def start_socket_server():
    HOST = '0.0.0.0'
    PORT = 9001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor socket em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[INFO] Conexão recebida de {addr}")
                data = conn.recv(4096)
                if not data:
                    continue
                try:
                    metrics_data = json.loads(data.decode('utf-8'))

                    # Debug opcional:
                    # print("[DEBUG] JSON recebido:", metrics_data)

                    total_pods.set(metrics_data.get("total_pods", 0))
                    cpu_utilization.set(metrics_data.get("cpu_utilization", 0))
                    desired_replicas.set(metrics_data.get("hpa_replicas", 0))

                    status = metrics_data.get("status", {})
                    pod_running.set(status.get("Running", 0))
                    pod_failed.set(status.get("Failed", 0))
                    pod_pending.set(status.get("Pending", 0))

                except json.JSONDecodeError:
                    print("[ERRO] JSON inválido recebido.")

# Rota Prometheus para scrape
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Inicia o servidor socket em uma thread separada
    thread = threading.Thread(target=start_socket_server, daemon=True)
    thread.start()

    # Inicia o servidor Flask
    app.run(host="0.0.0.0", port=8000)
