from codecs import replace_errors
from flask import request, jsonify
from flask_login import login_required, current_user
from app import *
from app import app
from app import mongo

collections_user = "users"


@app.route('/get_allprofile', methods=['GET'])
@login_required
def get_allprofile():
    # Spécifier la projection avec exclusion de _id et inclusion de username
    if current_user.username == "testuser":
        allprofile_request = list(mongo.db[collections_user].find({}, {"_id": 0, "username": 1}))
        return jsonify({
            "status": "success",
            "users": allprofile_request
        }),200
    else:
        return jsonify({
            "status": "error",
            "message": "Vous avez pas les droits"
        })
