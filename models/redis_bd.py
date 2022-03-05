# Fernando Vizuet -----------------------------------------------
def conversion(url_larga: str) -> str:
    # Code here

    url_corta = "https://bit.ly/36Yvv9W"
    return url_corta


def add_liga_publica(url_larga, categoria) -> bool:

    # Hacer la conversion liga publica
    url_corta = conversion(url_larga)

    # Agregar a redis
    return True


# ---------------------------------------------------------------

### Fernando Avitua --------------------------------------------
def add_liga_publica(url_larga, categoria) -> bool:

    llaveDic = f"{url_larga}"

    # Hacer la conversion liga publica
    url_corta = conversion(url_larga)

    exito = r.hmset(llaveDic, {"url_corta": url_corta, "categoria": categoria})
    # Agregar a redis
    return exito


def dictBytes_a_dictString(diccionario):
    return {k.decode("utf-8"): v.decode("utf-8") for k, v in diccionario.items()}


# Crear ligas de user


def agregarUser(username, nombre, password):
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


def recuperaListas(username, categoria=""):
    cjto_url_pri = r.smembers(f"lpriv_{username}")
    lista_url_pri = [si.decode("utf-8") for si in cjto_url_pri]

    cjto_url_pub = r.smembers(f"{username}_pub")
    lista_url_pub = [si.decode("utf-8") for si in cjto_url_pub]

    categorias = {}
    for url in lista_url_pri:
        llaveDic = f"{username}_{url}"
        dict_url = dictBytes_a_dictString(r.hgetall(llaveDic))

        cat = dict_url["categoria"]
        url_corta = dict_url["url_corta"]

        if not categorias.get(cat):
            categorias[cat] = [url_corta]
        else:
            categorias[cat].append(url_corta)

    for url in lista_url_pub:
        llaveDic = f"{url}"
        dict_url = dictBytes_a_dictString(r.hgetall(llaveDic))

        cat = dict_url["categoria"]
        url_corta = dict_url["url_corta"]

        if not categorias.get(cat):
            categorias[cat] = [url_corta]
        else:
            categorias[cat].append(url_corta)

    return categorias


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


def verificar_usuario() -> bool:
    """Verifica si el usuario existe"""
    pass


def find_all_ligas_publicas() -> list:
    """Encuentra todas las ligas publicas"""
    pass


def find_all_liga_by_category(categoria) -> list:
    """Encuentras todas las lista del tal categoria"""
    pass


# -----------------------------------------------------------------
