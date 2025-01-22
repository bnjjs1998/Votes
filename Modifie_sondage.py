from datetime import datetime

from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user

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
    data = request.get_json()
    data_title = data.get('Title')
    data_choices = data['updatedChoices']
    data_choices_new = data.get
    print(data_choices)
    # Extraire toutes les `newValue`
    new_values = [choice.get('newValue') for choice in data_choices]
    print(new_values)

    # Je vérifie que la question n'est pas en public
    result_in_question = mongo.db.questions.find_one({'title': data_title})
    if result_in_question:
        return jsonify({
            "message": "la question est en public les infos ne peuvent pas etre modifié"
        })

    return jsonify({
        "hello": data
    })



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
