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
@app.route('/sondage', methods=['POST'])
@login_required
def test():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        survey_title = request.form.get('surveyTitle')
        questions = request.form.getlist('questions[0][choices][]')

        # Verifier les données
        if not survey_title or not questions:
            return jsonify({"status_code": 400, "message": "Le titre et les choix sont requis."})

        # Construire les données du sondage
        Sondages = {
            'title': survey_title,
            'questions': [{
                'choices': questions
            }]
        }

        # Insérer le sondage dans la collection 'surveys'
        result = mongo.db.surveys.insert_one(Sondages)

        # Ajouter le sondage complet dans le document de l'utilisateur
        Sondages['_id'] = str(result.inserted_id)  # Convertir l'ObjectId en chaîne

        # j'insère dans la liste Sondage
        mongo.db.users.find_one_and_update(
            {"_id": current_user.id},
            {"$push": {"sondage": Sondages}}
        )
        return jsonify({
            "status_code": 200,
            "message": "Sondage ajouté avec succès",
            "Sondages": Sondages
        })



if __name__ == '__main__':
    app.run(debug=True)
