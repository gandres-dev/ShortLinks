from flask import Flask, render_template, request, redirect
from models.redis_bd import *

app = Flask(__name__)
username = ""


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrarse", methods=['GET', 'POST'])
def registrarse():
    if request.method == 'GET':
        return render_template("registrarse.html")
    else:
        username = request.form.get('username')
        age = request.form.get('age')
        password = request.form.get('password')
        #add_user(username, age, password)
        return redirect('/')


@app.route("/addLink", methods=['GET', 'POST'])
def add_link():
    if request.method == 'GET':
        return render_template("addLink.html")
    else:
        url_larga = request.form.get('url_largo')
        liga = request.form.get('ligas')
        categoria = request.form.get('categoria')
        # print(url_larga); print(liga); print(categoria)
        if liga == 'publica':
            add_liga_publica(url_larga, categoria)
            add_liga_publica_user(username, url_larga)
        else:
            add_liga_privada_user(username, url_larga, categoria)        
        
        return redirect('/confirmacion')
    
# Le indicamos que le van mandar una peticion POST a perfil
@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    if request.method == 'GET':
        return render_template('perfil.html')
    else:
        # Obtenemos el contenido de la petición
        global username
        username = request.form.get("username")
        # Hacer verificaion si existe el usuario para ingresar al sistema
        # if not verificar():
            # Si no rediccionarlo a home
            #return redirect("index.html")
        # else:
        # Le pasamos los valores al html
        return render_template("perfil.html", username=username)

@app.route("/tablero")
def tablero():
    ligas_publicas = find_all_ligas_publicas()    
    return render_template("tablero.html", ligas_publicas=ligas_publicas)

@app.route("/confirmacion")
def confirmacion():
    return render_template("confirmacion.html")

if __name__ == "__main__":
    app.run(debug=True)