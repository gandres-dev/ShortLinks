# Short links
Sistema de reducción de URLs
- Soporta el manejo de usuarios.
- Permitir que se tengan ligas publicas y ligas privadas.
- Cada usuario tiene una wishlist de los sitios que desean visitar en el futuro.
- Es posible de categorizar las URLs.

## Installation
~~~
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
~~~
---

## Usage
~~~
python app.py 127.0.0.1 6379
~~~

- El tercer argumento sera la direccion ip donde se esta corriendo redis, por defecto es `127.0.0.1`.

Para conocer la ip donde se esta corriendo de un contenedor de docker es con:

`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' contenedor_redis`

- El cuarto argumento será el puerto donde esta escuchando redis, por defecto es `6379`.
---
##  Resources
Flask

- https://youtu.be/Yz1gUwXPPJw
- https://youtu.be/i_zS8nt7LGk

Redis with flask

- https://youtu.be/sgJZna1fJH4
- https://youtu.be/CC_7BlTUtGw

## Contributors
- Fernando Santa Rita Vizuet ([@FSRV24](https://github.com/FSRV24) )
- Fernando Avitúa ([@FunkySpiderman](https://github.com/FunkySpiderman) )
- Guillermo Andrés ([@gandres-dev](https://github.com/gandres-dev) )