# Impresoras
PosBox es compatible con impresoras térmicas como as la EPSON TM-T20, la EPSON TM-T70, la EPSON TM-T88 y la Star TSP650II.


# Cajas regstradoras
Metapace K-2

# Balanza de peso
El PosBox admite por defecto Mettler Toledo Ariva familia de productos. El ADAM Equipamiento AZExtra La familia también se incluye (a partir de v15). 


# Escaner
De todos los escáneres de códigos de barras, recomendamos Honeywell Eclipse línea del producto. Son compatibles desde el primer momento con el PosBox. Si los conecta directamente a la computadora de escritorio será necesario configurarlos para poder utilizar la disposición del teclado de su computadora.

```
1
```

# Links:
Información de HardWare

https://www.odoo.com/es_ES/page/point-of-sale-hardware

# Notas Interesantes

	

2/12/14


El PosBox no es más que un Raspberry pi ( Modelo b+) con una tarjeta Micro SD con la imagen del disco del proyecto de Odoo para Posbox que te puedes descargar aquí : 

http://nightly.odoo.com/trunk/posbox/

Una vez lo tengas bajada la imagen  ( la última es la V10)  la "metes" en una tarjeta Micro SD de 8 Gb con un programa para hacer "arrancable" la tarjeta, es decir para que la Raspberry arranque desde la Micro SD . Puedes hacerlo ( en linux con el comando dd)  en Windows con el programa "Win32 Disk Imager". Esto no te llevará mas de dos minutos.

Después de encender la Raspberry (recuerda meter la MicroSD con la imagen antes de conectarla) Le conectas el cable de red y desúes la impresora de tickets por usb ( La Epson TM T20II funciona de maravilla) Si lo has hecho todo bien, te saldrá por la impresora  un "ticket" con la Ip que se le ha asignado desde el Router a la Raspberry. Entras en Odoo y en la configuración del TPV le dices que utilice el proxy para imprimir y le pones la IP anterior y a funcionar.

Coste aproximado :

Raspberry Pi  B+ 32 € 
Impresora Epson TMII 120 € 
Cualquier Lector laser normal de mano,  desde 60 € en adelante
Un cajón portamonedas , sobre 80 €

Ah, y la Micro SD 7€

El ahorro es considerable y funciona de maravilla (dependiendo del tipo de negocio que quieras manejar con el TPV de Odoo).


