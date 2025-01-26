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
    try:
        # Récupérer les données envoyées par le frontend
        data = request.get_json()
        title = data.get('Titre')
        if not title:
            return jsonify({
                "success": False,
                "message": "Le titre de la question est requis."
            }), 400

        # Vérifier si la question existe dans la collection `questions`
        question = mongo.db.questions.find_one({'title_question': title})
        if not question:
            return jsonify({
                "success": False,
                "message": "La question spécifiée n'existe pas."
            }), 404

        question_id = question['_id']
        print(f"ID de la question trouvée : {question_id}")

        # Vérifier si la question est déjà archivée dans `scrutin_archive`
        archived_question = mongo.db.scrutin_archive.find_one({'_id': question_id})
        if archived_question:
            return jsonify({
                "success": True,
                "message": "Le sondage est déjà bloqué et archivé."
            }), 200

        # Mettre à jour le statut de la question comme "blocked"
        update_result = mongo.db.questions.update_one(
            {'_id': question_id},
            {'$set': {'status': 'blocked'}}
        )
        if update_result.modified_count == 0:
            return jsonify({
                "success": False,
                "message": "Impossible de bloquer la question."
            }), 400

        # Vérifier que le statut a bien été mis à jour
        updated_question = mongo.db.questions.find_one({'_id': question_id})
        if updated_question.get('status') != 'blocked':
            return jsonify({
                "success": False,
                "message": "La mise à jour du statut a échoué."
            }), 500

        print(f"Le statut de la question est maintenant 'blocked'.")

        # Archiver la question dans `scrutin_archive`
        mongo.db.scrutin_archive.insert_one(updated_question)
        print("La question a été archivée avec succès.")

        # Supprimer la question de la collection `questions`
        delete_result = mongo.db.questions.delete_one({'_id': question_id})
        if delete_result.deleted_count == 0:
            return jsonify({
                "success": False,
                "message": "La suppression de la question a échoué."
            }), 500

        print("La question a été supprimée de la collection 'questions'.")

        # Retourner une réponse en cas de succès
        return jsonify({
            "success": True,
            "message": f"Le sondage '{title}' a été bloqué, archivé et supprimé avec succès."
        }), 200

    except Exception as e:
        print(f"Erreur lors du traitement de la requête : {e}")
        return jsonify({
            "success": False,
            "message": "Une erreur interne est survenue."
        }), 500



