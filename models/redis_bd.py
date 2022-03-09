from tkinter.ttk import PanedWindow
import redis

r = redis.Redis(host="127.0.0.1", port=6379)

# Fernando Vizuet -----------------------------------------------


def conversion(url_larga: str) -> str:
    # Code here
    """
    Esta función hace una reducción de un URL dado
    y crea un par llave valor que te lleva al link
    original.
    """
    # ¡¡¡¡¡¡¡¡¡¡¡¡¡librerías necesarias!!!!!!!!!!!!!!
    # import random
    # import string

    letras = string.ascii_uppercase + string.ascii_lowercase + string.digits
    new_url = "https://bit.ly/" + "".join(random.choice(letras) for i in range(4))

    return new_url


def add_liga_publica(url_larga, categoria) -> bool:

    # Hacer la conversion liga publica
    url_corta = conversion(url_larga)

    # Agregar a redis
    return True


# ---------------------------------------------------------------

# Fernando Avitua --------------------------------------------
def add_liga_publica(url_larga, categoria) -> bool:

    llaveDic = f"{url_larga}"

    r.sadd("urls", url_larga)
    # Hacer la conversion liga publica
    url_corta = conversion(url_larga)

    exito = r.hmset(llaveDic, {"url_corta": url_corta, "categoria": categoria})
    # Agregar a redis
    return exito


def dictBytes_a_dictString(diccionario):
    return {k.decode("utf-8"): v.decode("utf-8") for k, v in diccionario.items()}


# Crear ligas de user
def agregar_user(username, nombre, password):
    """Agrega al usuario a la base de datos"""
    exito = r.hmset(username, {"nombre": nombre, "password": password})
    return exito


def add_liga_publica_user(username, url_larga, categoria) -> True:
    # Agregar liga publicas en una estructura de datos
    # de conjuntos

    # checar si existe user, no se necesita

    # También debe agregar a la lista pública
    add_liga_publica(url_larga, categoria)

    key_pub_usuario = f"{username}_pub"

    exito = r.sadd(key_pub_usuario, url_larga)

    return exito


def add_liga_privada_user(username, url_larga, categoria) -> True:
    # Crear la estructura de liga privada
    # y agregar url_larga,url_corta y categoria

    # Creamos el set de ligas privadas

    r.sadd(f"lpriv_{username}", url_larga)

    # Creamos un diccionario por cada url_larga
    url_corta = conversion(url_larga)

    exito = r.hmset(
        f"{username}_{url_larga}", {"url_corta": url_corta, "categoria": categoria}
    )
    return exito


# Read
def recuperaListas(username):
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

    return categorias_pri, categorias_pub


# Delete
def borrarLiga(username, url_larga):
    key_url = f"{username}_{url_larga}"
    print(key_url)
    return r.delete(key_url)


# Update
def actualizarLiga(username, liga, categoria_nueva):

    key_liga = f"{username}_{liga}"
    exito = r.hset(name=key_liga, key="categoria", value=categoria_nueva)

    return exito


# -----------------------------------------------------------------


# Funciones que faltan implementar----------------------------------
def add_user(username, age, password) -> bool:
    """Agrega al usuario a la base de datos"""
    pass


def existe_usuario(username, password) -> bool:
    """Verifica si el usuario existe"""
    if not username or not password:
        return False
    existe = r.hmget(username, "password")
    if existe:
        password_user = existe[0].decode("utf-8")
        if password_user == password:
            # print("Entro")
            return True
    return False


def find_all_ligas_publicas() -> list:
    """Encuentra todas las ligas publicas"""

    lista = []

    for i in r.smembers("urls"):
        lista.append(i.decode("utf-8"))

    return lista


def find_all_liga_by_category(categoria) -> list:
    """Encuentras todas las lista del tal categoria"""

    lista = []

    for i in find_all_ligas_publicas:
        if r.hvals(i)[0].decode("utf-8") == categoria:
            lista.append(r.hvals(i)[0].decode("utf-8"))

    return lista


# -----------------------------------------------------------------
