# rsync

El comando linux rsync es una herramienta rápida y muy versátil para copiar archivos de forma local o remota. Así se describe este comando cuando ves la ayuda del comando man respecto al comando rsync. Este comando permite realizar una copia exacta de un archivo o directorio, en este último caso incluyendo todos los elementos dentro de este directorio, incluyendo todas las rutas y archivos, incluidos sus permisos y propiedades.

Una de las ventajas mas interesantes de este comando es que puede comprobar las dos rutas y actualizar solo los archivos nuevos y los que han cambiado de una ruta a otra. Si se interrumpiera el comando antes de concluir, solo basta con ejecutar de nuevo el comando y detectará cuales archivos faltaron para continuar donde se interrumpió.

```
rsync -avt *.sql root@157.230.8.181:/root
```


