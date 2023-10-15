import socket

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request.decode('utf-8')}")
    client_socket.send(b"ACK")
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Listening on port 9999")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client)

if __name__ == "__main__":
    main()
