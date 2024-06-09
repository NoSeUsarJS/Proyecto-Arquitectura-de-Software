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
        nombre = input("Ingrese el nombre del platillo: ")
        tiempo = input("Ingrese el tiempo medio de espera: ")
        precio = input("Ingrese el precio: ")
        descripcion =input("Ingrese la descripcion del platillo: ")
        data = {"action": "1", "nombre": nombre, "tiempo": tiempo, "precio": precio, "descripcion": descripcion}
        
        #No tocar
        message = soa_formatter("meal_manager", json.dumps(data))
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

def edit_client():

    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        nombre =input("ingrese el platillo a modificar: ")
        tiempo = input("Ingrese el tiempo medio nuevo: ")
        data = {"action": "2", "nombre": nombre, "tiempo": tiempo}
        
        #No tocar
        message = soa_formatter("meal_manager", json.dumps(data))
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

def delete_client():
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        nombre = input("Ingrese el nombre del platillo: ")
        data = {"action": "3", "nombre": nombre}
        
        #No tocar
        message = soa_formatter("meal_manager", json.dumps(data))
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
        data = {"action": "4"}
        
        #No tocar
        message = soa_formatter("meal_manager", json.dumps(data))
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
        print("1. Add meal")
        print("2. Edit meal")
        print("3. Delete meal")
        print("4. Watch meals")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_client()
        elif choice == "2":
            edit_client()
        elif choice == "3":
            delete_client()
        elif choice == "4":
            watch_client()
        elif choice == "5":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

#"meal_manager": "SV009"