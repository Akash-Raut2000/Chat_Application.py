import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = []

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                remove_client(client_socket)
            else:
                broadcast(message, client_socket)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            remove_client(client_socket)
            break

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                remove_client(client)
                print(f"An error occurred: {str(e)}")

def main():
    print("Chat server is listening on port", PORT)
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()