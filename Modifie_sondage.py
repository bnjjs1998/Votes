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
def change_state_btn():
    # Récupérer les données envoyées par le client
    data = request.get_json()
    title_quest = data.get('question_title')
    state = data.get('privacy')

    print(f"Données reçues : {data}")
    print(f"État demandé : {state}")

    # Vérifier que le champ 'title_question' est présent
    if not title_quest:
        return jsonify({
            "status": 400,
            "message": "Le champ 'question_title' est requis."
        }), 400

    # Gestion des états 'private' et 'public'
    if state == "private":
        print(f"Le sondage '{title_quest}' est passé en privé.")
        # Supprimer le document correspondant
        delete_result = mongo.db.questions.delete_one({"title_question": title_quest})

        if delete_result.deleted_count > 0:
            print(f"Le sondage '{title_quest}' a été supprimé avec succès.")
        else:
            print(f"Aucun sondage trouvé avec le titre '{title_quest}'. Rien à supprimer.")

    elif state == "public":
        print(f"Le sondage '{title_quest}' est passé en public.")
        # Vérifier si le document existe déjà
        existing_question = mongo.db.questions.find_one({"title_question": title_quest})

        if existing_question:
            print(f"Le sondage '{title_quest}' existe déjà. Mise à jour de l'état.")
            mongo.db.questions.update_one(
                {"title_question": title_quest},
                {"$set": {"privacy": "public"}}
            )
        else:
            print(f"Le sondage '{title_quest}' n'existe pas. Création du document.")
            mongo.db.questions.insert_one({
                "title_question": title_quest,
                "choices": data.get("choices", []),
                "privacy": "public"
            })

    else:
        print("État inconnu. Aucune action effectuée.")
        return jsonify({
            "status": 400,
            "message": "L'état spécifié est inconnu."
        }), 400

    return jsonify({
        "status": 200,
        "message": f"L'état du sondage '{title_quest}' a été modifié avec succès."
    }), 200
