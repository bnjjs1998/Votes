from flask import request, jsonify
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo
from systeme_log import *

# je vais commencer à mettre en place le systeme de compte
@app.route('/get_sondage_current_id', methods=['GET'])
@login_required
def get_sondage():
    # Ici, je prépare une requete qui va extraire toutes les questions que l'utilisateur connecté a posées

    data_quest = mongo.db.users.find_one(
        {"_id": current_user.id},
        {"Sondage": 1}
    )
    # je convertis l'ensemble des éléments obtenu en liste
    sondage = data_quest.get('Sondage', [])

    #je retourne les elements voulu
    return jsonify({
        "status_code": 200,
        "Sondage": sondage
    })

