import socket

# Cria o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Endereço IP local e porta (altere IP conforme o computador servidor)
IP_SERVIDOR = '0.0.0.0'  # Aceita conexões de qualquer IP da rede
PORTA = 5000

# Liga o socket ao IP e porta
server_socket.bind((IP_SERVIDOR, PORTA))
server_socket.listen(1)

print(f"Servidor esperando conexão na porta {PORTA}...")

# Aceita conexão de um cliente
conn, addr = server_socket.accept()
print(f"Conectado por {addr}")

while True:
    dados = conn.recv(1024)
    if not dados:
        break
    print(f"Cliente: {dados.decode()}")
    conn.sendall(b"Mensagem recebida!")

conn.close()
