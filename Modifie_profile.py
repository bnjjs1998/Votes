from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo

#je crée la route qui va permettre de modifier le profile
@app.route('/modifie_profile')
@login_required
def modifie_profile():
    return render_template('modifie_profile.html')

@app.route('/Get_modifie_profile', methods=['POST', 'GET'])
@login_required
def modify_profile():
    if request.method == 'GET':
        user_id = current_user.id
        user_data = mongo.db.users.find_one({"_id": user_id})

        if not user_data:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "username": user_data.get('username'),
            "email": user_data.get('email'),
        })

    elif request.method == 'POST':
        data = request.get_json()
        new_email = data.get('email')

        if not new_email:
            return jsonify({"error": "Email is required"}), 400
        #test
        user_id = current_user.id
        result = mongo.db.users.update_one(
            {"_id": user_id},
            {"$set": {"email": new_email}}
        )

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "success"})

@app.route('/remove_profile', methods=['POST', 'GET'])
@login_required
def delete_profile():
    try:
        # Debug info
        print("Début de la suppression du profil.")

        # Récupérer l'ID de l'utilisateur (au format string UUID)
        user_id = str(current_user.id)  # Pas de conversion en ObjectId ici

        # Trouver le document correspondant dans la collection `users`
        session = mongo.db.users.find_one({"_id": user_id})
        if not session:
            return jsonify({"error": "User not found"}), 404
        else:
            print("La session a été trouvée pour l'utilisateur.")

            # Clés à conserver
            keys_to_keep = {"_id", "username", "mes_sondages"}

            # Identifier les clés à supprimer dynamiquement
            keys_to_unset = {key: "" for key in session.keys() if key not in keys_to_keep}

            # Supprimer les clés non désirées
            mongo.db.users.update_one(
                {"_id": user_id},  # Filtrer par l'utilisateur
                {"$unset": keys_to_unset}  # Supprimer les clés non désirées
            )

        return jsonify({"message": "Profile successfully cleaned and updated"}), 200

    except Exception as e:
        print(f"Erreur pendant la suppression : {e}")
        return jsonify({"error": "An error occurred"}), 500

