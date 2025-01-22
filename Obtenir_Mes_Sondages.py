from flask import request, jsonify
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo
from systeme_log import *

#charger le template html
@app.route('/template_my_questions', methods=['GET'])
@login_required
def template_my_questions():
    return render_template('my_questions.html')


@app.route('/get_sondage_current_id', methods=['GET'])
@login_required
def get_sondage():
    try:
        # Récupérer tous les titres de la collection `scrutin_archive`
        archived_titles = [doc["title_question"] for doc in mongo.db.scrutin_archive.find({}, {"title_question": 1})]

        # Récupérer les sondages de l'utilisateur
        data_quest = mongo.db.users.find_one(
            {"_id": current_user.id},
            {"Mes sondages": 1}
        )

        if not data_quest or "Mes sondages" not in data_quest:
            return jsonify({
                "status_code": 404,
                "message": "Utilisateur ou sondages non trouvés."
            }), 404

        # Vérifier si un titre correspond
        sondage = data_quest.get("Mes sondages", [])
        for item in sondage:
            if item.get("title_question") in archived_titles:
                print(item.get("title_question"))


                # Supprimer l'objet entier correspondant
                mongo.db.users.update_one(
                    {"_id": current_user.id},
                    {"$pull": {"Mes sondages": {"title_question": item.get("title_question")}}}
                )

        return jsonify({
            "status_code": 200,
            "Sondage": sondage
        }), 200

    except Exception as e:
        print(f"Erreur lors de la récupération des sondages : {e}")
        return jsonify({
            "status_code": 500,
            "message": "Une erreur interne est survenue."
        }), 500