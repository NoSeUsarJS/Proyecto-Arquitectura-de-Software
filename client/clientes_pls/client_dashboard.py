import socket
from common.soa_formatter import soa_formatter
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Función para mostrar la gráfica de ventas
def display_sales_chart(image_base64):
    image_data = base64.b64decode(image_base64)
    plt.figure(figsize=(10, 6))
    img = plt.imread(BytesIO(image_data))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 5001)  # Cambia esto al puerto del bus de servicios
print('Connecting to {} port {}'.format(*server_address))

# Connect to the server
sock.connect(server_address)

try:
    while True:
        user_input = input('Enviar solicitud para obtener datos del dashboard? y/n: ')
        if user_input != 'y':
            break
        
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
        
        print("Received raw data: {!r}".format(data))  # Declaración de depuración
        response = json.loads(data.decode())
        print('Received data: {}'.format(response))

        # Mostrar gráfica de ventas del día
        display_sales_chart(response['sales_chart'])

        # Mostrar porcentaje de productos vendidos
        print("\nPorcentaje de Productos Vendidos:")
        for product, percentage in response['product_percentage'].items():
            print(f"{product}: {percentage:.2f}%")

        # Mostrar inventario
        print("\nInventario de Productos:")
        for product, stock in response['inventory_data'].items():
            print(f"{product}: {stock} en stock")

finally:
    print('Closing socket')
    sock.close()
