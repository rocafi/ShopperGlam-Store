import os
from dotenv import load_dotenv
from flask import Flask, flash, render_template, session, redirect, url_for, request
from flask_session import Session

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

@app.route('/')
def index():
    return render_template('general/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('general/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # SI EL METODO ES POST
    if request.method == 'POST':
            return redirect(url_for('register'))
    # SI EL METODO ES GET
    if request.method == 'GET':
        return render_template('general/register.html')



if __name__ == '__main__':
    app.run()