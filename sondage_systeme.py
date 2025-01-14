from flask import request, jsonify
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
    try:
        data = request.get_json()
        print('Donnée reçue:', data)
        title_question = data.get('title_question')
        print(f"Titre de la question : {title_question}")

        # Vérifier si 'choices' est bien présent
        choices_data = data.get('choices', {})
        print(f"Choix reçus : {choices_data}")

        for choice in choices_data:
            print(f"Choix : {choice}")

        return jsonify({
            "status_code": 200,
            "message": "Réponses reçues et traitées",
            "choices": choices_data
        })

    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({
            "status_code": 500,
            "message": f"Erreur lors du traitement des votes: {e}"
        }), 500
