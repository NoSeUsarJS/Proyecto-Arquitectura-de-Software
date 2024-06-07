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
    def create_user(self, nombre,rut,rol,password):
        try:
            query = f"INSERT INTO persona (nombre, rut, rol, password) VALUES ({nombre},{rut},{rol},{password})"
            auth = self.execute_query(query)
            if auth:
                print("Se ha creado el usuario")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
        
    def login(self, nombre, password):
        try:
            query = f"SELECT * FROM persona WHERE nombre = '{nombre}' AND password = '{password}'"
            auth = self.execute_query(query)
            if auth:
                print(auth)
                return 'True'
            else:
                print(auth)
                return 'Wrong'
        except Exception as e:
            return 'False'
        
    def borrar_user(self, ID):
        try:
            query = f"DELETE FROM persona WHERE id = '{ID}' "
            auth = self.execute_query(query)
            if auth:
                print("Borre, con exito al usuario con el ID: ",ID)
                return 'True'
            else:
                print(auth)
                return 'Wrong'
        except Exception as e:
            return 'False'
        
    def ver_personal(self):
        try:
            query = f"SELECT * FROM persona"
            auth = self.execute_query(query)
            if auth:
                print(auth)
                return 'True'
            else:
                print(auth)
                return 'Wrong'
        except Exception as e:
            return 'False'
    def create_mesa(self,numero,cantidad):
        try:
            query = f"INSERT INTO mesa (mesa, numero_personas) VALUES ({numero},{cantidad})"
            auth = self.execute_query(query)
            if auth:
                print("Se ha creado la mesa")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
    def ver_mesas(self):
        try:
            query = f"SELECT * FROM mesa"
            auth = self.execute_query(query)
            if auth:
                print(auth)
                return 'True'
            else:
                print(auth)
                return 'Wrong'
        except Exception as e:
            return 'False'
    def actualizar_mesa(self,numero,cantidad):
        try:
            query = f"UPDATE mesa SET numero_personas = {cantidad} WHERE mesa = {numero}"
            auth = self.execute_query(query)
            if auth:
                print("Se ha creado la mesa")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
    def borrar_mesa(self,numero):
        try:
            query = f"DELETE FROM mesa WHERE mesa = {numero} "
            auth = self.execute_query(query)
            if auth:
                print("Se ha borrado la mesa")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
    
    def ver_ingredientes(self):
        try:
            query = f"SELECT * FROM ingredientes"
            auth = self.execute_query(query)
            if auth:
                print(auth)
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'

    def crear_ingrediente(self, nombre,cantidad):
        try:
            query = f"INSERT INTO ingredientes ( nombre, cantidad_ingredientes) VALUES ({nombre},{cantidad})"
            auth = self.execute_query(query)
            if auth:
                print("Se ha creado el ingrediente")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
        
    def actualizar_ingrediente(self,numero,cantidad):
        try:
            query = f"UPDATE ingredientes SET cantidad_ingredientes = {cantidad} WHERE id_ingrediente = {numero}"
            auth = self.execute_query(query)
            if auth:
                print("Se ha creado la mesa")
                return 'True'
            else:
                return 'Wrong'
        except Exception as e:
            return 'False'
        
    def borrar_ingrediente(self,numero):
        try:
            query = f"DELETE FROM ingredientes WHERE id_ingrediente = {numero} "
            auth = self.execute_query(query)
            if auth:
                print("Se ha borrado la el ingrediente")
                return 'True'
            else:
                return 'Wrong'
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


# Reemplaza los valores con la información de tu base de datos
server = DatabaseServer(host='localhost', port='5432', dbname='mydatabase', user='myuser', password='mypassword')

server.create_connection()
server.create_tables()

#server.create_user("'diego'","'26843998-6'","false","'mi_password_secreto'") #Sirve para agregar {Nombre} {RUT} {true o false} {password} del cliente

#server.login("diego","mi_password_secreto") # Sirve muestra la matriz retornar true para el login ? q lo envie de vuelta al servicio
#server.login("iego","mi_password_secreto") # muestra el resultado q es vacio
#server.create_user("'A'","'25678974-6'","true","'mi_password_secreto'")
#server.ver_personal() # devuelve matriz de matriz de personas
#server.borrar_user(2)
#server.ver_personal()

#server.create_mesa(1,4)
#server.ver_mesas()
#server.actualizar_mesa(1,2)
#server.ver_mesas()
#server.borrar_mesa(1)
#server.ver_mesas()

#server.crear_ingrediente("'Arroz'",50)
#server.ver_ingredientes()
#server.actualizar_ingrediente(1,10)
#server.ver_ingredientes()
#server.borrar_ingrediente(1)
#server.ver_ingredientes()

