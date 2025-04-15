# Usa uma imagem base leve com Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements.txt primeiro para otimizar cache
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Agora copia o restante do código
COPY . .

# Expõe a porta que o app Flask usará
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "main.py"]
