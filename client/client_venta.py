import socket
import json
from common.soa_formatter import soa_formatter
import ast


def cerrar_cuenta():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        id = input("Ingrese id del pedido: ")
        data = {"action": "1", "id": id}
        
        #No tocar
        message = soa_formatter("finish_order_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Received raw data:", data)
        # Agregar manejo de errores
        
        return True
                    
    finally:
        print('Closing socket')
        sock.close()
        print(data.decode()[7:])

def watch_client():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        data = {"action": "2"}
        
        #No tocar
        message = soa_formatter("finish_order_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Received raw data:", data)
        # Agregar manejo de errores
        data1 = f"{json.loads(data.decode()[7:])}" 

        list_of_strings = ast.literal_eval(data1)
        print(list_of_strings)
        return True
                    
    finally:
        print('Closing socket')
        sock.close()
        for i in range(len(list_of_strings)):
            print(list_of_strings[i])

def main():
    while True:
        print("\nMain Menu:")
        print("1. Watch Ventas")
        print("2. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            watch_client()
        elif choice == "2":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
