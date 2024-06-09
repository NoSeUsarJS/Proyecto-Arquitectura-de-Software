import psycopg2
from psycopg2 import sql

class DatabaseServer:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
    def create_connection(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname='postgres',
                user=self.user,
                password=self.password
            )
            self.conn.autocommit = True
            cursor = self.conn.cursor()

            # Verificar si la base de datos ya existe
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (self.dbname,))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.dbname)))
                print(f"Database '{self.dbname}' created successfully.")
            else:
                print(f"La base de datos '{self.dbname}' ya existe.")

            cursor.close()
            self.conn.close()

            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
    def query(self, query):
        try:
            auth = self.execute_query(query)
            if auth != None:
                return auth
        except Exception as e:
            return 'False'
    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if cursor.description is not None:
                result = cursor.fetchall()
                self.conn.commit()
                return result
            else:
                self.conn.commit()
                return None
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            cursor.close()
    def create_tables(self):
        try:
            create_persona_table = """
            CREATE TABLE IF NOT EXISTS persona (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(255),
                rut VARCHAR(12),
                rol BOOLEAN ,
                password VARCHAR(255)
            )
            """
            create_ingredientes_table = """
            CREATE TABLE IF NOT EXISTS ingredientes (
                id_Ingrediente SERIAL PRIMARY KEY,
                Nombre VARCHAR(255),
                Cantidad_ingredientes INT 
            )
            """
            create_platillo_table = """
            CREATE TABLE IF NOT EXISTS platillo (
                id_platillo SERIAL PRIMARY KEY,
                Nombre_platillo VARCHAR(255),
                Tiempo_medio_espera TIME,
                Precio INT,
                Descripcion TEXT
            )
            """
            create_Relacion_Ingrediente_Platillo_table = """
            CREATE TABLE IF NOT EXISTS Relacion_Ingrediente_Platillo (
                id_ingrediente INT,
                id_platillo INT,
                Cantidad_ingredientes INT,
                PRIMARY KEY (id_ingrediente, id_platillo),
                FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_Ingrediente),
                FOREIGN KEY (id_platillo) REFERENCES platillo(id_platillo)
            )
            """
            create_pedido_table = """
            CREATE TABLE IF NOT EXISTS pedido (
                id_Pedido SERIAL PRIMARY KEY,
                Mesa INT REFERENCES Mesa(Mesa),
                Hora TIME NOT NULL,
                id_persona INT REFERENCES persona(id)
            )
            """
            create_Relacion_Platillo_Pedido_table = """
            CREATE TABLE IF NOT EXISTS Relacion_Platillo_Pedido (
                id_platillo INT REFERENCES platillo(id_platillo),
                id_pedido INT REFERENCES pedido(id_Pedido),
                Comentario TEXT,
                PRIMARY KEY (id_platillo, id_pedido)
            )
            """
            create_mesa_table = """
            CREATE TABLE IF NOT EXISTS mesa (
                Mesa SERIAL PRIMARY KEY,
                Numero_personas INT
            )
            """
            create_Venta_table = """
            CREATE TABLE IF NOT EXISTS Venta (
                id_Venta SERIAL PRIMARY KEY,
                id_pedido INT REFERENCES pedido(id_Pedido),
                Precio_Total INT 
            )
            """
            self.execute_query(create_persona_table)
            self.execute_query(create_ingredientes_table)
            self.execute_query(create_platillo_table)
            self.execute_query(create_mesa_table)
            self.execute_query(create_pedido_table)
            self.execute_query(create_Relacion_Ingrediente_Platillo_table)
            self.execute_query(create_Relacion_Platillo_Pedido_table)
            self.execute_query(create_Venta_table)
            
            print("Tablas creadas con éxito.")
        except Exception as e:
            print(f"Error al crear las tablas: {e}")

server = DatabaseServer(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')
server.create_connection()
server.create_tables()

#Probar Query
#server.query("") #Igual se tendria q ver en el dockerfile de la base de datos lo q se haga, si es select, con print se ve todo
