from datetime import datetime

from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user


@app.route('/update_choices', methods=['POST'])
@login_required
def update_choices():
    # Récupération des données envoyées par le frontend
    data = request.get_json()
    sondage_id = data.get('sondage_id')
    new_choices = data.get('new_choices')

    # Log des données reçues
    print(f"Reçu - sondage_id: {sondage_id}, new_choices: {new_choices}")

    # Simuler la mise à jour des choix dans la base de données (ou autre traitement)
    # Par exemple, si la mise à jour réussit, vous renvoyez les nouveaux choix :

    return jsonify({
        "succes": True,
        "updated_choices": new_choices  # Vous renvoyez les choix mis à jour
    })



@app.route('/update_title', methods=['POST'])
@login_required
def update_title():
    # Récupération des données envoyées par le frontend
    data = request.get_json()
    print(f"Données reçues pour la mise à jour du titre: {data}")  # Ajout d'un log pour afficher les données reçues

    new_title = data.get('new_title')
    print(f"Nouveau titre reçu: {new_title}")  # Vérifiez le nouveau titre reçu
    return jsonify({
        "success": True
    })


@app.route('/Delete_btn', methods=['POST'])
@login_required
def delete_btn():
    data = request.get_json()

    # Afficher les données reçues pour déboguer
    print(f"Data received for delete: {data}")



    return jsonify({
        "success": True
    })

@app.route('/Change_state_btn', methods=['POST'])
@login_required
def change_state_btn():
    # Récupérer les données envoyées par le frontend
    data = request.get_json()
    is_private = data.get('isPrivate')  # État (privé/public)
    question_title = data.get('question_title')
    choices = data.get('choices')
    Creator = current_user.username

    print(f"Titre: {question_title}, État: {'Privé' if is_private else 'Public'}, Choix: {choices}")

    # Accéder à la collection "questions" de la base de données par défaut
    questions_collection = mongo.db.questions
    users_collections = mongo.db.users


    if is_private:
        print('Le contenu est privé')


    else:
        print('Le contenu est public')

        # Mise à jour pour rendre la question publique dans la collection 'questions'
        result_private = questions_collection.find_one_and_update(
            {"Title Question": question_title},
            {
                "$set": {
                    "Stat": is_private,  # Mise à jour de l'état (privé ou public)
                    "Title Question": question_title,
                    "Choix": choices,
                    "Create_by": Creator,
                    "privacy": "public"  # Ajout de la clé 'privacy' pour indiquer le statut
                }
            },
            upsert=True,  # Insérer si le document n'existe pas
            return_document=True  # Retourne le document mis à jour ou inséré
        )
        print(f"Résultat de la mise à jour dans questions: {result_private}")

        # Mise à jour du tableau 'Mes sondages' dans la collection 'users' pour inclure 'privacy' et 'Stat'
        result_update_users = users_collections.update_many(
            {"_id": current_user.id, "Mes sondages.title_question": question_title},
            {
                "$set": {
                    "Mes sondages.$.privacy": "public",  # Mettre à jour le champ 'privacy' dans 'Mes sondages'
                    "Mes sondages.$.Stat": is_private  # Ajout de la clé 'Stat' dans mes_sondages
                }
            }
        )
        print(f"Documents affectés dans users (mise à jour): {result_update_users.modified_count}")

    # Retourner une réponse JSON
    return jsonify({
        'success': True,
        'new_state': 'Privé' if is_private else 'Public'
    })
