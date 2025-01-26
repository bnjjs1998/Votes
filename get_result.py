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
@app.route('/get_result', methods=['GET'])
@login_required
def get_result():
    get_archive = mongo.db.scrutin_archive.find()
    archive_list = list(get_archive)
    # Convertir les ObjectId en chaînes de caractères pour JSON
    for item in archive_list:
        item['_id'] = str(item['_id'])
    print(archive_list)
    return jsonify(
        {"data": archive_list},
        {'success': 'true'},
        {'username': current_user.username}
    )
