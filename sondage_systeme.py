import time
from unittest import result
import time
from flask import request, jsonify
from flask_jwt_extended import current_user
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
@app.route('/Vote', methods=['POST'])
@login_required  # Retirez temporairement pour tester
def vote():
    try:
        # Données brutes pour débogage
        print("Données brutes reçues :", request.data)

        # Parse les données JSON
        data = request.get_json()
        print("Données reçues :", data)

        question_title = data.get('question_title')
        choices = data.get('choices')

        #je récupère l'id du user connecté
        user_id = current_user.id
        # Vérifiez si l'utilisateur existe
        user = mongo.db.users.find_one({"_id": user_id})
        print("Utilisateur trouvé :", user)

        # Vérifiez si la question existe
        question = mongo.db.questions.find_one({"title_question": question_title})

        question_id = question["_id"]
        print(f"ID de la question trouvée : {question_id}")

        # Mettre à jour les votes de l'utilisateur
        user_vote_entry = {
            "user_id": user_id,
            "username": user.get("username", "Anonyme"),
            "choices": choices
        }

        # Ajouter ou mettre à jour `user_votes`
        user_votes = question.get("user_votes", [])
        existing_vote = next((vote for vote in user_votes if vote["user_id"] == user_id), None)

        if existing_vote:
            existing_vote["choices"] = choices
        else:
            user_votes.append(user_vote_entry)

        # Logique Condorcet
        options = list(choices.keys())
        pairwise_results = {
            option: {opponent: 0 for opponent in options if opponent != option}
            for option in options
        }

        for option, rank in choices.items():
            for opponent, opponent_rank in choices.items():
                if option != opponent:
                    if rank < opponent_rank:
                        pairwise_results[option][opponent] += 1
                    elif rank > opponent_rank:
                        pairwise_results[opponent][option] += 1

        print("Résultats par paires :", pairwise_results)

        final_scores = {option: 0 for option in options}
        for option, opponents in pairwise_results.items():
            for opponent, score in opponents.items():
                if score > pairwise_results[opponent][option]:
                    final_scores[option] += 1

        print("Scores finaux selon Condorcet :", final_scores)

        # Mise à jour de la question
        updated_question = mongo.db.questions.find_one_and_update(
            {"_id": question_id},
            {
                "$set": {
                    "user_votes": user_votes,
                    "Condorcet_Scores": final_scores
                }
            },
            return_document=True
        )

        # Convertir les ObjectId en chaînes
        updated_question["_id"] = str(updated_question["_id"])

        # Mise à jour des préférences utilisateur
        user_classements = user.get("mes_classements", [])
        classement_entry = {
            "title": question_title,
            "choices": choices,
            "Condorcet_Scores": final_scores
        }

        existing_classement = next((c for c in user_classements if c["title"] == question_title), None)
        if existing_classement:
            existing_classement["choices"] = choices
            existing_classement["Condorcet_Scores"] = final_scores
        else:
            user_classements.append(classement_entry)

        mongo.db.users.update_one(
            {"_id": user_id},
            {"$set": {"mes_classements": user_classements}}
        )
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({
            "status": 500,
            "message": "Erreur interne",
            "details": str(e)
        }), 500
