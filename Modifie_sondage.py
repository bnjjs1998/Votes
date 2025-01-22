from datetime import datetime

from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user
#
@app.route('/update_title', methods=['POST'])
@login_required
def update_title():
    data = request.get_json()
    old_title = data.get('old_Titre')
    new_title = data.get('new_Titre')
    user_id = current_user.id  # Récupération de l'ID utilisateur connecté

    # Validation des entrées
    if not user_id:
        return jsonify({
            "error": "Vous devez être connecté pour mettre à jour un titre."
        }), 401

    if not old_title or not new_title:
        return jsonify({
            "success": False,
            "error": "Les titres (ancien et nouveau) sont requis."
        }), 400

    # Vérification si l'ancien titre existe et n'est pas public
    public_question = mongo.db.questions.find_one({'title': old_title})
    if public_question:
        return jsonify({
            "success": False,
            "error": "La question est en public, elle ne peut pas être modifiée."
        }), 410

    # Mise à jour dans la collection `users`
    result = mongo.db.users.update_one(
        {
            '_id': user_id,
            'Mes sondages.title_question': old_title     # Filtre par titre dans `Mes sondages`
        },
        {
            '$set': {'Mes sondages.$.title_question': new_title}  # Mettre à jour le titre spécifique
        }
    )

    # Vérification si la mise à jour a eu lieu
    if result.matched_count == 0:
        return jsonify({
            "success": False,
            "error": "Le titre à mettre à jour n'a pas été trouvé."
        }), 404

    return jsonify({
        "success": True,
        "message": f"Le titre '{old_title}' a été mis à jour avec succès.",
        "old_title": old_title,
        "new_title": new_title
    }), 200


@app.route('/update_choices', methods=['POST'])
@login_required
def update_choice():
    try:
        # Récupérer les données JSON
        data = request.get_json()
        print("Données reçues :", data)

        data_title = data.get('Titre')
        choices = data.get('choices', [])
        user_id = current_user.id  # UUID, pas ObjectId

        if not user_id:
            return jsonify({"success": False, "error": "L'utilisateur n'est pas connecté."}), 401

        if not data_title:
            return jsonify({"success": False, "error": "Le titre est requis."}), 400

        if not choices:
            return jsonify({"success": False, "error": "Les choix sont requis."}), 400

        # Extraire les nouveaux choix
        new_values = [choice['newValue'] for choice in choices if 'newValue' in choice]
        print("Nouveaux choix extraits :", new_values)

        if not new_values:
            return jsonify({
                "success": False,
                "error": "Aucun choix valide trouvé."
            }), 400

        # Mise à jour MongoDB
        result = mongo.db.users.update_one(
            {
                '_id': user_id,  # Utiliser directement l'UUID
                'Mes sondages.title_question': data_title
            },
            {
                '$set': {'Mes sondages.$.choices': new_values}
            }
        )

        if result.matched_count == 0:
            return jsonify({
                "success": False,
                "error": "Sondage introuvable pour cet utilisateur."
            }), 404

        return jsonify({
            "success": True,
            "message": f"Les choix pour le sondage '{data_title}' ont été mis à jour avec succès.",
            "new_values": new_values
        }), 200

    except Exception as e:
        print("Erreur inattendue :", str(e))
        return jsonify({"success": False, "error": "Une erreur interne s'est produite."}), 500

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    data = request.get_json()
    data_title = data.get("Titre")
    print(data_title)
    print(data)
    return jsonify({
        'success': True
    })



@app.route('/Change_state_btn', methods=['POST'])
def change_state_btn():

    # Récupérer les données envoyées par le client
    data = request.get_json()
    title_quest = data.get('Titre')
    print(data)




    return jsonify({
        "status": 200,
        "message": f"L'état du sondage '{title_quest}' a été modifié avec succès."
    }), 200
