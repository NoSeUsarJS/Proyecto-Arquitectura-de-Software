import socket
import json
from common.soa_formatter import soa_formatter
import ast

# capaz se elimina ? 
def add_client(plato):
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        while True:
            try:
                cantidad_ingredientes = int(input("Cantidad de ingredientes que tiene esta comida: "))
                break  # Salir del bucle si la entrada es un número válido
            except ValueError:
                print("Por favor, ingresa un número válido.")
        client_inventory.watch_client()
        lista_id = []
        consumido = []
        for i in range(cantidad_ingredientes):
            lista_id.append(input("Ingrese el id del ingrediente: "))
            consumido.append(input("cantidad que se usa del ingrediente: "))
        data = {"action": "5", "ingredientes": lista_id, "consumido": consumido, "nombre": plato}
        
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

def edit_client(plato):

    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        ingrediente = input("Ingrese el ingrediente a modificar: ")
        cantidad = input("Ingrese nueva cantidad que se utiliza en el platillo")

        data = {"action": "6", "nombre": plato, "ingrediente": ingrediente, "cantidad": cantidad}
        

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

def delete_client(plato):
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        data = {"action": "7", "nombre": plato}
        
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

def watch_client(plato):
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        data = {"action": "8", "nombre": plato}
        
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