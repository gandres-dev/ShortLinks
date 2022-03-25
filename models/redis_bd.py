import redis
import random
import string
import sys
import os
from redis.cluster import RedisCluster as Redis
from redis.cluster import ClusterNode


host_defecto = "127.0.0.1"
puerto_defecto = 6379
if len(sys.argv) > 1:
    host_defecto = sys.argv[1]

if len(sys.argv) > 2:
    puerto_defecto = int(sys.argv[2])

# Verificamos si existe esa variable de entorno
if os.environ['REDIS_URL']:
    host_defecto = os.environ['REDIS_URL']


nodes = [ClusterNode(os.environ['REDIS_URL'], 6379), ClusterNode(os.environ['REDIS_URL'], 6378)]
rc = Redis(startup_nodes=nodes)
print(rc.get_nodes())
#r = redis.Redis(host=host_defecto, port=puerto_defecto)
r = ""
# r.flushdb()

# Fernando Vizuet -----------------------------------------------


def conversion(url_larga: str) -> str:
    # Code here
    """
    Esta función hace una reducción de un URL dado
    y crea un par llave valor que te lleva al link
    original.
    """
    # Definimos una semilla
    random.seed(sum([ord(c) for i, c in enumerate(url_larga)]))
    letras = string.ascii_uppercase + string.ascii_lowercase + string.digits
    new_url = "https://bit.ly/" + "".join(random.choice(letras) for i in range(4))

    return new_url


# Fernando Avitua --------------------------------------------
def add_liga_publica(url_larga, categoria) -> bool:
    """Agrega ligas publicas"""
    llaveDic = f"{url_larga}"

    r.sadd("urls", url_larga)

    # Hacer la conversion liga publica
    url_corta = conversion(url_larga)

    exito = r.hmset(llaveDic, {"url_corta": url_corta, "categoria": categoria})
    # Agregar a redis
    return exito


def dictBytes_a_dictString(diccionario):
    """Codifica un dato de tipo binario a su correspondientes string utf-8"""
    return {k.decode("utf-8"): v.decode("utf-8") for k, v in diccionario.items()}


# Crear ligas de user
def agregar_user(username, nombre, password):
    """Agrega al usuario a la base de datos"""
    exito = r.hmset(username, {"nombre": nombre, "password": password})
    return exito


def add_liga_publica_user(username, url_larga, categoria) -> True:
    """Agregar liga publicas en una estructura de datos de conjuntos"""

    # También debe agregar a la lista pública
    add_liga_publica(url_larga, categoria)

    key_pub_usuario = f"{username}_pub"

    exito = r.sadd(key_pub_usuario, url_larga)

    return exito


def add_liga_privada_user(username, url_larga, categoria) -> True:
    """Crea la estructura de liga privada y agregar url_larga,url_corta y categoria"""

    # Creamos el set de ligas privadas
    r.sadd(f"lpriv_{username}", url_larga)

    # Creamos un diccionario por cada url_larga
    url_corta = conversion(url_larga)

    exito = r.hmset(
        f"{username}_{url_larga}", {"url_corta": url_corta, "categoria": categoria}
    )
    return exito


# Read
def recuperar_listas(username):
    cjto_url_pri = r.smembers(f"lpriv_{username}")
    lista_url_pri = [si.decode("utf-8") for si in cjto_url_pri]

    cjto_url_pub = r.smembers(f"{username}_pub")
    lista_url_pub = [si.decode("utf-8") for si in cjto_url_pub]

    categorias_pri = {}
    categorias_pub = {}
    for url in lista_url_pri:
        llaveDic = f"{username}_{url}"
        dict_url = dictBytes_a_dictString(r.hgetall(llaveDic))

        cat = dict_url["categoria"]
        url_corta = dict_url["url_corta"]

        if not categorias_pri.get(cat):
            categorias_pri[cat] = [url_corta]
        else:
            categorias_pri[cat].append(url_corta)

    for url in lista_url_pub:
        llaveDic = f"{url}"
        dict_url = dictBytes_a_dictString(r.hgetall(llaveDic))

        cat = dict_url["categoria"]
        url_corta = dict_url["url_corta"]

        if not categorias_pub.get(cat):
            categorias_pub[cat] = [url_corta]
        else:
            categorias_pub[cat].append(url_corta)

    return categorias_pub, categorias_pri


# Delete
def borrar_liga_priv(username, url_corta):

    for url_larga in r.smembers(f"lpriv_{username}"):

        dicc_nombre = f"{username}_{url_larga.decode('utf-8')}"
        url_corta1 = r.hget(dicc_nombre, "url_corta")

        if url_corta == url_corta1.decode("utf-8"):
            # Se quita la liga del conjunto lpriv_username
            r.srem(f"lpriv_{username}", url_larga)

            # Se elimina el diccionario con llave dicc_nombre
            r.delete(dicc_nombre)

            break  # Termina el loop si ya se encontró

    return True


def borrar_liga_pub(username, url_corta):

    for url_larga in r.smembers(f"{username}_pub"):

        dicc_nombre = f"{url_larga.decode('utf-8')}"
        url_corta1 = r.hget(dicc_nombre, "url_corta")

        if url_corta == url_corta1.decode("utf-8"):
            # Se quita la liga del conjunto username_pub
            r.srem(f"{username}_pub", url_larga)

            # Se quita del conjunto url
            r.srem("urls", url_larga)

            # Se elimina el diccionario con llave dicc_nombre
            r.delete(dicc_nombre)

            break  # termina el loop si ya se encontró

    return True


# Función que elimina una liga especificando si es publica
def borrar_liga(username, url_corta, publico=True):
    if publico:
        return borrar_liga_pub(username, url_corta)

    return borrar_liga_priv(username, url_corta)


# Update
def actualizar_liga(username, liga, categoria_nueva):

    key_liga = f"{username}_{liga}"
    exito = r.hset(name=key_liga, key="categoria", value=categoria_nueva)

    return exito


# -----------------------------------------------------------------


def existe_usuario(username, password) -> bool:
    """Verifica si el usuario existe"""
    if not username or not password:
        return False
    existe = r.hmget(username, "password")
    print(existe)
    if existe[0]:
        password_user = existe[0].decode("utf-8")
        if password_user == password:
            # print("Entro")
            return True
    return False


def find_all_ligas_publicas() -> dict:
    """Encuentra todas las ligas publicas"""
    dict_categoria = {}
    for url in r.smembers("urls"):
        # lista.append(i.decode("utf-8"))
        # lista.append((i.decode("utf-8"), r.get(i.decode("utf-8"))))
        url_to = url.decode("utf-8")
        llave_dict = f"{url_to}"
        dict_url = dictBytes_a_dictString(r.hgetall(llave_dict))
        categoria = dict_url["categoria"]
        url_corta = dict_url["url_corta"]
        if not dict_categoria.get(categoria):
            dict_categoria[categoria] = [url_corta]
        else:
            dict_categoria[categoria].append(url_corta)
    return dict_categoria


def find_all_liga_by_category(categoria) -> list:
    """Encuentras todas las lista del tal categoria"""
    # lista = []
    # for i in find_all_ligas_publicas():
    #     if r.hvals(i)[1].decode("utf-8") == categoria:
    #         lista.append(r.hvals(i)[0].decode("utf-8"))
    pass
    # return lista


# -----------------------------------------------------------------
