import pandas as pd
from datetime import datetime
import os
import psycopg2

import json
import socket
from common.services import Service
from common.services import soa_formatter

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
        # Agregar manejo de errores
        try:
            return data.decode()[7:]  
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
                    
    finally:
        print('Closing socket')
        sock.close()

# Función para manejar la solicitud del inventario
def handle_inventory_request(data: str) -> str:
    data = json.loads(data)
    action = data.get('action')
    
    if action == "1":
        print("Generando Excel de comidas...")
        query = f"SELECT * FROM platillo;"
        response = Enviar(query)
        matriz = json.loads(response)
        
        df = pd.DataFrame(matriz, columns=["ID", "Nombre", "Tiempo", "Precio", "Descripción"])
        df.to_excel("comidas.xlsx", index=False)
        
        response = "Excel de comidas generado"

    elif action == "2":
        print("Generando Excel...")
        query = f"SELECT * FROM ingredientes;"
        response = Enviar(query)
        matriz = json.loads(response)
        
        df = pd.DataFrame(matriz, columns=["ID", "Nombre", "Cantidad"])
        df.to_excel("ingredientes.xlsx", index=False)
        
        response = "Excel de ingredientes generado"

    elif action == "3":
        print("Generando Excel...")
        query = f"SELECT * FROM persona;"
        response = Enviar(query)
        matriz = json.loads(response)
        
        df = pd.DataFrame(matriz, columns=["ID Persona", "Nombre", "RUT", "Rol", "Password"])
        df.to_excel("personas.xlsx", index=False)
        
        response = "Excel de personas generado"

    elif action == "4":
        print("Generando Excel...")
        query = f"SELECT * FROM venta;"
        response = Enviar(query)
        matriz = json.loads(response)
        
        df = pd.DataFrame(matriz, columns=["ID Venta", "ID Pedido", "Precio Total"])
        df.to_excel("ventas.xlsx", index=False)
        
        response = "Excel de ventas generado"
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 

# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="generate_excel", host="localhost", port=5001)
inventory_service.run_service(handle_inventory_request)
