from src.entities.config_bd import *
from werkzeug.security import generate_password_hash, check_password_hash

def registerClient(username,email,password):
    user = db.execute(text("SELECT username, email, password FROM users WHERE username = :username OR email = :email"), {"username": username, "email": email}).fetchone()
    if user:
        return "No valido! Correo o Usuario ya existente"
    
    db.execute(text("INSERT INTO users (username, email, password, status, user_role) VALUES (:username, :email, :password, :status, :user_role)"), {"username": username, "email": email, "password": generate_password_hash(password), "status": True, "user_role": 'Cliente'})
    db.commit()
    return None

def login(email, password):
    user = db.execute(text("SELECT email, password FROM users WHERE email = :email"), {"email": email}).fetchone()
    if user and check_password_hash(user.password, password):
         return None
    
    return "Correo o contraseña incorrectos"

def obtainUserData(email):
    user = db.execute(text("SELECT user_id, username, email, phone, id_card, status, image, user_role FROM users WHERE email = :email"), {"email": email}).fetchone()
    permissions = db.execute(text("SELECT p.name FROM users as u JOIN user_permissions as up ON u.user_id = up.user_id JOIN permissions as p ON p.permission_id = up.permissions_id WHERE email = :email"), {"email": email}).fetchall()
    return {"user": user, "permissions": permissions}