from codecs import replace_errors

from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo

#retourner un élément aléatoire


@app.route('/the_quest')
@login_required
def the_quest():
    return  render_template('the_question.html')


@app.route('/get_questions', methods=['GET'])
def get_questions():
    questions = mongo.db.questions.find()  # Récupère toutes les questions de la collection
    print(questions)

    # Créer une liste sans les _id
    questions_data = []
    for question in questions:
        question_data = question.copy()  # Créer une copie de la question
        question_data.pop('_id', None)  # Supprime la clé '_id'
        questions_data.append(question_data)

    return jsonify(questions_data)  # Retourne la liste des questions sans l'_id


@app.route('/my_questions', methods=['GET'])
@login_required
def my_sondage():
    user_questions = mongo.db.users.find_one(
        {'_id': current_user.id},
        {'Mes sondages': 1}
    )


    if user_questions is None or 'Mes sondages' not in user_questions:
        return jsonify({
            "message":"vous devez poster au moin un sondage"
        })

    return jsonify({
        "messages":"success",
        "my_questions": user_questions['Mes sondages']
    })
