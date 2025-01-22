from codecs import replace_errors
from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo

#retourner un élément aléatoire


@app.route('/get_all_questions', methods=['GET'])
@login_required
def get_all_questions():
    all_question = mongo.db.questions.find()

    questions = []
    for question in all_question:
        question_data = question.copy()
        question_data['_id'] = str(question['_id'])
        questions.append(question_data)

    return render_template('all_questions.html', questions=questions, user=current_user.username)

@app.route('/get_last_questions', methods=['GET'])
@login_required
def liste_sondage():
    all_question = mongo.db.questions.find().sort('creation_date', -1).limit(10)

    # Convertir les résultats MongoDB en liste de dictionnaires et ajouter l'ID de chaque question
    questions = []
    for question in all_question:
        question_data = question.copy()
        question_data['_id'] = str(question['_id'])
        questions.append(question_data)

    return jsonify(questions)  # Retourne la liste des questions sans l'_id


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
