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
    print(data)

    return jsonify({
        "hello": data
    })


@app.route('/update_choices', methods=['POST'])
@login_required
def update_choice():
    data = request.get_json()
    print(data)

    return jsonify({
        "hello": data
    })



@app.route('/delete')
@login_required
def delete():
    data = request.get_json()
    print(data)
    return jsonify({
        'success': True
    })



@app.route('/Change_state_btn', methods=['POST'])
def change_state_btn():

    # Récupérer les données envoyées par le client
    data = request.get_json()
    title_quest = data.get('question_title')
    state = data.get('privacy')


    # je vérifie la table archive si c'est le cas erreur
    document_block = mongo.db.scrutin_archive.find_one({'title_question': title_quest})
    if document_block:
        return jsonify({
            "error": "la question est deja dans les archive"
        })

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
                "choices_label": data.get("choices", []),
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
