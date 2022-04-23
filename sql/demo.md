https://sqliteonline.com/

# Crear tabla
````
CREATE TABLE empleados (
 DNI INTEGER NOT NULL,
 NOMBRE VARCHAR(255),
 APELLIDO VARCHAR(255),
 SUELDO FLOAT);
````

# Insertar tabla
````
inSERT INTO empleados(DNI, NOMBRE, APELLIDO, SUELDO, EDAD) VALUES (122122, "Luna", "Perez", 222, 33)
````


# Seleccional tabla
````
SELECT * FROM empleados;
SELECT * FROM empleados WHERE sueldo > 13 ORDER BY DNI;
````

# Actualizar tabla
````
UPDATE empleados SET edad = 23 WHERE sueldo > 12;
````
