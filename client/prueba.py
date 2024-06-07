import socket
from common.soa_formatter import soa_formatter
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 5000)
print('Connecting to {} port {}'.format(*server_address))

# Connect to the server
sock.connect(server_address)

try:
    while True:
        user_input = input('Send Hello world to servi? y/n: ')
        if user_input != 'y':
            break
        
        data = {"food": "pollo con papas fritas", "price": 7000}
        message = soa_formatter("create_order_manager", json.dumps(data)).encode()
        print('Sending {!r}'.format(message))
        sock.sendall(message)

        print('Waiting for transaction')
        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Checking servi answer ...")
        print('Received {!r}'.format(data))

finally:
    print('Closing socket')
    sock.close()
