from datetime import datetime
from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user


@app.route('/result')
@login_required
def result():
    return render_template('Result.html')

@app.route('/B_btn', methods=['POST'])
@login_required
def block_btn():
    data = request.get_json()

    # Afficher les données reçues pour débogage
    print(f"Data received for Block result: {data}")

    # Validation des données
    title = data.get('question_title')  # Utilisation de 'title_question' au lieu de 'question_title'


    try:
        # Requête pour vérifier que la question existe
        question = mongo.db.questions.find_one({'title_question': title})
        question_id = question['_id']
        print(f"Question ID : {question_id}")
        #Changer le status de la questions
        mongo.db.questions.update_one(
            {'_id': question_id},
            {'$set': {'status': 'blocked'}}  # Modifier le champ 'status' en 'blocked'
        )
        print(f"Le sondage avec ID {question_id} a été bloqué.")
        print(question)

        status = data.get('status')
        if status == 'blocked':
            print('ça a fonctionné')



    except Exception as e:
        print(f"Erreur lors de l'accès à MongoDB : {e}")
        return jsonify({
            "success": False,
            "message": "Une erreur interne est survenue."
        }), 500

    # Retourner une réponse en cas de succès
    return jsonify({
        "success": True,
        "message": "Le sondage a été bloqué avec succès."
    })
