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
    # MODELOS DE DATOS E INFORMACION DE LOS PRODUCTOS E INGRESOS DE PROVEEDORES
##################################################################################################################

class categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class sub_categories(db.Model):
    __tablename__ = 'sub_categories'
    sub_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class category_subcategories(db.Model):
    __tablename__ = 'category_subcategories'
    category_subcategories_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.sub_category_id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

# # ---------------------- PRODUCT DETAILLS MODELS --------------------------------

class measurement_units(db.Model):
    __tablename__ = 'measurement_units'
    measurement_unit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class colors(db.Model):
    __tablename__ = 'colors'
    color_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class sizes(db.Model):
    __tablename__ = 'sizes'
    size_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class brands(db.Model):
    __tablename__ = 'brands'
    brand_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


status_product = ENUM('active', 'inactive', 'damaged', 'lost', 'stolen', 'donated', name='status_product', create_type=True, metadata=db.metadata)

class products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sku = db.Column(db.Integer, nullable=False, unique=True, server_default=text("nextval('unique_id_seq_9digits')"))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.size_id'), nullable=True)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), nullable=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.brand_id'), nullable=True)
    status = db.Column(status_product, nullable=True, default='active')
    image = db.Column(db.String(100), nullable=True)
    unit_measurement_id = db.Column(db.Integer, db.ForeignKey('measurement_units.measurement_unit_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('sub_categories.sub_category_id'), nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())


class purchases(db.Model):
    __tablename__ = 'purchases'
    purchase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'), nullable=False)
    bill = db.Column(db.String(100), nullable=True)
    note = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    created_time = db.Column(db.Time, nullable=False, server_default=func.current_time())

class purchases_detail(db.Model):
    __tablename__ = 'purchases_detail'
    purchase_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.purchase_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
