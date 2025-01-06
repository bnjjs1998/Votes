from codecs import replace_errors

from flask import request, jsonify
from flask_login import login_required
from app import *
from app import app
from app import mongo

collection = ''

@app.route('/liste_sondage', methods=['GET'])
@login_required
def liste_sondage():





    return
