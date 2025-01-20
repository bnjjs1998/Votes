from datetime import datetime
from flask import render_template, jsonify, request
from flask_login import UserMixin, login_required, current_user
from app import *
from app import app
from app import mongo
from request_friend import collections_user




@app.route('/B_btn', methods=['POST'])
@login_required
def block_btn():
    data = request.get_json()

    # Afficher les données reçues pour débogage
    print(f"Data received for Block result: {data}")

    # Validation des données
    title = data.get('question_title')

    try:
        # Vérifier si la question existe
        question = mongo.db.questions.find_one({'title_question': title})
        question_id = question['_id']
        print(f"Question ID : {question_id}")

        # Changer le statut de la question
        mongo.db.questions.update_one(
            {'_id': question_id},
            {'$set': {'status': 'blocked'}}
        )
        # Vérifier si le statut a été mis à jour
        updated_question = mongo.db.questions.find_one({'_id': question_id})
        if updated_question.get('status') == 'blocked':
            print("Mise à jour réussie : le statut est maintenant 'blocked'.")
            result_filtre = list(mongo.db.questions.aggregate([
                {'$match': {'_id': question_id}},  # Correctement fermé
                {'$merge': {'into': 'scrutin_archive'}}  # Supprimé l'espace dans le nom
            ]))
            # Vérifié que le document est bien archivé
            document_block = mongo.db.scrutin_archive.find_one({'_id': question_id})
            if document_block:
                print('Le document à bien été archivé')
                # On peut suprimer le document de question
                result_delete = mongo.db.questions.delete_one({'_id': question_id})
                if result_delete:
                    print('Le document à bien été supprimé de la collection question')
                    #On fait la requête
                    delete_result = mongo.db.questions.delete_one({'_id': question_id})
                    if delete_result:
                        print('La question à bien été transféré aux archives')

    except Exception as e:
        print(f"Erreur lors de l'accès à MongoDB : {e}")
        return jsonify({
            "success": False,
            "message": "Une erreur interne est survenue."
        }), 500

    # Retourner une réponse en cas de succès
    return jsonify({
        "success": True,
        "message": f"Le sondage '{title}' a été bloqué avec succès."
    })
