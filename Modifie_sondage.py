from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo

# Créer une route pour récup la data du frontend
@app.route('/Change_Choice', methods=['GET', 'POST'])
@login_required
def change_sondage():
    data = request.get_json()
    print(data)
    return jsonify({
        "success": True,
    })

@app.route('/update_sondage_title', methods=['GET', 'POST'])
@login_required
def update_sondage_title():
    data = request.get_json()
    print(data)
    return jsonify({
        "success": True,
    })

