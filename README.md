# Centro dee Documentación - Migración de vase de datos

## Ejecutar migración completa:
Movernos al directorio scripts_python.
Ejecutar el script: `.\script_total <password>`  
Donde `password` es la contraseña del usuario root en el puerto `3306`, en host `"localhost"` o `"127.0.0.1"`.  
Cualquiera de estos se puede cambiar desde el método main de los seis scripts de python, si fuera necesario.   

## Listado de scripts, y su locación.
`./scripts_python/FotoRodajes.py`     
`./scripts_python/fotomontajes.py`  
`./scripts_python/vhs_dvd/VhsDvd.py`    
`./scripts_python/cartel/cartel.py`  
`./scripts_python/stills/stills.py `   
`./scripts_python/person/person.py `   

## Notas
Dentro de cada script de python se pueden acotar las pruebas. Para aglizar.  
    
Para los scripts `person`, `cartel` y `stills` se hace descomentando la linea  
`data = data[0:10]`, donde se marca un nuevo rango de la lista inicial. 
  
Para los restantes, `FotoRodajes`, `Fotomontajes` y `VhsDvd`, dentro del `main`, en el loop principal, se modifica la cota superior del rango principal del if `if item[0] >= 1 and item[0] <= 100000`

## Datos especificcos de algunas tablas.
### Para ejecutar tabla única
 - **Correr PeliculasConexionDB.py**, para recolectar los datos de la tabla unica (la anterior), limpiar y procesarla, y termina en el archivo cd_vhs_dvd.csv. Debería usarse solo si los datos de unica cambian, o se modifica el parseo.
 - **Correr VhsDvd.py** para insertar a la nueva base.

 ## Sobre crear la migración desde el dump.
 1- Ejecutar el script del dump sql en alguna base de datos, para actualizar la base.
 2- Correr PeliculasConexion.py, para actualizar el csv de la tabla unica.
 3- Hacer un export de los datos de Stills. Usando el query en stills.py, y reemplazar el stills.json.
 4- Hacer un export de los datos de Personalidades. Usando el query en person.py, y reemplazar person.json.
 5- Para Cartel, hace falta ir a `cartel car union.sql`  
  donde se agrega un atributo car_consulta a la tabla original de cartel, y se exporta a dos diferentes Json, en este caso no se usa un query pues el select * por defecto que usa workbench es suficiente. no hay renombre de tablas.
 6- Para FotoRodajes dentro de FotoRodajes.py se deja el query para exportar la tabla a .csv. 
 6- Para el resto de los scripts no basta crear sus .json ya que en tiempo de ejecución hace la consulta a la base de datos directamente.


