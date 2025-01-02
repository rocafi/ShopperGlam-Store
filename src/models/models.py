from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ENUM

db = SQLAlchemy()

##################################################################################################################
    # MODELOS RELACIONADOS A LOS USUARIOS Y SUS ROLES
##################################################################################################################

roles = ENUM('Administrador','Operador', 'Cliente', name='roles', create_type=True, metadata=db.metadata)

class users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    id_card = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.String(1000), nullable=True)
    user_role = db.Column(roles, nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

class permissions(db.Model):
    __tablename__ = 'permissions'
    permission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

class user_permissions(db.Model):
    __tablename__ = 'user_permissions'
    user_permissions_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    permissions_id = db.Column(db.Integer, db.ForeignKey('permissions.permission_id'), nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

##################################################################################################################
    # 
##################################################################################################################