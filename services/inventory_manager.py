import pandas as pd
import psycopg2
from common.services import Service
import json

# Configuración del servicio
SERVICE_NAME = "inventory_manager"
host, port = "soabus", 5001 
service = Service(SERVICE_NAME, host, port)

# Configuración de PostgreSQL
db_config = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'postgres_db'
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

# Función para agregar ingrediente
def add_ingredient(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO inventory (product, stock) VALUES (%s, %s)
    """
    cursor.execute(query, (data['product'], data['stock']))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ingrediente agregado."

# Función para eliminar ingrediente
def delete_ingredient(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    DELETE FROM inventory WHERE product = %s
    """
    cursor.execute(query, (data['product'],))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ingrediente eliminado."

# Función para editar ingrediente
def edit_ingredient(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    UPDATE inventory SET stock = %s WHERE product = %s
    """
    cursor.execute(query, (data['stock'], data['product']))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ingrediente editado."

# Función para ver ingredientes
def view_ingredients():
    conn = get_db_connection()
    query = """
    SELECT product, stock FROM inventory;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

# Función para manejar la solicitud del inventario
def handle_inventory_request(data: str) -> str:
    data = json.loads(data)
    action = data.get('action')
    
    if action == "add":
        response = add_ingredient(data)
    elif action == "delete":
        response = delete_ingredient(data)
    elif action == "edit":
        response = edit_ingredient(data)
    elif action == "view":
        response = view_ingredients()
    else:
        response = "Acción no válida."

    return str(json.dumps(response))

service.run_service(handle_inventory_request)
