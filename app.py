from bson import ObjectId
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import uuid
from pymongo import ReturnDocument



app = Flask(__name__)
app.secret_key = "supersecretkey"  # Changez cette clé pour sécuriser votre application

# Configuration MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydb"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Flask-Login Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



#import des différentes routes du system de log
from systeme_log import *
from sondage_systeme import *
from Obtenir_Mes_Sondages import *
from Route_basique import *
from request_friend import *
from Liste_sondage import *
from Modifie_profile import *




if __name__ == '__main__':
    app.run(debug=True)
