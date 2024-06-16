import pandas as pd
from datetime import datetime
import os
import psycopg2

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
        print("Generando Excel de comidas...")
        query = f"SELECT * FROM platillo"
        response = Enviar(query)
        matriz = json.loads(response)
        
        for i in range(len(matriz)):
            id = matriz[i][0]
            nombre = matriz[i][1]
            tiempo = matriz[i][2]
            precio = matriz[i][3]
            descripcion = matriz[i][4]
        
        response = "Excel de comidas generado"

    elif action == "2":
        print("Generando Excel...")
        query = f"SELECT * FROM ingredientes"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        
        for i in range(len(matriz)):
            id = matriz[i][0]
            nombre = matriz[i][1]
            cantidad = matriz[i][2]
            
        response = "Excel de ingredientes generado"
    elif action == "3":
        print("Generando Excel...")
        query = f"SELECT * FROM persona"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        
        for i in range(len(matriz)):
            id_persona = matriz[i][0]
            nombre = matriz[i][1]
            rut = matriz[i][2]
            rol = matriz[i][3]
            password = matriz[i][4]
            
        response = "Excel de personas generado"
    elif action == "4":
        print("Generando Excel...")
        query = f"SELECT * FROM venta"
        response = Enviar(query)
        
        
        matriz = json.loads(response)
        
        for i in range(len(matriz)):
            id_venta = matriz[i][0]
            id_pedido = matriz[i][1]
            precio_total = matriz[i][2]
           
        response = "Excel de ventas generado"
    else:
        response = "Acción no válida."
    
    print("Sending response:", response) 
    
    return response 
# "db_manager": "SV005",
# Inicializar y ejecutar el servicio
inventory_service = Service(service_name="generate_excel", host="localhost", port=5001)
inventory_service.run_service(handle_inventory_request)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    print("Connecting to database with config:", db_config)  # Añadido para depuración
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

# Función para obtener la ruta del escritorio
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

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
    producto_mas_vendido = productos_mas_vendidos.iloc[0] if not productos_mas_vendidos.empty else {}

    # Generar el archivo Excel con todas las pestañas
    desktop_path = get_desktop_path()
    full_path = os.path.join(desktop_path, filename)
    with pd.ExcelWriter(full_path) as writer:
        ventas_diarias.to_excel(writer, sheet_name='Ventas Diarias', index=False)
        ventas_semanales.to_excel(writer, sheet_name='Ventas Semanales', index=False)
        ventas_mensuales.to_excel(writer, sheet_name='Ventas Mensuales', index=False)
        productos_mas_vendidos.to_excel(writer, sheet_name='Productos Más Vendidos', index=False)
        inventory_df.to_excel(writer, sheet_name='Inventario', index=False)

        # Agregar la hoja del total de ventas
        total_sales_df = pd.DataFrame({'Total Sales': [total_sales]})
        total_sales_df.to_excel(writer, sheet_name='Total Ventas', index=False)

        # Agregar la hoja del producto más vendido
        if not producto_mas_vendido.empty:
            producto_mas_vendido_df = pd.DataFrame(producto_mas_vendido).transpose()
            producto_mas_vendido_df.to_excel(writer, sheet_name='Producto Más Vendido', index=False)

    print(f"Reporte generado: {full_path}")

