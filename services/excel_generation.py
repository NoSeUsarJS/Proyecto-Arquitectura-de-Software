import pandas as pd
import psycopg2
from common.services import Service
import json
from datetime import datetime

# Configuración del servicio
SERVICE_NAME = "generate_excel"
host, port = "soabus", 5001  # Conectar con el bus de servicios en el puerto 5000
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

# Función para obtener los datos de ventas desde PostgreSQL
def get_sales_data():
    conn = get_db_connection()
    query = """
    SELECT date, product, quantity, price
    FROM sales;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Función para obtener los datos de inventario desde PostgreSQL
def get_inventory_data():
    conn = get_db_connection()
    query = """
    SELECT product, stock
    FROM inventory;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Función para generar el reporte en Excel
def generate_excel_report(sales_df, inventory_df, filename='sales_report.xlsx'):
    sales_df['date'] = pd.to_datetime(sales_df['date'])

    # Ventas diarias, semanales y mensuales
    ventas_diarias = sales_df.groupby(sales_df['date'].dt.date).agg({'quantity': 'sum', 'price': 'sum'}).reset_index()
    ventas_semanales = sales_df.groupby(sales_df['date'].dt.to_period('W')).agg({'quantity': 'sum', 'price': 'sum'}).reset_index()
    ventas_mensuales = sales_df.groupby(sales_df['date'].dt.to_period('M')).agg({'quantity': 'sum', 'price': 'sum'}).reset_index()

    # Total de ventas
    total_sales = sales_df['price'].sum()

    # Productos más vendidos
    productos_mas_vendidos = sales_df.groupby('product').agg({'quantity': 'sum'}).reset_index().sort_values(by='quantity', ascending=False)
    producto_mas_vendido = productos_mas_vendidos.iloc[0]

    # Generar el archivo Excel con todas las pestañas
    with pd.ExcelWriter(filename) as writer:
        ventas_diarias.to_excel(writer, sheet_name='Ventas Diarias', index=False)
        ventas_semanales.to_excel(writer, sheet_name='Ventas Semanales', index=False)
        ventas_mensuales.to_excel(writer, sheet_name='Ventas Mensuales', index=False)
        productos_mas_vendidos.to_excel(writer, sheet_name='Productos Más Vendidos', index=False)
        inventory_df.to_excel(writer, sheet_name='Inventario', index=False)

        # Agregar la hoja del total de ventas
        total_sales_df = pd.DataFrame({'Total Sales': [total_sales]})
        total_sales_df.to_excel(writer, sheet_name='Total Ventas', index=False)

        # Agregar la hoja del producto más vendido
        producto_mas_vendido_df = pd.DataFrame(producto_mas_vendido).transpose()
        producto_mas_vendido_df.to_excel(writer, sheet_name='Producto Más Vendido', index=False)

    print(f"Reporte generado: {filename}")

# Función para manejar la solicitud de generación de reporte
def generate_report(data: str) -> str:
    data = json.loads(data)
    sales_df = get_sales_data()  # Obtén los datos de ventas desde PostgreSQL
    inventory_df = get_inventory_data()  # Obtén los datos de inventario desde PostgreSQL
    generate_excel_report(sales_df, inventory_df)  # Genera el reporte en Excel
    response = {
        "message": "Reporte generado exitosamente."
    }
    return str(json.dumps(response))

service.run_service(generate_report)
