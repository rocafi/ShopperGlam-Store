import os
from flask import Flask
from dotenv import load_dotenv

from models import db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

def create_app():
    db.drop_all()
    db.create_all()
    print("Tablas creadas")

if __name__ == '__main__':
    with app.app_context():
        create_app()