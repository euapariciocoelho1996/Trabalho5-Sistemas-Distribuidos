import socket

# IP do servidor (altere para o IP local do computador onde o servidor está rodando)
IP_SERVIDOR = '192.168.0.103'  # <-- coloque o IP real do servidor aqui
PORTA = 5000

# Cria o socket
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((IP_SERVIDOR, PORTA))

mensagem = input("Digite a mensagem para o servidor: ")
cliente_socket.sendall(mensagem.encode())

# Espera resposta
resposta = cliente_socket.recv(1024)
print("Servidor respondeu:", resposta.decode())

cliente_socket.close()
