# Remplazar Cadena
```
int_rut = int_rut.replace("-", '')
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

# Limpiar cadena espacio
```
s = 'wwwthisisasstringooo' s.strip()
```
