import json

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

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Vous pouvez ici ajouter des informations à transmettre au template (comme l'utilisateur connecté)
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET'])
@login_required  # Assure que seul un utilisateur connecté peut accéder à cette route
def profile():
    # Récupération des informations de l'utilisateur depuis MongoDB
    user_data = mongo.db.users.find_one({"_id": current_user.id})
    if not user_data:
        return jsonify({"message": "User not found"}), 404

    # Création de la réponse avec les données de l'utilisateur
    user_profile = {
        "username": user_data["username"],
        "email": user_data["email"],
    }
    return jsonify(user_profile), 200

@app.route('/counter', methods=['GET', 'POST'])
@login_required
def counter():

    user_id = current_user.id

    # Trouver et mettre à jour le document en utilisant le UUID directement
    result = mongo.db.users.find_one_and_update(
        {"_id": user_id},
        {"$inc": {"counter": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    # Convertir le _id en string si nécessaire
    if "_id" in result:
        result["_id"] = str(result["_id"])

    return jsonify({
        "total_document": result,
        "routes_Counter": 200
    })

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({
        "message": f"Welcome {current_user.username}",
        "email": current_user.email,
    }
    )
@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    #On commence par récupérer l'user connecté à l'instanté
    user_id = current_user.id
    # on récupère le contenant du formulaire
    test_post = request.form.get("Post_Test")
    print(f"Test Post Value: {test_post}")
    #Maintenant, je teste si le champ est vide
    if test_post == '':
        return render_template('dashboard.html')

    result = mongo.db.users.find_one_and_update(
        {"_id": user_id},  # critère de recherche
        {"$push": {"question": test_post}},  # opération de mise à jour
        return_document=True
    )

    return jsonify({
        "status_code": 200,
        "message":"success"
    })

if __name__ == '__main__':
    app.run(debug=True)
