from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
@app.route('/update_choices', methods=['POST'])
@login_required
def update_choices():
    # Récupération des données envoyées par le frontend
    data = request.get_json()
    sondage_id = data.get('sondage_id')
    new_choices = data.get('new_choices')

    # Log des données reçues
    print(f"Reçu - sondage_id: {sondage_id}, new_choices: {new_choices}")

    # Simuler la mise à jour des choix dans la base de données (ou autre traitement)
    # Par exemple, si la mise à jour réussit, vous renvoyez les nouveaux choix :

    return jsonify({
        "succes": True,
        "updated_choices": new_choices  # Vous renvoyez les choix mis à jour
    })



@app.route('/update_title', methods=['POST'])
@login_required
def update_title():
    # Récupération des données envoyées par le frontend
    data = request.get_json()
    print(f"Données reçues pour la mise à jour du titre: {data}")  # Ajout d'un log pour afficher les données reçues

    new_title = data.get('new_title')
    print(f"Nouveau titre reçu: {new_title}")  # Vérifiez le nouveau titre reçu
    return jsonify({
        "success": True
    })


@app.route('/Delete_btn', methods=['POST'])
@login_required
def delete_btn():
    data = request.get_json()

    # Afficher les données reçues pour déboguer
    print(f"Data received for delete: {data}")



    return jsonify({
        "success": True
    })

@app.route('/Block_btn', methods=['POST'])
@login_required
def block_btn():
    data = request.get_json()
    # Afficher les données reçues pour déboguer
    print(f"Data received for Block Vote: {data}")



    return jsonify({
        "success": True
    })

@app.route('/Change_state_btn', methods=['POST'])
@login_required
def change_state_btn():
    data = request.get_json()
    # Afficher les données reçues pour déboguer
    print(f"Data received for change state {data}")


    return jsonify({
        "success": True
    })







