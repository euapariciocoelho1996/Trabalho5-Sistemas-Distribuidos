# SISTEMAS DISTRIBUÍDOS - TOLERÂNCIA A FALHAS, AUTO-RECUPERAÇÃO, ESCALONAMENTO HORIZONTAL E MONITORAMENTO REMOTO

Este projeto implementa um sistema distribuído entre dois notebooks interligados, com foco em monitoramento remoto de um cluster Kubernetes. Utilizamos Prometheus, Grafana, Flask, Sockets e Docker para coleta, envio e visualização de métricas do cluster, incluindo dados em tempo real do HPA e do estado dos pods.
```
📁 TRABALHO5-SISTEMAS-DISTRIBUIDOS
│
├── 📁 notebookA                     
│   ├── 📁 app                      # Aplicativo Flask
│   │   ├── main.py                
│   │   └── requirements.txt       
│   │
│   ├── 📁 k8s                      # Arquivos de configuração do cluster Kubernetes
│   │   ├── components.yaml
│   │   ├── deployment.yaml
│   │   ├── hpa.yaml
│   │   └── service.yaml
│   │
│   ├── Dockerfile                 # Dockerfile do Notebook A
│   ├── k8s_metrics_sender.py      # Script que coleta e envia métricas via socket
│   └── requirements.txt
│
├── 📁 notebookB                     # Recebe métricas e expõe via Prometheus e Grafana
│   ├── 📁 prometheus                
│   │   └── prometheus.yml
│   │
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── metrics_receiver.py
│   └── requirements.txt
│
└── README.md
```
## ✅ Requisitos

🚙 Docker e Docker Compose

🥝 Python 3.13.2

📦 Flask 3.1.0

📱 Minikube / Kubernetes (v1.35.0)

📊 Prometheus (latest)

📈 Grafana (latest)

## 🚀 Como Executar o Projeto

### 1️⃣ Notebook A 
```
Iniciar Docker
Iniciar minikube (minikube start) pelo PowerShell Adm.
Verificar se o minikube foi iniciado corretamente com: minikube status (deve aparecer running)
cd arquivos
cd notebookA
kubectl apply -f k8s/
cd app
pip install -r requirements.txt
Verificar pods ativos com: kubectl get pods (deve iniciar com 2)
Executar k8s_metrics_sender.py

CASO QUEIRA VER USO DA CPU: kubectl get hpa -w
```

### 2️⃣ Notebook B 

```
Iniciar Docker
cd arquivos
cd notebookB
pip install -r requirements.txt
docker-compose up -d
Executar metrics_receiver.py

```
### O Prometheus estará disponível na porta 9090, e o Grafana na 3000, para ver o funcionamento:

```
Prometheus: http://localhost:9090
Grafana: http://localhost:3000

Ajustes no Grafana:

Usuário: admin
Senha: admin

Adicionar Gráficos. No Grafana:

- Open menu
- Connections
- Data sources
- Add New Data Source
- Seleciona Prometheus
- Default desativado
- Coloca http://localhost:9090 no prometheus server url
- Salva
- Dashboards
- New
- New Dashboards
- Add visualização
- Prometheus criado

```
### APLICANDO SOBRECARGA ARTIFICIAL EM UM POD 

```
kubectl get pods (ver pods ativos)

kubectl get hpa -w (uso da cpu)

kubectl exec -it <nome do pod> -- /bin/sh
Acessa o terminal interativo (sh) dentro do pod especificado.

apt-get update && apt-get install -y stress
Atualiza a lista de pacotes e instala a ferramenta stress, usada para simular carga de CPU.

stress --cpu 1 --timeout 60
Gera uma carga de CPU utilizando 1 núcleo por 60 segundos, útil para testar o escalonamento automático (HPA).

```
### ⚙️ Funcionamento Interno

```
O Notebook A coleta métricas do cluster Kubernetes com kubectl e envia para o Notebook B usando socket.

O Notebook B recebe as métricas e as expõe na rota /metrics, que o Prometheus consome.

O Grafana acessa o Prometheus para visualizar as métricas com dashboards.

As métricas monitoradas incluem:

Uso de CPU por pod

Estado dos pods (Running, Pending, Failed)

Ações disparadas pelo HPA

Número total de pods ativos
```



📆 Contribuidores

Luis Eduardo

Francisco Aparício

Victor Macêdo
