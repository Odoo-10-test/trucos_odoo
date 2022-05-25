https://sqliteonline.com/

# Borrado de Factura por id
````
delete from account_move where old_id in (22001733,#,#)
````


# Actualizar Factura
````
update account_move set name = concat('F',old_id) where old_id <> 0
````

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
