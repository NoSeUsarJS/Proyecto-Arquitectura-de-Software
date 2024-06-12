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
    if action == "0":
        rut = data.get('rut')
        password = data.get('password')
        print("Buscando persona...")
        query = f"SELECT rol FROM persona WHERE rut = '{rut}' AND password = '{password}'"
        Ver = Enviar(query)
        #print(len(Ver))
        transformar = json.loads(Ver)
        transformar = json.dumps(transformar[0][0])
        response = transformar[0][0]
    elif action == "1":
        nombre = data.get('nombre')
        rut = data.get('rut')
        rol = data.get('rol')
        password = data.get('password')
        print("Agregando persona...")
        query = f"INSERT INTO persona (nombre, rut, rol, password) VALUES ('{nombre}','{rut}',{rol},'{password}')"
        Enviar(query)
        response = "Persona añadida"

    elif action == "2":
        rut = data.get('rut')
        rol = data.get('rol')
        print("Actualizando persona...")
        query = f"UPDATE persona SET rol = {rol} WHERE rut = '{rut}'"
        Enviar(query)
        response = "Persona actualizada"

    elif action == "3":
        rut = data.get('rut')
        query = f"DELETE FROM persona WHERE rut = '{rut}' "
        Enviar(query)
        response = "Persona eliminada"

    elif action == "4":
        query = f"SELECT * FROM persona"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        lista = []
        for i in range(len(matriz)):
            id = matriz[i][0]
            nombre = matriz[i][1]
            rut = matriz[i][2]
            rol = matriz [i][3]
            password = matriz[i][4]

            lista.append(f" id: {id} - nombre: {nombre} - rut: {rut} - rol: {rol} - password: {password}")
        response = json.dumps(lista)
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 
# "db_manager": "SV005",
# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="account_manager", host="localhost", port=5001)
inventory_service.run_service(handle_inventory_request)
