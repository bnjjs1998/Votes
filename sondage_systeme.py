from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import current_user
from flask_login import login_required

from app import *
from app import app
from app import mongo
from systeme_log import *

@app.route('/Post_sondage', methods=['POST'])
@login_required
def post_sondage():
    # je récupère les datas du formulaire
    title = request.form['quest_title']
    choices = request.form.getlist('questions[0][choices][]')
    print(f"Titre du sondage: {title}")
    print(f"Choix de réponses: {choices}")

    #Une fois récupère, je crée un jeu de donnée pour préparer la requete
    sondage_data = {
        "title_question": title,
        "choices": choices,
        "Créateur" : current_user.username,
    }
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
    # Récupérer les données envoyées via POST
    choice_1 = request.form.get('choice_1_Input')
    choice_2 = request.form.get('choice_2_Input')
    choice_3 = request.form.get('choice_3_Input')
    print(choice_1, choice_2, choice_3)
    # Vérifier que les valeurs ne sont pas nulles
    if not choice_1 or not choice_2 or not choice_3:
        return jsonify({
            "status_code": 400,
            "message": "Tous les choix doivent être remplis."
        })
    if choice_1 == choice_2 and choice_3 == choice_2:
        print("Un des votes est identique ça ne convient pas")
        return jsonify({
            "status_code": 500,
        })

    # Retourner les choix sous forme de JSON
    return jsonify({
        "status_code": 200,
        "choice_1": choice_1,
        "choice_2": choice_2,
        "choice_3": choice_3
    })
