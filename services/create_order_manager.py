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
def handle_order_action(data: str) -> str:
    data = json.loads(data)
    action = data.get('action')
    
    if action == "1":
        mesa = data.get('mesa')
        rut = data.get('rut')
        platillos = list(data.get('platillos'))
        hora = datetime.now().time()
        print("Agregando pedido...")
        query = f"INSERT INTO pedido (mesa, hora, id_persona) VALUES ({mesa},'{hora}', (SELECT id FROM persona WHERE rut = '{rut}'))"
        ver1 = True if Enviar(query) == "null" else False

        if not ver1:
            response = "Error al añadir pedido"
            print(response)
            return response
        
        for platillo in platillos:
            id_platillo , comentario = platillo.get('platillo'), platillo.get('comentario')
            query = f"Insert INTO Relacion_Platillo_Pedido (id_platillo, id_pedido, Comentario) VALUES ({id_platillo}, (SELECT id_Pedido FROM pedido WHERE hora = '{hora}' AND mesa = {mesa}), '{comentario}')"
            ver1 = True if Enviar(query) == "null" else False
            if not ver1:
                response = f"Error al añadir platillo {id_platillo}"
                print(response)
                return response

        response = "Pedido añadido"

    elif action == "2":
        query = f"SELECT * FROM pedido"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        print(matriz)
        lista = []
        for i in range(len(matriz)):
            id = matriz[i][0]
            mesa = matriz[i][1]
            hora = matriz[i][2]
            id_persona = matriz[i][3]
            lista.append(f" Id: {id} - Mesa: {mesa} - Hora: {hora} - ID persona: {id_persona}")
        response = json.dumps({
            "pedidos": lista
        })
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 
# "db_manager": "SV005",
# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="create_order_manager", host="localhost", port=5001)
inventory_service.run_service(handle_order_action)