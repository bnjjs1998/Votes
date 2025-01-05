from flask import request, jsonify
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

        # Construire les données du sondage
        Sondages = {
            'title': Title_quest,
            'questions': [{
                'choices': questions
            }]
        }
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

