# Buenas practicas


# for
```
for i, elemento in enumerate(elementos):
for i, elemento in enumerate(elementos, 5):

```


# IF en una sola linea
```
str(p.indicadores_id.mutualidad_id.codigo) if p.indicadores_id.mutualidad_id else '00',
```

```
lista = []

for elemento in elementos:
    lista.append(elemento.nombre)


lista = [elemento.nombre for elemento in elementos]

diccionario = {llave: valor for llave, valor in elementos.items()}

i += 1
```

# Codigos Lindos
```
int_rut = int_rut.replace("-", '')
```

# Operador ternario
```
var=1
resultado="Tiene valor" if var>0 else "No tiene valor"
```

# Evaluar funcion
```
largo = 12
ancho = 13
print eval('largo*ancho')
```

# Manejo de Excepciones
```
#-*- coding: utf-8 -*-

dividendo = 5
divisor = 0
try:
    c = dividendo / divisor
    print c
except:
    print "No se permite la division por cero"
```

# Manejo de Excepciones Capturando el Tipo
```
try:
    # aquí ponemos el código que puede lanzar excepciones
except IOError:
    # entrará aquí en caso que se haya producido
    # una excepción IOError
except ZeroDivisionError:
    # entrará aquí en caso que se haya producido
    # una excepción ZeroDivisionError
except:
    # entrará aquí en caso que se haya producido
    # una excepción que no corresponda a ninguno
    # de los tipos especificados en los except previos
```

# Codificando un caracter
```
vals['name'] = field['RAZON SOCIAL'].decode("latin-1").encode("utf-8")
```

# Suma
```
res += 1
res = res + 1
```

# Extraer una cadena
```
# -- coding: utf-8 --
var = "PO00002"
print var[0:2]
```

# Limpiar cadena espacio
```
s.strip()
```
# Redondea si es entero
```
value_p = id.fixed_price
            if (value_p % 1) == 0 or value_p.is_integer():
                value_p =  int(value_p)
```


# Comparación y Asignacion en una Línea
```
self.amount = total_advance > 0 and total_advance or self.sale_id.residual
```

