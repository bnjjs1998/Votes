from datetime import datetime

from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user

@app.route('/update_title', methods=['POST'])
@login_required
def update_title():
    data = request.get_json()
    data_title = data.get('title')
    print(data)


    #Je vérifie que la question n'est pas en public
    result_in_question = mongo.db.questions.find_one({'title': data_title})
    if result_in_question:
        return jsonify({
            "message": "la question est en public les infos ne peuvent pas etre modifié"
        })



    return jsonify({
        "success": data
    })


@app.route('/update_choices', methods=['POST'])
@login_required
def update_choice():
    data = request.get_json()
    data_title = data.get('Title')
    data_choices = data['updatedChoices']
    data_choices_new = data.get
    print(data_choices)
    # Extraire toutes les `newValue`
    new_values = [choice.get('newValue') for choice in data_choices]
    print(new_values)

    # Je vérifie que la question n'est pas en public
    result_in_question = mongo.db.questions.find_one({'title': data_title})
    if result_in_question:
        return jsonify({
            "message": "la question est en public les infos ne peuvent pas etre modifié"
        })

    return jsonify({
        "hello": data
    })



@app.route('/delete', methods=['POST'])
@login_required
def delete():
    data = request.get_json()

    data_title = data.get("Titre")
    print(data_title)
    print(data)
    return jsonify({
        'success': True
    })



@app.route('/Change_state_btn', methods=['POST'])
def change_state_btn():

    # Récupérer les données envoyées par le client
    data = request.get_json()
    title_quest = data.get('Titre')
    print(data)




    return jsonify({
        "status": 200,
        "message": f"L'état du sondage '{title_quest}' a été modifié avec succès."
    }), 200
