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

@app.route('/Post_vote', methods=['POST', 'GET'])
@login_required
def post_vote():
    # Récupérer les données envoyées par le frontend
    data = request.get_json()
    print('Donnée reçue:', data)

    # Vérification des champs obligatoires
    title_question = data.get('question_title')
    choices_data = data.get('choices')

    if not title_question or not choices_data:
        return jsonify({
            "status": 400,
            "message": "Les champs 'question_title' et 'choices' sont requis."
        }), 400

    # Vérifier si la question existe déjà dans la collection 'questions'
    existing_question = mongo.db.questions.find_one({"question_title": title_question})

    if not existing_question:
        return jsonify({
            "status": 404,
            "message": f"Le sondage avec le titre '{title_question}' est introuvable."
        }), 404

    document_id = existing_question["_id"]
    print(f"Le sondage '{title_question}' trouvé. ID : {document_id}")

    # Initialisation de la logique de Condorcet : Comparaison par paires
    options = list(choices_data.keys())
    pairwise_results = {option: {opponent: 0 for opponent in options if opponent != option} for option in options}

    for option, rank in choices_data.items():
        for opponent, opponent_rank in choices_data.items():
            if option != opponent:
                if rank < opponent_rank:
                    pairwise_results[option][opponent] += 1
                elif rank > opponent_rank:
                    pairwise_results[opponent][option] += 1

    print("Résultats par paires :", pairwise_results)

    # Calcul des scores finaux selon Condorcet
    final_scores = {option: 0 for option in options}
    for option, opponents in pairwise_results.items():
        for opponent, score in opponents.items():
            if score > pairwise_results[opponent][option]:
                final_scores[option] += 1

    print("Scores finaux selon Condorcet :", final_scores)

    # Mettre à jour le document dans la collection 'questions'
    update_result = mongo.db.questions.update_one(
        {"_id": document_id},
        {
            "$set": {
                "Condorcet_Scores": final_scores  # Enregistre les scores calculés
            },
            "$push": {
                "votes": {
                    "user_id": current_user.username,  # Identifiant de l'utilisateur
                    "choices": choices_data           # Les choix de cet utilisateur
                }
            }
        }
    )


    # Réponse en cas de succès
    return jsonify({
        "status": 200,
        "message": "Les votes ont été traités et intégrés avec succès.",
        "Condorcet_Scores": final_scores
    }), 200
from bson import ObjectId

@app.route('/Vote', methods=['POST'])
@login_required  # Retirez temporairement pour tester
def vote():
    try:
        # Données brutes pour débogage
        print("Données brutes reçues :", request.data)

        # Parse les données JSON
        data = request.get_json()
        print("Données reçues :", data)

        # Vérifiez que les champs nécessaires sont présents
        question_title = data.get('question_title')
        choices = data.get('choices')

        if not question_title or not choices:
            return jsonify({"status": 400, "message": "Le titre de la question et les choix sont requis."}), 400

        # Comparer avec la collection `questions` pour vérifier si la question existe
        question = mongo.db.questions.find_one({"title_question": question_title})

        if not question:
            return jsonify({"status": 404, "message": "La question spécifiée n'existe pas."}), 404

        question_id = question["_id"]  # Obtenir l'ID de la question
        print(f"ID de la question trouvée : {question_id}")

        # Logique Condorcet : Comparaison par paires
        options = list(choices.keys())
        pairwise_results = {
            option: {opponent: 0 for opponent in options if opponent != option}
            for option in options
        }

        # Comparaison des paires
        for option, rank in choices.items():
            for opponent, opponent_rank in choices.items():
                if option != opponent:
                    if rank < opponent_rank:
                        pairwise_results[option][opponent] += 1
                    elif rank > opponent_rank:
                        pairwise_results[opponent][option] += 1

        print("Résultats par paires :", pairwise_results)

        # Calcul des scores finaux selon Condorcet
        final_scores = {option: 0 for option in options}
        for option, opponents in pairwise_results.items():
            for opponent, score in opponents.items():
                if score > pairwise_results[opponent][option]:
                    final_scores[option] += 1

        print("Scores finaux selon Condorcet :", final_scores)

        # Mise à jour du document avec les résultats Condorcet
        updated_question = mongo.db.questions.find_one_and_update(
            {"_id": question_id},  # Filtre basé sur l'ID
            {
                "$set": {
                    "choices": choices,              # Met à jour les choix
                    "Condorcet_Scores": final_scores  # Ajoute les scores Condorcet
                }
            },
            return_document=True  # Retourne le document mis à jour
        )

        # Convertir _id en chaîne pour le retour JSON
        if updated_question:
            updated_question["_id"] = str(updated_question["_id"])

        # Afficher la question mise à jour pour débogage
        print("Question mise à jour :", updated_question)

        # Retourner une réponse avec les scores calculés
        return jsonify({
            "status": 200,
            "message": "Vote traité avec succès.",
            "Condorcet_Scores": final_scores,
            "Updated_Question": updated_question  # Retourne la question mise à jour pour validation
        }), 200

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({"status": 500, "message": "Erreur interne", "details": str(e)}), 500
