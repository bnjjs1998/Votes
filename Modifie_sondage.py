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

from flask import jsonify, request
from flask_login import login_required, current_user
from bson import ObjectId

@app.route('/delete', methods=['POST'])
@login_required
def delete():
    try:
        # Récupérer les données de la requête
        data = request.get_json()
        data_title = data.get("Titre")
        user_id = current_user.id

        if not data_title:
            return jsonify({"success": False, "error": "Titre requis."}), 400

        # Suppression d'un sondage dans `Mes sondages`
        result = mongo.db.users.find_one_and_update(
            {
                "_id": user_id  # Rechercher l'utilisateur par ID
            },
            {
                "$pull": {
                    "Mes sondages": {"title_question": data_title}  # Supprimer le sondage par titre
                }
            },
            return_document=True  # Retourner le document après mise à jour
        )

        if not result:
            return jsonify({
                "success": False,
                "error": "Utilisateur ou sondage introuvable."
            }), 404





        return jsonify({
            "success": True,
            "message": f"Le sondage '{data_title}' a été supprimé avec succès.",
            "updated_user": result
        }), 200

    except Exception as e:
        print("Erreur inattendue :", str(e))
        return jsonify({"success": False, "error": "Une erreur interne s'est produite."}), 500

@app.route('/Change_state_btn', methods=['POST'])
@login_required
def change_state_btn():
    user_id = current_user.id

    # Récupérer les données envoyées par le client
    data = request.get_json()
    title_quest = data.get('Titre')
    state = data.get('state')
    print("État reçu :", state)
    print("Données reçues :", data)

    # Requête pour trouver la question dans `Mes sondages`
    find_my_question = mongo.db.users.find_one(
        {
            "_id": user_id,
            "Mes sondages": {
                "$elemMatch": {
                    "title_question": title_quest
                }
            }
        },
        {
            "Mes sondages.$": 1  # Récupérer uniquement l'objet correspondant
        }
    )

    if find_my_question:
        # Récupérer l'objet à partir de la réponse
        my_question = find_my_question["Mes sondages"][0]

        # Mettre à jour la clé `state` dans `Mes sondages`
        update_my_question = mongo.db.users.update_one(
            {
                "_id": user_id,
                "Mes sondages.title_question": title_quest
            },
            {
                "$set": {"Mes sondages.$.state": state}
            }
        )

        if update_my_question.modified_count > 0:
            print(f"L'état du sondage '{title_quest}' a été mis à jour avec succès dans 'Mes sondages'.")

            # Ajouter ou mettre à jour dans la collection `questions`
            mongo.db.questions.find_one_and_update(
                {"title_question": title_quest},
                {
                    "$set": {
                        "title_question": my_question["title_question"],
                        "choices": my_question["choices"],  # Ajouter les choix
                        "expiration_date": my_question.get("expiration_date"),
                        "state": state
                    }
                },
                upsert=True  # Crée le document s'il n'existe pas
            )
            print(f"Le sondage '{title_quest}' a été transféré ou mis à jour dans la collection 'questions'.")

        if state == "Privé":
            # Supprimer la question de la collection `questions`
            mongo.db.questions.delete_one({"title_question": title_quest})
            print(f"Le sondage '{title_quest}' a été supprimé de la collection 'questions'.")
            return jsonify({
                "status": 200,
                "message": f"Le sondage '{title_quest}' a été marqué comme privé et supprimé de la collection 'questions'."
            }), 200

    # Ne pas supprimer de `Mes sondages`, garder l'objet en place
    return jsonify({
        "status": 200,
        "message": f"L'état du sondage '{title_quest}' a été modifié et transféré avec succès."
    }), 200
