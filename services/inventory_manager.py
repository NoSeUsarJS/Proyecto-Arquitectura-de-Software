import json
import psycopg2
import pandas as pd
from common.services import Service

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword"
}

# Función para conectar a la base de datos
def get_db_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para agregar ingrediente
def add_ingredient(data):
    conn = get_db_connection()
    if conn is None:
        return "Error al conectar a la base de datos"
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
    if conn is None:
        return "Error al conectar a la base de datos"
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
    if conn is None:
        return "Error al conectar a la base de datos"
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
    if conn is None:
        return "Error al conectar a la base de datos"
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

    print("Sending response:", response)  # Añadido para depuración
    return str(json.dumps(response))

# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="inventory_manager", host="localhost", port=5001)
inventory_service.run_service(handle_inventory_request)
