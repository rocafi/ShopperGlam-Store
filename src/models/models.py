from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

##################################################################################################################
    # MODELOS RELACIONADOS A LOS USUARIOS Y SUS ROLES
##################################################################################################################

class users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    id_card = db.Column(db.String(16), nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.String(1000), nullable=True)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

class roles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

class user_roles(db.Model):
    __tablename__ = 'user_roles'
    user_role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

##################################################################################################################
    # MODELOS RELACIONADOS A LOS USUARIOS Y SUS ROLES
##################################################################################################################