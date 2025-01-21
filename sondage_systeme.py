import time
from unittest import result
import time
from flask import request, jsonify
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo
from systeme_log import *
from bson.objectid import ObjectId
from datetime import datetime

@app.route('/Post_sondage', methods=['POST'])
@login_required
def post_sondage():
    # je récupère les datas du formulaire
    title = request.form['quest_title']
    choices = request.form.getlist('questions[0][choices][]')
    # on initalise la date d'expiration
    expiration_date_str = request.form.get('expiration_date')
    if not expiration_date_str:
        return jsonify({"status": 400, "error": "La date d'expiration est obligatoire."}), 400
    def parse_date(date_str):
        formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    expiration_date = parse_date(expiration_date_str)
    if not expiration_date:
        return jsonify({"status": 400, "error": "Format de la date d'expiration invalide."}), 400

    # Vérifier si la date d'expiration est dans le passé
    if expiration_date <= datetime.now():
        return jsonify({"status": 400, "error": "La date d'expiration doit être dans le futur."}), 400

    print(f"Titre du sondage: {title}")
    print(f"Choix de réponses: {choices}")
    print(f"Date d'expiration: {expiration_date}")

    #Une fois récupère, je crée un jeu de donnée pour préparer la requete sur la collection question global
    sondage_data = {
        "title_question": title,
        "choices": choices,
        "creator" : current_user.username,
        "expiration_date": expiration_date,
        "creation_date": datetime.now()
    }
    #jeux de donnée pour la session de l'utilisateur
    my_sondage_data = {
        "title_question": title,
        "choices": choices,
        "expiration_date": expiration_date
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
            "status": "success",
            "titre_question": title,
            "choices": choices,
            "expiration_date": expiration_date.strftime('%Y-%m-%d %H:%M:%S'),
            "message": "Sondage créé avec succès."
        }
    ), 200
@app.route('/Vote', methods=['POST'])
@login_required
def vote():
    try:
        # Récupération des données JSON
        data = request.get_json()
        print("Données reçues :", data)

        # Vérifications avec logs
        if not data:
            print("Erreur : aucune donnée reçue")
            return jsonify({"status": 400, "message": "Aucune donnée reçue"}), 400

        if "title_question" not in data:
            print("Erreur : 'title_question' manquant")
            return jsonify({"status": 400, "message": "'title_question' manquant"}), 400

        if "choices" not in data:
            print("Erreur : 'choices' manquant")
            return jsonify({"status": 400, "message": "'choices' manquant"}), 400

        if not isinstance(data["choices"], dict):
            print("Erreur : 'choices' n'est pas un dictionnaire")
            return jsonify({"status": 400, "message": "'choices' doit être un dictionnaire"}), 400

        # Traitement principal
        question_title = data["title_question"]
        choices = data["choices"]

        # Vérifiez l'utilisateur
        user_id = current_user.id
        user = mongo.db.users.find_one({"_id": user_id})

        # Vérifiez la question
        question = mongo.db.questions.find_one({"title_question": question_title})

        question_id = question["_id"]
        #i
        # Logique Condorcet (inchangée)
        pairwise_results = {
            option: {opponent: 0 for opponent in choices if opponent != option}
            for option in choices
        }
        for option, rank in choices.items():
            for opponent, opponent_rank in choices.items():
                if option != opponent:
                    if rank < opponent_rank:
                        pairwise_results[option][opponent] += 1
                    elif rank > opponent_rank:
                        pairwise_results[opponent][option] += 1

        final_scores = {option: 0 for option in choices}
        for option, opponents in pairwise_results.items():
            for opponent, score in opponents.items():
                if score > pairwise_results[opponent][option]:
                    final_scores[option] += 1

        # Mise à jour de la base de données
        mongo.db.questions.update_one(
            {"_id": question_id},
            {
                "$set": {
                    "Condorcet_Scores": final_scores
                }
            }
        )

        return jsonify({
            "status": 200,
            "message": "Vote enregistré avec succès",
            "scores": final_scores
        }), 200

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({
            "status": 500,
            "message": "Erreur interne",
            "details": str(e)
        }), 500
