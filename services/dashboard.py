import pandas as pd
import psycopg2
from common.services import Service
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configuración del servicio
SERVICE_NAME = "dashboard"
host, port = "localhost", 5001  # Asegúrate de que esto coincide con la configuración del bus de servicios
service = Service(SERVICE_NAME, host, port)

# Configuración de PostgreSQL
db_config = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'localhost'  # Cambia 'postgres_db' a 'localhost'
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    print("Connecting to database with config:", db_config)  # Añadido para depuración
    conn = psycopg2.connect(**db_config)
    return conn

# Función para obtener datos de ventas desde PostgreSQL
def get_sales_data():
    conn = get_db_connection()
    query = """
    SELECT date, product, quantity, price
    FROM sales;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Función para obtener datos de inventario desde PostgreSQL
def get_inventory_data():
    conn = get_db_connection()
    query = """
    SELECT product, stock
    FROM inventory;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Función para generar gráfica de ventas del día
def generate_sales_chart(sales_df):
    if sales_df.empty:
        return None
    sales_today = sales_df[sales_df['date'] == pd.Timestamp('today').normalize()]
    if sales_today.empty:
        return None
    plt.figure(figsize=(10, 6))
    sales_today.groupby('product')['quantity'].sum().plot(kind='bar')
    plt.title('Ventas del Día')
    plt.xlabel('Producto')
    plt.ylabel('Cantidad Vendida')
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return image_base64

# Función para manejar la solicitud del dashboard
def handle_dashboard_request(data: str) -> str:
    try:
        sales_df = get_sales_data()
        inventory_df = get_inventory_data()

        # Generar gráfica de ventas del día
        sales_chart = generate_sales_chart(sales_df)

        # Calcular porcentaje de productos vendidos
        total_quantity = sales_df['quantity'].sum()
        if total_quantity == 0:
            product_percentage = {}
        else:
            product_percentage = sales_df.groupby('product')['quantity'].sum() / total_quantity * 100
            product_percentage = product_percentage.to_dict()

        # Preparar datos de inventario
        inventory_data = inventory_df.set_index('product').to_dict()['stock'] if not inventory_df.empty else {}

        response = {
            "sales_chart": sales_chart,
            "product_percentage": product_percentage,
            "inventory_data": inventory_data
        }
        return str(json.dumps(response))
    except Exception as e:
        return str(json.dumps({"error": str(e)}))

service.run_service(handle_dashboard_request)
