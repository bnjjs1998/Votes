from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import current_user
from flask_login import login_required

from app import *
from app import app
from app import mongo
from systeme_log import *

@app.route('/sondage', methods=['POST'])
@login_required
def test():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        Title_quest = request.form.get('surveyTitle')
        questions = request.form.getlist('questions[0][choices][]')

        # Verifier les données
        if not Title_quest or not questions:
            return jsonify({"status_code": 400, "message": "Le titre et les choix sont requis."})

        date = datetime.datetime.now()
        # Construire les données du sondage
        Sondages = {
            'title': Title_quest,
            "Created_by": current_user.usernames,
            "Date": date.strftime("%d/%m/%Y"),
            'questions': [{
                'choices': questions
            }]
        }

        #Inserer la donnée dans Sondage
        mongo.db.Sondages.insert_one(Sondages)
        # j'insère dans la liste Sondage
        mongo.db.users.find_one_and_update(
            {"_id": current_user.id},
            {"$push": {"Sondage": Sondages}}
        )
        return jsonify({
            "status_code": 200,
            "message": "Sondage ajouté avec succès",
            "Sondages": Sondages
        })

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

    #ici je vais mettre la requete find and update vers ma database




    # Retourner les choix sous forme de JSON
    return jsonify({
        "status_code": 200,
        "choice_1": choice_1,
        "choice_2": choice_2,
        "choice_3": choice_3
    })
