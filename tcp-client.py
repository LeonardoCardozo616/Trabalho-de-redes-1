import socket
import hashlib

def receive_file_data():
    # Recebendo os dados
    file_info = client_socket.recv(1024).decode('utf-8').split('\n')
    file_name = file_info[0]
    file_size = int(file_info[1])
    file_hash = file_info[2]
    file_status = file_info[3]

    # Arquivo não foi encontrado
    if file_status == "nok":
        print("Arquivo inexistente no servidor.")
        return
    
    # Escreve o arquivo no diretório local
    with open('Novo_Arquivo.txt', 'wb') as file:
        received_data = 0
        while received_data < file_size:
            data = client_socket.recv(1024)
            received_data += len(data)
            file.write(data)

    # Verifica o hash do arquivo
    hash_sha256 = hashlib.sha256()
    with open (file_name, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            hash_sha256.update(data)
    received_hash = hash_sha256.hexdigest()

    if received_hash == file_hash:
        print(f'Arquivo {file_name} recebido e verificado com sucesso.')
        print(f'Nome: {file_name}\nTamanho: {file_size}\nHash: {file_hash}\nStatus: {file_status}')
    else:
        print(f'Erro na integridade do arquivo: {file_hash} != {received_hash}')

# Criando Socket Cliente
HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Opções disponíveis:")
print("1. Sair")
print("2. Requisitar um arquivo")
print("3. Modo Chat")

while True:
    choice = input("Escolha uma opção (1/2/3): ")
    
    # Dependendo da escolha vai ativar uma das requests
    if choice == "1":
        client_socket.send("Sair".encode('utf-8'))
        break
    elif choice == "2":
        file_request = input("Digite o nome do arquivo desejado: ")
        client_socket.send(f"Arquivo {file_request}".encode('utf-8'))
        receive_file_data()
    elif choice == "3":
        client_socket.send("Chat".encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))
        while True:
            message = input("Digite sua mensagem (ou 'sair' para encerrar o chat): ")
            if message.lower() == "sair":
                client_socket.send(message.encode('utf-8'))
                break
            client_socket.send(message.encode('utf-8'))
        print(client_socket.recv(1024).decode('utf-8'))

print(client_socket.recv(1024).decode('utf-8'))
client_socket.close()
