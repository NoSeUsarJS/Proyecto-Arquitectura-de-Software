from common.services import Service
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
            return data.decode()[7:]  # Aquí asumes que hay un prefijo de 7 caracteres que no es parte del JSON
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
            return None
                    
    finally:
        print('Closing socket')
        sock.close()

# Funciones para obtener datos desde PostgreSQL
def get_platillo_data():
    try:
        conn = Enviar("SELECT * FROM platillo")
        df = pd.read_sql_query("SELECT * FROM platillo", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting platillo data: {e}")
        return pd.DataFrame()

def get_inventory_data():
    try:
        conn = Enviar("SELECT * FROM ingredientes")
        df = pd.read_sql_query("SELECT * FROM ingredientes", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting inventory data: {e}")
        return pd.DataFrame()

def get_persona_data():
    try:
        conn = Enviar("SELECT * FROM persona")
        df = pd.read_sql_query("SELECT * FROM persona", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting persona data: {e}")
        return pd.DataFrame()

def get_venta_data():
    try:
        conn = Enviar("SELECT * FROM venta")
        df = pd.read_sql_query("SELECT * FROM venta", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting venta data: {e}")
        return pd.DataFrame()

# Función para manejar la solicitud de datos del dashboard
def handle_dashboard_request(data: str) -> str:
    data = json.loads(data)
    response = {}
    table = data.get("table")
    
    try:
        if table == 'platillo':
            platillo_data = get_platillo_data().to_dict()
            response['platillo_data'] = platillo_data
        elif table == 'ingredientes':
            inventory_data = get_inventory_data().to_dict()
            response['inventory_data'] = inventory_data
        elif table == 'persona':
            persona_data = get_persona_data().to_dict()
            response['persona_data'] = persona_data
        elif table == 'venta':
            venta_data = get_venta_data().to_dict()
            response['venta_data'] = venta_data
        else:
            response['error'] = "Invalid table selected."
    except Exception as e:
        response['error'] = f"An error occurred: {e}"

    return json.dumps(response)

# Inicializar y ejecutar el servicio
dashboard_service = Service(service_name="dashboard", host="localhost", port=5001)
dashboard_service.run_service(handle_dashboard_request)
