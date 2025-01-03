import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, session, redirect, url_for, request
from flask_session import Session
from functools import wraps
from flask import make_response

from src.entities.auth import *


app = Flask(__name__)
load_dotenv()

# ? configuracion de secret key para flash 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# ? configuracion de la session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def no_cache(view):
    def wrapped_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return wrapped_view

##################################################################################################################
    # RUTA INICIAL
##################################################################################################################

# !------------
@app.route('/')
def index():
    context = {
        'current_page': currentPage('logout') if session.get('user_id') else currentPage('login')
    }
    return render_template('index.html', context=context)

##################################################################################################################
    # RUTAS DE REGISTRO E INICIO DE SESION
##################################################################################################################

# TODO:----------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def registerClient():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # MOSTRAR ERRORES
        if errorOnRegister := validateClientCredentials(username, email, password, 'register'):
            flash(errorOnRegister, 'error')
            return redirect(url_for('registerClient'))
        
        # CONTIUAR SI ESTA CORRECTO
        flash("Usuario registrado exitosamente", 'register')
        return redirect(url_for('login'))
    
    # SI EL METODO ES GET
    if request.method == 'GET':
        context = {
            'current_page': currentPage('logout') if session.get('user_id') else currentPage('login')
        }
        print(session)
        return render_template('auth/register.html', context=context)
    
# TODO:------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # MOSTRAR ERRORES
        if errorOnRegister := validateClientCredentials("None", email, password, 'login'):
            flash(errorOnRegister, 'error')
            return redirect(url_for('login'))
        
        # CONTIUAR SI ESTA CORRECTO
        res = obtainUserData(email)
        session['user_id'] = res['user'].user_id
        session['username'] = res['user'].username
        session['user_role'] = res['user'].user_role
        session['permissions'] = res['permissions']

        print(session)
        return redirect(url_for('catalog'))
    
    # SI EL METODO ES GET
    if request.method == 'GET':
        context = {
            'current_page': currentPage('logout') if session.get('user_id') else currentPage('register')
        }
        print(session)
        return render_template('auth/login.html', context=context)

##################################################################################################################
    # RUTAS DEL CATALOGO
##################################################################################################################

@app.route('/catalog')
def catalog():
    context = {
        'current_page': currentPage('logout') if session.get('user_id') else currentPage('login')
    }
    print(session)
    return render_template('catalog/catalog.html', context=context)

# perfil
@app.route('/profile')
@login_required
@no_cache
def profile():
    context = {
        'current_page': currentPage('logout')
    }
    
    print(session)
    return render_template('catalog/profile.html', context=context)



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

##################################################################################################################
    # RUTAS DEL SISTEMA
##################################################################################################################

@app.route('/home')
def home():
    return 'Home'

@app.route('/dashboards')
def dashboard():
    return 'Dashboard'

@app.route('/operators')
def operators():
    return 'Operators'

@app.route('/providers')
def providers():
    return 'Providers'

@app.route('/sells')
def sells():
    return 'Sells'

@app.route('/returns')
def returns():
    return 'Returns'

@app.route('/reservations')
def reservations():
    return 'Reservations'

@app.route('/buys')
def buys():
    return 'Buys'

@app.route('/products')
def products():
    return 'Products'

@app.route('/configurations')
def configurations():
    return 'Configurations'

##################################################################################################################
    # FUNCIONES DE UTILIDAD
##################################################################################################################

def currentPage(route):
    routes = {
        'login': {'route': 'login', 'text': 'Iniciar sesion'},
        'register': {'route': 'register', 'text': 'Registrarse'},
        'logout': {'route': 'logout', 'text': 'Cerrar sesion'}
    }
    return routes.get(route)


if __name__ == '__main__':
    app.run()