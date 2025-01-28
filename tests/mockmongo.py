from unittest.mock import MagicMock

class MockMongoDB:
    def __init__(self):
        # Dictionnaire pour stocker les mocks des collections
        self.collections = {}

    def get_collection(self, name):
        """
        Retourne un mock pour une collection MongoDB.
        Si la collection n'existe pas encore, elle est créée.
        """
        if name not in self.collections:
            self.collections[name] = MagicMock()
        return self.collections[name]

    def simulate_error(self, collection_name, method_name, exception):
        """
        Simule une erreur pour une méthode donnée d'une collection spécifique.

        :param collection_name: Nom de la collection
        :param method_name: Méthode pour laquelle une erreur doit être simulée
        :param exception: Exception à lever lors de l'appel
        """
        collection = self.get_collection(collection_name)
        getattr(collection, method_name).side_effect = exception

    def reset(self):
        """
        Réinitialise toutes les collections mockées.
        """
        self.collections = {}
