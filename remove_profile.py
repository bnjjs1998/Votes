from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo


@app.route('/remove_profile', methods=['GET', 'POST'])
@login_required
def remove_profile():
    return jsonify({
        "msg": "success",
    })

