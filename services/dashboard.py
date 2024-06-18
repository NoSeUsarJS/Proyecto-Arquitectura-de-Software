import pandas as pd
import psycopg2
import json
import socket
from common.services import Service, soa_formatter

def Enviar(query):
    server_address = ('localhost', 5001)
    print('Connecting to {} port {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    
    data = {"query": query}
    try:
        message = soa_formatter("db_manager", json.dumps(data))
        sock.sendall(message)

        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''

        while amount_received < amount_expected:
            packet = sock.recv(amount_expected - amount_received)
            amount_received += len(packet)
            data += packet
        
        print("Received raw data:", data)
        try:
            decoded_data = data.decode()[7:]
            print("Decoded data:", decoded_data)
            return json.loads(decoded_data)
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
            return None
                    
    finally:
        print('Closing socket')
        sock.close()

# Función para manejar la solicitud de datos del dashboard
def handle_dashboard_request(data: str) -> str:
    data = json.loads(data)
    action = data.get('action')

    if action == "1":
        query = f"SELECT precio_total,fecha_insercion from venta"
        response = Enviar(query)
        response = json.dumps(response)
    
    
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 

# Inicializar y ejecutar el servicio
dashboard_service = Service(service_name="dashboard", host="localhost", port=5001)
dashboard_service.run_service(handle_dashboard_request)
