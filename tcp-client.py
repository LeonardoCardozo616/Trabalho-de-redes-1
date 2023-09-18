import socket
import hashlib

def receive_file_data():
    file_info = client_socket.recv(1024).decode('utf-8').split('\n')
    file_name = file_info[0]
    file_size = int(file_info[1])
    file_hash = file_info[2]
    file_status = file_info[3]
    print('file_name:', file_name)

    if file_status == "nok":
        print("Arquivo inexistente no servidor.")
        return
    
    received_data = client_socket.recv(1024)
    with open(file_name, 'wb') as file:
            file.write(received_data)

    print(f"Arquivo {file_name} recebido e verificado com sucesso.")
    print(received_data)
    return
    '''
    # Recebe os dados do arquivo
    received_data = b""
    while len(received_data) < file_size:
        data_chunk = client_socket.recv(1024)
        received_data += data_chunk
    
    # Verifica o Hash
    hasher = hashlib.sha256()
    hasher.update(received_data)
    received_hash = hasher.hexdigest()

    if received_hash == file_hash:
        # Grava o arquivo no cliente
        with open(file_name, 'wb') as file:
            file.write(received_data)
        
        print(f"Arquivo {file_name} recebido e verificado com sucesso.")
        return
    else:
        print(f'{file_hash} != {received_hash}')
        print(f"Erro na integridade do arquivo {file_name}. O hash não coincide.")
        return   
    '''

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
