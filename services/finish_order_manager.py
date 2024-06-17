import json
import socket
from common.services import Service
from common.services import soa_formatter
from datetime import datetime

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
def handle_finish_order(data: str) -> str:
    data = json.loads(data)
    action = data.get('action')
    
    if action == "1":
        id_pedido = data.get('id')
        precio_total = f"(SELECT SUM(platillo.Precio) AS total_precio FROM platillo INNER JOIN Relacion_Platillo_Pedido ON platillo.id_platillo = Relacion_Platillo_Pedido.id_platillo WHERE Relacion_Platillo_Pedido.id_pedido = {id_pedido})"
        print("Registrando venta...")
        query = f"INSERT INTO Venta (id_pedido, Precio_total) VALUES ({id_pedido}, {precio_total})"
        ver1 = True if Enviar(query) == "null" else False

        if not ver1:
            response = "Error al registrar venta"
            print(response)
            return response
        
        query = f"DELETE FROM Relacion_Platillo_Pedido WHERE id_pedido = {id_pedido}"
        ver1 = True if Enviar(query) == "null" else False

        if not ver1:
            response = "Error al registrar venta"
            print(response)
            return response
        
        query = f"DELETE FROM pedido WHERE id_Pedido = {id_pedido}"
        ver1 = True if Enviar(query) == "null" else False

        if not ver1:
            response = "Error al registrar venta"
            print(response)
            return response

        response = "Venta registrada"

    elif action == "2":
        query = f"SELECT * FROM Venta"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        print(matriz)
        lista = []
        for i in range(len(matriz)):
            id_venta = matriz[i][0]
            id_pedido = matriz[i][1]
            precio_total = matriz[i][2]
            lista.append(f" Id: {id_venta} - Id pedido: {id_pedido} - Precio total: {precio_total}")
        response = json.dumps({
            "ventas": lista
        })
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 
# "db_manager": "SV005",
# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="finish_order_manager", host="localhost", port=5001)
inventory_service.run_service(handle_finish_order)