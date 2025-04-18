from flask import Flask
from prometheus_client import Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import socket
import threading
import json

app = Flask(__name__)

# Definindo métricas
pod_total = Gauge('k8s_total_pods', 'Número total de pods')
pod_running = Gauge('k8s_pods_running', 'Pods em execução')
pod_pending = Gauge('k8s_pods_pending', 'Pods pendentes')
pod_failed = Gauge('k8s_pods_failed', 'Pods com falha')
cpu_util = Gauge('k8s_cpu_utilization', 'Utilização de CPU')
hpa_replicas = Gauge('k8s_hpa_desired_replicas', 'Réplicas desejadas pelo HPA')

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
                data = conn.recv(4096)
                if data:
                    metrics = json.loads(data.decode())
                    pod_total.set(metrics["total_pods"])
                    pod_running.set(metrics["status"].get("Running", 0))
                    pod_pending.set(metrics["status"].get("Pending", 0))
                    pod_failed.set(metrics["status"].get("Failed", 0))
                    cpu_util.set(metrics["hpa"].get("cpu_utilization", 0))
                    hpa_replicas.set(metrics["hpa"].get("desired_replicas", 0))

threading.Thread(target=start_socket_server, daemon=True).start()

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
