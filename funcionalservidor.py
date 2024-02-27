import socket
import threading

def handle_client(client, addr, clients):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"[{addr[0]}:{addr[1]}] {message}")
                broadcast(message, clients, client)
                if message.startswith("MOVE"):
                    # Envia a jogada para todos os clientes
                    for c in clients:
                        c.send(message.encode('utf-8'))
            else:
                remove_client(client, clients)
                break
        except:
            remove_client(client, clients)
            break

def broadcast(message, clients, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client, clients)

def remove_client(client, clients):
    if client in clients:
        clients.remove(client)
        client.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(5)
    print("Server is listening on port 5555...")
    
    clients = []

    while True:
        client, addr = server_socket.accept()
        clients.append(client)
        print(f"Connection established with {addr[0]}:{addr[1]}")
        
        if len(clients) == 2:
            for c in clients:
                c.send("start_game".encode('utf-8'))

        client_thread = threading.Thread(target=handle_client, args=(client, addr, clients))
        client_thread.start()

start_server()
