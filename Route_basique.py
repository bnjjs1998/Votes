from flask import request, jsonify
from flask_login import login_required

from app import *
from app import app
from app import mongo

#les routes basiques une fois authentifier
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