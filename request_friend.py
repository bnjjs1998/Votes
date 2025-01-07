from codecs import replace_errors

from flask import request, jsonify
from flask_login import login_required
from app import *
from app import app
from app import mongo


collections_user ="Users"

@app.route('/get_allprofile', methods=['GET', 'POST'])
def get_allprofile():
    allprofile_request = mongo.db.collections[collections_user].find()
    return jsonify({
        "status": "success",
    }),