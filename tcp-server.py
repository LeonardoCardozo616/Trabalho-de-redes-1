import socket
import threading
import os
import hashlib

def handle_client(client_socket, porta):
    while True:    
        # Recebe uma chamada
        request = client_socket.recv(1024).decode('utf-8').strip()
        
        if request == 'Sair':
            # Fecha a conexão
            print(f'{addr[0]}:{porta} - Fechando Conexão')
            client_socket.send('Fechando conexão. '.encode('utf-8'))
            client_socket.close()
            break
        
        elif request.startswith('Arquivo'):
            # Ainda em desenvolvimento
            file_name = request.split(' ')[1] #Nome

            if os.path.exists(file_name):
                print(f'Arquivo {file_name} encontrado!')
                with open(file_name, 'rb') as file:
                    file_data = file.read() #Arquivo

                hasher = hashlib.sha256()
                hasher.update(file_data)
                file_hash = hasher.hexdigest() #Hash

                file_size = len(file_data) #Tamanho
                file_status = 'ok' #Status

                data = f'{file_name}\n{file_size}\n{file_hash}\n{file_status}\n'.encode('utf-8')
                client_socket.send(data)
                client_socket.send(f'{file_data}'.encode('utf-8'))
            else:
                print(f'Arquivo {file_name} NAO encontrado!')
                client_socket.send(f'{file_name}\n0\n0\nnok'.encode('utf-8'))
                

        elif request == 'Chat':
            client_socket.send("Modo Chat ativado.".encode('utf-8'))
            while True:
                # Escreve as mensagens, a mensagem for "sair", o chat é encerrado
                message = client_socket.recv(1024).decode('utf-8')
                if message.lower() == "sair":
                    print(f"{porta} Saiu do Chat!")
                    break
                print(f"Mensagem ({porta}): {message}")
            
            client_socket.send("Modo Chat desativado.".encode('utf-8'))


HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor TCP esperando conexões em {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Cliente de {addr[0]}:{addr[1]} conectado!")

    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr[1],))
    client_thread.start()
