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
    data = request.get_json()
    print('donnée reçue :', data)

    #Vérifier que data contient quelque choses
    if not data:
        return jsonify({
            "status_code": 400,
            "message": "Aucune donnée reçue."
        })


    return jsonify({
        "status_code": 200,
        "message": "Les réponses ont été reçues.",
        "choices": data
    })
