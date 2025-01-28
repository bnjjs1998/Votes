import unittest
from unittest.mock import MagicMock, patch
from app import app, mongo
from tests.mockmongo import MockMongoDB  # Importer votre MockMongoDB

class TestGetResultRoute(unittest.TestCase):
    def setUp(self):
        # Configuration de l'application Flask pour les tests
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Initialisation de MockMongoDB
        self.mock_mongo = MockMongoDB()

        # Remplacement des collections MongoDB par les mocks
        mongo.db.scrutin_archive = self.mock_mongo.get_collection("scrutin_archive")

    @patch("flask_login.utils._get_user", return_value=MagicMock(is_authenticated=True))
    def test_get_result_success(self, mock_user):
        # Simuler des données archivées dans `scrutin_archive`
        mock_data = [
            {'_id': '12345', 'title': 'Archived Question 1', 'status': 'archived'},
            {'_id': '67890', 'title': 'Archived Question 2', 'status': 'archived'}
        ]
        self.mock_mongo.get_collection("scrutin_archive").find.return_value = mock_data

        # Simuler une requête GET
        response = self.client.get('/get_result')

        # Assertions sur le statut de la réponse
        self.assertEqual(response.status_code, 200)

        # Vérifications sur le contenu de la réponse
        response_data = response.get_json()
        self.assertEqual(len(response_data["data"]), 2)
        self.assertEqual(response_data["data"][0]["_id"], "12345")
        self.assertEqual(response_data["data"][1]["_id"], "67890")
        self.assertEqual(response_data["data"][0]["title"], "Archived Question 1")

    @patch("flask_login.utils._get_user", return_value=MagicMock(is_authenticated=False))
    def test_get_result_unauthorized(self, mock_user):
        # Simuler une requête GET sans utilisateur authentifié
        response = self.client.get('/get_result')

        # Vérifications sur le statut de redirection
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
        self.assertIn('/login', response.headers['Location'])  # Vérifie que la redirection cible `/login`

    def tearDown(self):
        # Réinitialiser les mocks après chaque test
        self.mock_mongo.reset()


if __name__ == '__main__':
    unittest.main()
