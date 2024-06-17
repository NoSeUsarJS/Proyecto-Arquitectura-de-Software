import socket
from common.soa_formatter import soa_formatter
import json

def request_data(table):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 5001)  # Cambia esto al puerto del bus de servicios
    print('Connecting to {} port {}'.format(*server_address))

    # Connect to the server
    sock.connect(server_address)

    try:
        data = {"request": "get_dashboard_data", "table": table}
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
        
        print("Received raw data: {!r}".format(data))  # Declaración de depuración
        data_str = data.decode()

        # Procesar el prefijo y extraer el JSON
        if data_str.startswith("SV003OK"):
            data_str = data_str[7:]

        if not data_str:
            print("Empty response received.")
            return

        try:
            response = json.loads(data_str)
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            return

        print('Received data: {}'.format(response))

        # Mostrar datos de la tabla seleccionada
        if table == 'platillo' and 'platillo_data' in response:
            print("\nDatos de Platillo:")
            for item in response['platillo_data']:
                print(item)

        elif table == 'ingredientes' and 'inventory_data' in response:
            print("\nInventario de Productos:")
            for item in response['inventory_data']:
                print(item)

        elif table == 'persona' and 'persona_data' in response:
            print("\nDatos de Persona:")
            for item in response['persona_data']:
                print(item)

        elif table == 'venta' and 'venta_data' in response:
            print("\nDatos de Venta:")
            for item in response['venta_data']:
                print(item)

        if 'error' in response:
            print(f"Error: {response['error']}")

    finally:
        print('Closing socket')
        sock.close()

def main():
    while True:
        print("\nMain Menu:")
        print("1. Obtener datos de Platillo")
        print("2. Obtener datos de Inventario")
        print("3. Obtener datos de Persona")
        print("4. Obtener datos de Venta")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            request_data('platillo')
        elif choice == "2":
            request_data('ingredientes')
        elif choice == "3":
            request_data('persona')
        elif choice == "4":
            request_data('venta')
        elif choice == "5":
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
