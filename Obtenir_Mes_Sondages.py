from flask import request, jsonify
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo
from systeme_log import *

#charger le template html
@app.route('/templte_my_questions', methods=['GET'])
@login_required
def template_my_questions():
    return render_template('my_quest.html')


@app.route('/get_sondage_current_id', methods=['GET'])
@login_required
def get_sondage():
    data_quest = mongo.db.users.find_one(
        {"_id": current_user.id},
        {"Mes sondages": 1}
    )
    print("Data from MongoDB:", data_quest)

    sondage = data_quest.get('Mes sondages', [])  # Utilisez "Mes sondages", pas "Sondage"

    print("Extracted Sondage:", sondage)

    return jsonify({
        "status_code": 200,
        "Sondage": sondage
    })
