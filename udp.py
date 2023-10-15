import socket
import time

# Sender
def udp_send():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2)  # Timeout for waiting for ACK
        data = b"Hello"
        s.sendto(data, ('localhost', 12345))
        try:
            ack, addr = s.recvfrom(1024)
            if ack == b"ACK":
                print("Received ACK")
        except socket.timeout:
            print("Didn't receive ACK, resending...")
            s.sendto(data, ('localhost', 12345))

# Receiver
def udp_receive():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', 12345))
        data, addr = s.recvfrom(1024)
        print(f"Received {data} from {addr}")
        s.sendto(b"ACK", addr)

# These functions would typically run on different machines or processes
