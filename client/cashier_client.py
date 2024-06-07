import socket
import json
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from common.soa_formatter import soa_formatter

def display_sales_chart(image_base64):
    if image_base64:
        image_data = base64.b64decode(image_base64)
        plt.figure(figsize=(10, 6))
        img = plt.imread(BytesIO(image_data))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    else:
        print("No sales data available for today.")

def dashboard_client():
    # Define the server address and port for dashboard
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
        user_input = input('Enviar solicitud para obtener datos del dashboard? y/n: ')
        if user_input == 'y':
            data = {"request": "get_dashboard_data"}
            message = soa_formatter("dashboard", json.dumps(data))
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
            
            print("Received raw data: {!r}".format(data))
            data_str = data.decode()
            if data_str.startswith("SV003OK"):
                data_str = data_str[7:]

            response = json.loads(data_str)
            print('Received data: {}'.format(response))

            if 'sales_chart' in response:
                display_sales_chart(response['sales_chart'])

            if 'product_percentage' in response:
                print("\nPorcentaje de Productos Vendidos:")
                for product, percentage in response['product_percentage'].items():
                    print(f"{product}: {percentage:.2f}%")

            if 'inventory_data' in response:
                print("\nInventario de Productos:")
                for product, stock in response['inventory_data'].items():
                    print(f"{product}: {stock} en stock")

            if 'error' in response:
                print(f"Error: {response['error']}")
    finally:
        print('Closing socket')
        sock.close()

def inventory_client():
    # Define the server address and port for inventory
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
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

            message = soa_formatter("inventory_manager", json.dumps(data))
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
            try:
                response_str = data.decode()
                response = json.loads(response_str)
            except json.JSONDecodeError:
                print("Error decoding JSON response.")
                continue

            if choice == "4":
                import pandas as pd
                df = pd.DataFrame(response)
                print(df)
            else:
                print(response)
    finally:
        print('Closing socket')
        sock.close()

def generate_excel_client():
    # Define the server address and port for generate_excel
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    try:
        user_input = input('Enviar solicitud para generar reporte? y/n: ')
        if user_input == 'y':
            data = {"request": "generate_report"}
            message = soa_formatter("generate_excel", json.dumps(data))
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
            
            print("Checking service answer ...")
            response_str = data.decode()
            print('Received {!r}'.format(response_str))
            
            if response_str.startswith("SV004OK"):
                response_str = response_str[7:]

            response = json.loads(response_str)
            print('Received response:', response)
    finally:
        print('Closing socket')
        sock.close()

def main():
    while True:
        print("\nMain Menu:")
        print("1. Dashboard")
        print("2. Inventory Manager")
        print("3. Generate Excel Report")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            dashboard_client()
        elif choice == "2":
            inventory_client()
        elif choice == "3":
            generate_excel_client()
        elif choice == "4":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
