# Short links

![img](img/app.png)

Sistema de reducción de URLs
- Soporta el manejo de usuarios.
- Permitir que se tengan ligas publicas y ligas privadas.
- Cada usuario tiene una wishlist de los sitios que desean visitar en el futuro.
- Es posible de categorizar las URLs.

## Installation
~~~
# Opcional para crear un entorno virtual.
python3 -m venv env
source env/bin/activate

# Necesario para instalar todos los paquetes.
pip install -r requirements.txt
~~~
---

## Usage
~~~
# Opcional poner los parametros.
python app.py 127.0.0.1 6379

# Si no se ponen se usaran los valores por defecto.
python app.py
~~~

- El tercer argumento sera la direccion ip donde se esta corriendo redis, por defecto es `127.0.0.1`.

Para conocer la ip donde se esta corriendo de un contenedor de docker es con:

`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' contenedor_redis`

- El cuarto argumento será el puerto donde esta escuchando redis, por defecto es `6379`.
---

## Usage with Docker 
Creamos la arquitectura que seran todos los componentes de nuestra aplicación:
~~~
# Crea los contenedores de las imagenes indicadas y crea toda una red.
docker-compose up

# Eliminar todos los recursos ocupando, como los contenedores creados y la red.
docker-compose down
~~~
Una vez hecho esto estará todo listo para usarse.


## Contributors
- Fernando Santa Rita Vizuet ([@FSRV24](https://github.com/FSRV24) )
- Fernando Avitúa ([@FunkySpiderman](https://github.com/FunkySpiderman) )
- Guillermo Andrés ([@gandres-dev](https://github.com/gandres-dev) )