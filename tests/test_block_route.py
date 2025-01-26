import unittest
from unittest.mock import MagicMock, patch
from app import app, mongo
from mockmongo import MockMongoDB


class TestBlockBtnRoute(unittest.TestCase):
    def setUp(self):
        # Configuration de l'application Flask pour les tests
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Initialisation du mock MongoDB
        self.mock_mongo = MockMongoDB()

        # Remplacement des collections MongoDB par les mocks
        mongo.db.questions = self.mock_mongo.get_collection("questions")
        mongo.db.scrutin_archive = self.mock_mongo.get_collection("scrutin_archive")

    @patch("flask_login.utils._get_user", return_value=MagicMock(is_authenticated=True))
    def test_block_btn_success(self, mock_user):
        # Simuler une question existante et son statut
        self.mock_mongo.get_collection("questions").find_one.side_effect = [
            {'_id': '12345', 'title_question': 'Test Question', 'status': 'active'},
            {'_id': '12345', 'title_question': 'Test Question', 'status': 'blocked'}
        ]
        self.mock_mongo.get_collection("questions").update_one.return_value.modified_count = 1
        self.mock_mongo.get_collection("questions").delete_one.return_value.deleted_count = 1
        self.mock_mongo.get_collection("scrutin_archive").find_one.return_value = None

        # Simuler une requête POST
        response = self.client.post('/B_btn', json={"Titre": "Test Question"})

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertEqual(response.json['message'], "Le sondage 'Test Question' a été bloqué, archivé et supprimé avec succès.")

    def tearDown(self):
        # Réinitialiser les mocks
        self.mock_mongo.reset()


if __name__ == '__main__':
    unittest.main()
