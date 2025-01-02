import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, session, redirect, url_for, request
from flask_session import Session

from src.entities.auth import *


app = Flask(__name__)
load_dotenv()

# ? configuracion de secret key para flash 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# ? configuracion de la session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

##################################################################################################################
    # RUTAS PRINCIPALES
##################################################################################################################

# !------------
@app.route('/')
def index():
    return render_template('index.html')

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
        current_page = {'route': 'login','text': 'Iniciar sesion'}
        context = {
            'current_page': current_page
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
        session['email'] = res['user'].email
        session['phone'] = res['user'].phone
        session['id_card'] = res['user'].id_card
        session['status'] = res['user'].status
        session['image'] = res['user'].image
        session['user_role'] = res['user'].user_role
        session['permissions'] = res['permissions']

        print(session)
        return redirect(url_for('login'))
    
    # SI EL METODO ES GET
    if request.method == 'GET':
        current_page = {'route': 'register','text': 'Registrarse'}
        context = {
            'current_page': current_page
        }
        print(session)
        return render_template('auth/login.html', context=context)





if __name__ == '__main__':
    app.run()