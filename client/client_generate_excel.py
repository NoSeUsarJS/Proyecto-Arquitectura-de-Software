import socket
import json
from common.soa_formatter import soa_formatter
import ast


def add_client():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        while True:
            print("Menu")
            print("1. Excel Comidas")
            print("2. Excel Inventario")
            print("3. Excel Personal")
            print("4. Excel Ventas")
            numero = input("Ingrese numero de la accion: ")
            if numero == "1" or numero == "2" or numero == "3" or numero == "4":
                data = {"action": numero}
                break
            else:
                print("Ingresar numero valido")
        #No tocar
        message = soa_formatter("generate_excel", json.dumps(data))
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

def main():
    while True:
        print("\nMain Menu:")
        print("1. Generar excel")
        print("2. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_client()
        elif choice == "2":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
