import json
from common.services import Service
from db_class import DatabaseServer

def handle_db_request(data: str) -> str:
    data = json.loads(data)
    action = data.get('query')
    print("Consultando en la base de datos. . .")
    response = server.query(action)
    print(response)
    data = {"respuesta": response}
    
    print("Sending response:", json.dumps(data))  # Añadido para depuración
    return json.dumps(response) #str(json.dumps(response))

# Se inicia la base de datos
server = DatabaseServer(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
server.create_connection()
server.create_tables()
# Comunicacion del servicio
db_service = Service(service_name="db_manager", host="localhost", port=5001)
db_service.run_service(handle_db_request)