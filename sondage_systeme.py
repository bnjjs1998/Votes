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
    try:
        username = current_user.username
        data = request.get_json()
        print('Donnée reçue:', data)
        title_question = data.get('title_question')
        print(f"Titre de la question : {title_question}")
        # Vérifier si 'choices' est bien présent
        choices_data = data.get('choices', {})
        print(f"Choix reçus : {choices_data}")
        #foutre une requete push mongo
        _id_question = data.get('_id')
        print("voici l'id de la question à upgrade: ",_id_question)
        #la requete en dure
        result_in_question = mongo.db.questions.find_and_update_one(
            {"questions": _id_question},
            {"$push":{
                "classement": choices_data
            }}
        )
        #mise en place du systeme de vote
        for choice, classement in choices_data.items():
            counter_classement_1 = 0
            counter_classement_2 = 0
            counter_classement_3 = 0
            print(f"Choix : {choice}, classement : {classement}")
            if classement == 1:
                print("C'est votre choix numéros 1")
                counter_classement_1 = counter_classement_1 + 3
                print(counter_classement_1)
            if classement == 2:
                print("C'est votre choix numéros 2")
                counter_classement_2 = counter_classement_2 + 2
                print(counter_classement_2)
            if classement == 3:
                print("C'est votre choix numéros 2")
                counter_classement_3 = counter_classement_3 + 1
                print(counter_classement_3)
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
