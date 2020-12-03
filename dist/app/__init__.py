from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)
csrf = CSRFProtect(app)
UPLOAD_FOLDER = './app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db_admin:Gofigure876@localhost/pooldb'

db = SQLAlchemy(app)

# Login manger
login_mananger = LoginManager()
login_mananger.init_app(app)
login_mananger.login_view = 'login'
login_mananger.login_message = 'Please log in to access this page!'


from app import views
