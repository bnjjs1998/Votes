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
    # on initialise la date d'expiration
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


    #jeux de donnée pour la session de l'utilisateur
    my_sondage_data = {
        "title_question": title,
        "choices": choices,
        "expiration_date": expiration_date,
        "state":"Privé"
    }

    #insertions du jeu de donnée dans la collection users
    result_in_users = mongo.db.users.update_one(
        {"_id": current_user.id},
        {"$push": {"Mes sondages": my_sondage_data}}
    )

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
    if not request.is_json:
        print("data is not json", request.data)
        return jsonify({"status": 415, "message": "Le contenu doit être au format JSON"}), 415

    try:
        # Récupération des données JSON
        data = request.get_json()
        print("Données reçues :", data)

        # Vérifications initiales
        if not data:
            return jsonify({"status": 400, "message": "Aucune donnée reçue"}), 400
        if "title_question" not in data or "choices" not in data:
            return jsonify({"status": 400, "message": "Données incomplètes : 'title_question' ou 'choices' manquant"}), 400

        # Récupération de la question dans la base
        question_title = data["title_question"]
        question = mongo.db.questions.find_one({"title_question": question_title})
        if not question:
            return jsonify({"status": 404, "message": "Question introuvable"}), 404

        # Vérifier la date d'expiration
        expiration_date = question.get("expiration_date")
        if expiration_date:
            # Si expiration_date est déjà un objet datetime, l'utiliser directement
            if isinstance(expiration_date, datetime):
                expiration_date_obj = expiration_date
            else:
                # Sinon, convertir en datetime
                expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%dT%H:%M:%S.%f+00:00')

            # Vérifier si la date d'expiration est dépassée
            if datetime.now() > expiration_date_obj:
                return jsonify({"status": 400, "message": "La période de vote est expirée"}), 410

        # Logique Condorcet (inchangée)
        choices = data["choices"]
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

        # Mise à jour des scores Condorcet dans la base
        mongo.db.questions.update_one(
            {"_id": question["_id"]},
            {"$set": {"Condorcet_Scores": final_scores}}
        )

        return jsonify({
            "status": 200,
            "message": "Vote enregistré avec succès",
            "scores": final_scores
        }), 200

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({"status": 500, "message": "Erreur interne", "details": str(e)}), 500



@app.route('/role')
@login_required
def role():
    data_quest = mongo.db.users.find_one(
        {"_id": current_user.id},
        {"role": 1}
    )
    if data_quest:
        return jsonify({
            "status": 200,
        })
    else:
        return jsonify({
            "status": 404,
        })