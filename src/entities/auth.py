from src.entities.query import *


def validateClientCredentials(username, email, password, action):
    if action == 'register':
        required = {'Usuario': username, 'Correo': email, 'Contraseña': password}
    
        for field, value in required.items():
            if not value:
                return f"El campo '{field}' es obligatorio"
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres"

        if data := registerClient(username,email,password):
            return data

        return None

    if action == 'login':
        required = {'Correo': email, 'Contraseña': password}
    
        for field, value in required.items():
            if not value:
                return f"El campo '{field}' es obligatorio"
        if len(password) < 8:
            return "La contraseña fue de al menos 8 caracteres"
        if data := login(email, password):
            return data

        return None


    