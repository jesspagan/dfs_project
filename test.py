import socket
import sys

HOST, PORT = "", 8000
p = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(p)

finally:
    sock.close()