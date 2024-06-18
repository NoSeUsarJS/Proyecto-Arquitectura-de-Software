# Proyecto Arquitectura de Software
 
Para correr el docker
docker-compose up -d

Para que funcione la base de datos (docker postgres)
pip install psycopg2
pip install openpyxl

para ver el bash de la bd:
docker exec -it postgres_db bash
psql -U myuser mydatabase

Ver tablas
\dt

Agregar a la tabla ventas:
ALTER TABLE usuarios ADD COLUMN fecha_insercion JSONB;

CREATE OR REPLACE FUNCTION actualizar_fecha_insercion()
RETURNS TRIGGER AS $$
BEGIN
  NEW.fecha_insercion := jsonb_build_object(
    'timestamp', CURRENT_TIMESTAMP
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insertar_fecha_insercion
BEFORE INSERT ON usuarios
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_insercion();
