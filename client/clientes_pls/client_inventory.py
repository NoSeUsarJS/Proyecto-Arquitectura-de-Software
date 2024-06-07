import socket
from common.soa_formatter import soa_formatter
import json

# Función para enviar solicitud al servicio
def send_request(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5001)  # Cambia esto al puerto del bus de servicios
    sock.connect(server_address)
    
    try:
        message = soa_formatter("inventory_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        response = json.loads(data.decode())
        return response
    finally:
        sock.close()

# Función para mostrar menú y realizar acciones
def menu():
    while True:
        print("\nMenu:")
        print("1. Agregar ingrediente")
        print("2. Eliminar ingrediente")
        print("3. Editar ingrediente")
        print("4. Ver ingredientes")
        print("5. Salir")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            product = input("Nombre del ingrediente: ")
            stock = int(input("Cantidad en stock: "))
            data = {"action": "add", "product": product, "stock": stock}
        elif choice == "2":
            product = input("Nombre del ingrediente a eliminar: ")
            data = {"action": "delete", "product": product}
        elif choice == "3":
            product = input("Nombre del ingrediente a editar: ")
            stock = int(input("Nueva cantidad en stock: "))
            data = {"action": "edit", "product": product, "stock": stock}
        elif choice == "4":
            data = {"action": "view"}
        elif choice == "5":
            break
        else:
            print("Opción no válida.")
            continue

        response = send_request(data)
        if choice == "4":
            print("\nInventario:")
            for item in response:
                print(f"Producto: {item['product']}, Stock: {item['stock']}")
        else:
            print(response)

if __name__ == "__main__":
    menu()
import socket
from common.soa_formatter import soa_formatter
import json

# Función para enviar solicitud al servicio
def send_request(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5001)  # Cambia esto al puerto del bus de servicios
    sock.connect(server_address)
    
    try:
        message = soa_formatter("inventory_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        response = json.loads(data.decode())
        return response
    finally:
        sock.close()

# Función para mostrar menú y realizar acciones
def menu():
    while True:
        print("\nMenu:")
        print("1. Agregar ingrediente")
        print("2. Eliminar ingrediente")
        print("3. Editar ingrediente")
        print("4. Ver ingredientes")
        print("5. Salir")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            product = input("Nombre del ingrediente: ")
            stock = int(input("Cantidad en stock: "))
            data = {"action": "add", "product": product, "stock": stock}
        elif choice == "2":
            product = input("Nombre del ingrediente a eliminar: ")
            data = {"action": "delete", "product": product}
        elif choice == "3":
            product = input("Nombre del ingrediente a editar: ")
            stock = int(input("Nueva cantidad en stock: "))
            data = {"action": "edit", "product": product, "stock": stock}
        elif choice == "4":
            data = {"action": "view"}
        elif choice == "5":
            break
        else:
            print("Opción no válida.")
            continue

        response = send_request(data)
        if choice == "4":
            print("\nInventario:")
            for item in response:
                print(f"Producto: {item['product']}, Stock: {item['stock']}")
        else:
            print(response)

if __name__ == "__main__":
    menu()
