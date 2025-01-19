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
    # Afficher les données reçues pour déboguer
    print(f"Data received for Block result: {data}")

    return jsonify({
        "success": True,
        "message": "Le sondage a été bloqué avec succès."
    })
