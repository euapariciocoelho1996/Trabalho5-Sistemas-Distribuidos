from flask import Flask, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sistemas Distribuídos - 2025.1</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            font-family: 'Montserrat', sans-serif;
            color: #fff;
            text-align: center;
            padding-top: 50px;
        }

        .container {
            max-width: 700px;
            margin: 0 auto;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        }

        h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 15px;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        }

        h2 {
            font-size: 22px;
            font-weight: 500;
            margin-bottom: 25px;
            color: #d1e8ff;
        }

        p, ul {
            font-size: 18px;
            color: #e0e0e0;
        }

        ul {
            list-style: none;
            padding: 0;
            margin-top: 20px;
        }

        ul li {
            margin-bottom: 8px;
        }

        .highlight {
            color: #00ffd5;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ Sistemas Distribuídos</h1>
        <h2>Período 2025.1 • Tolerância a Falhas e Monitoramento com Kubernetes</h2>
        <p>Aplicação Flask com métricas Prometheus integrada e funcionando perfeitamente.</p>
        
        <h2>👨‍💻 Equipe:</h2>
        <ul>
            <li class="highlight">Francisco Aparício Nascimento Coelho</li>
            <li class="highlight">Luis Eduardo Silva Brito</li>
            <li class="highlight">Victor Macedo Carvalho</li>
        </ul>

        <h2>🎓 Professor:</h2>
        <p class="highlight">FRANCISCO AIRTON PEREIRA DA SILVA</p>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
