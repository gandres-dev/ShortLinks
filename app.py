from unicodedata import category
from flask import Flask, render_template, request, redirect
from models.redis_bd import *

app = Flask(__name__)
username = ""
categories = ["Musica", "Educacion", "Ciencia"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrarse", methods=['GET', 'POST'])
def registrarse():
    if request.method == 'GET':
        return render_template("registrarse.html")
    else:
        username = request.form.get('username')
        nombre = request.form.get('nombre')
        password = request.form.get('password')
        exito = agregar_user(username, nombre, password)        
        return redirect('/')


@app.route("/addLink", methods=['GET', 'POST'])
def add_link():
    if request.method == 'GET':
        return render_template("addLink.html")
    else:
        url_larga = request.form.get('url_largo')
        liga = request.form.get('ligas')
        categoria = request.form.get('categoria')        
        if liga == 'publico':                          
            add_liga_publica_user(username, url_larga, categoria)            
        else:
            # Significa que es liga privada                      
            add_liga_privada_user(username, url_larga, categoria)
        url_corta = conversion(url_larga)              
        return render_template("/confirmacion.html", url_corta=url_corta)
    
# Le indicamos que le van mandar una peticion POST a perfil
@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    global username
    if request.method == 'GET':
        # Obtener las ligas publicas y privadas del usuario        
        ligas_pub, ligas_priv = recuperar_listas(username)  
        return render_template("perfil.html", username=username, ligas_pub=ligas_pub, ligas_priv=ligas_priv)
    else:
        # Obtenemos el contenido de la petición
        username = request.form.get("username")
        password = request.form.get("password")
        # Hacer verificaion si existe el usuario para ingresar al sistema
        if not existe_usuario(username, password):
            # Si no rediccionarlo a home
            return redirect("/")
        else:
            #Le pasamos los valores al html
            # Le pasamos las ligas publicas y privadas que tiene el usuario                        
            
            ligas_pub, ligas_priv = recuperar_listas(username)         
            return render_template("perfil.html", username=username, ligas_pub=ligas_pub, ligas_priv=ligas_priv)

@app.route("/tablero")
def tablero():
    ligas_publicas = find_all_ligas_publicas()   
    return render_template("tablero.html", ligas_publicas=ligas_publicas)

@app.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar_link():
    # Elimina link
    ligas = request.form.getlist('link')    
    for liga in ligas:
        borrar_liga(username, liga, True)
        borrar_liga(username, liga, False)
        
    return redirect("/perfil")
    

if __name__ == "__main__":
    app.run(debug=True)