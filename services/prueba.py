import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 5000)
print('Connecting to {} port {}'.format(*server_address))

# Connect to the server
sock.connect(server_address)

try:
    # Send initial message to the server
    message = b'00010sinitservi'
    print('Sending {!r}'.format(message))
    sock.sendall(message)
    sinit = 1 

    while True:
        print("Waiting for a transaction")
        
        # Receive the expected amount of data length (first 5 bytes)
        amount_expected = int(sock.recv(5))
        amount_received = 0
        data = b''

        # Receive the actual data
        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Processing...")
        print('Received {!r}'.format(data))
        
        if sinit == 1:
            sinit = 0
            print('Received sinit answer')
        else:
            print("Sending answer")
            message = b'00013servireceived'
            print('Sending {!r}'.format(message))
            sock.sendall(message)

finally:
    print('Closing socket')
    sock.close()
