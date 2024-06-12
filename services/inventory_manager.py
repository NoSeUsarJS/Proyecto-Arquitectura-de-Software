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
        nombre = data.get('nombre')
        cantidad = data.get('cantidad')
        print("Agregando ingredientes...")
        query = f"INSERT INTO ingredientes ( nombre, cantidad_ingredientes) VALUES ({nombre},{cantidad})"
        Enviar(query)
        response = "Ingrediente añadido"

    elif action == "2":
        nombre = data.get('nombre')
        cantidad = data.get('cantidad')
        print("Actualizando Mesa...")
        query = f"UPDATE ingredientes SET cantidad_ingredientes = {cantidad} WHERE nombre = {nombre}"
        Enviar(query)
        response = "Ingredientes actualizados"

    elif action == "3":
        nombre = data.get('nombre')
        query = f"DELETE FROM ingredientes WHERE nombre = {nombre} "
        Enviar(query)
        response = "Mesa eliminada"

    elif action == "4":
        query = f"SELECT * FROM ingredientes"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        lista = []
        for i in range(len(matriz)):
            id = matriz[i][0]
            nombre = matriz[i][1]
            cantidad = matriz[i][2]
            lista.append(f" Id: {id} - Nombre: {nombre} - Cantidad: {cantidad}")
        response = json.dumps(lista)
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 
# "db_manager": "SV005",
# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="inventory_manager", host="localhost", port=5001)
inventory_service.run_service(handle_inventory_request)