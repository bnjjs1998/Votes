from unittest import result

from flask import request, jsonify
from flask_login import login_required
from app import *
from app import app
from app import mongo
from systeme_log import *
from bson.objectid import ObjectId

@app.route('/Post_sondage', methods=['POST'])
@login_required
def post_sondage():
    # je récupère les datas du formulaire
    title = request.form['quest_title']
    choices = request.form.getlist('questions[0][choices][]')
    print(f"Titre du sondage: {title}")
    print(f"Choix de réponses: {choices}")

    #Une fois récupère, je crée un jeu de donnée pour préparer la requete sur la collection question global
    sondage_data = {
        "title_question": title,
        "choices": choices,
        "Créateur" : current_user.username,
    }
    #jeux de donnée pour la session de l'utilisateur
    my_sondage_data = {
        "title_question": title,
        "choices": choices,
    }

    #insertions du jeu de donnée dans la collection users
    result_in_users = mongo.db.users.update_one(
        {"_id": current_user.id},
        {"$push": {"Mes sondages": my_sondage_data}}
    )

    #On va créer une collection question pour l'ensemble des questions
    result_in_question = mongo.db.questions.insert_one(sondage_data)
    return jsonify(
        {
            "test": "success",
            "titre_question": title,
            "choices": choices,
        }
    )


@app.route('/Post_vote', methods=['POST'])
@login_required
def post_vote():
    # Récupérer les données envoyées par le frontend
    data = request.get_json()
    print('Donnée reçue:', data)

    # Extraire et nettoyer les données
    _id_question = data.get('_id')
    title_question = data.get('title_question')
    choices_data = data.get('choices', {})
    print(f"ID question : {_id_question}, Choix reçus : {choices_data}")

    # Préparer l'objet à ajouter dans mes_classement
    classement = {
        "_id_question": _id_question,
        "title": title_question,
        "choices": choices_data,
    }

    # Vérifier si cette question a déjà été votée
    already_voted = mongo.db.users.find_one(
        {
            "_id": current_user.id,
            "mes_classement.title": title_question
        }
    )
    if already_voted:
        return jsonify(
            {
                "status": 400,
                "error": "La question a déjà été votée."
            }
        ), 400
    else:
        # Ajouter le classement dans "mes_classement" pour l'utilisateur
        mongo.db.users.find_one_and_update(
            {"_id": current_user.id},
            {"$push": {"mes_classement": classement}},
            return_document=True
        )

        # Initialisation des compteurs pour chaque rangnnn
        resultat_3 = 0
        resultat_2 = 0
        resultat_1 = 0

        # Structure des résultats des votes
        votes_result_data = {
            "_id": ObjectId(_id_question),
            "title_question": title_question,
            "result_votes": {}  # Initialisation de l'objet 'choices'
        }

        # Parcours de chaque choix et de son rang
        for clef, rank in choices_data.items():
            print('Les clefs sont:', clef)
            # Incrémentation des résultats
            if rank == 1:
                resultat_3 += 1
                votes_result_data["result_votes"][clef] = resultat_3
            elif rank == 2:
                resultat_2 += 2  # 2 points pour le rang 2
                votes_result_data["result_votes"][clef] = resultat_2
            elif rank == 3:
                resultat_1 += 3  # 3 points pour le rang 3
                votes_result_data["result_votes"][clef] = resultat_1

        # Mise à jour des résultats dans MongoDB pour la question
        mongo.db.questions.update_one(
            {"_id": ObjectId(_id_question)},  # Filtrage sur l'ID de la question
            {"$set": votes_result_data}  # Mise à jour des résultats de votes
        )

        return jsonify(
            {
                "status": 200,
                "message": "Vote enregistré avec succès."
            }
        ), 200




