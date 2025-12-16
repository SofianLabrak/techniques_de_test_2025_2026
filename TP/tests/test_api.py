import uuid
from unittest.mock import patch, MagicMock
import requests

import pytest

from api import PointSetManagerError, PointSetNotFoundError, app, get_pointset_from_manager
from point_set import PointSet
from triangulator import Triangulator


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTriangulationAPI:
    def test_triangulation_succes(self, client):
        pointset_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])

        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{pointset_id}')

            assert response.status_code == 200
            assert response.mimetype == 'application/octet-stream'

            # Verify content
            _, triangles = Triangulator.deserialize_triangles(response.data)
            assert len(triangles) == 1

    def test_uuid_invalide(self, client):
        response = client.get('/triangulation/invalid-uuid')
        assert response.status_code == 400
        assert "Format UUID invalide" in response.json['error']

    def test_pointset_non_trouve(self, client):
        pointset_id = str(uuid.uuid4())
        error = PointSetNotFoundError("PointSet non trouvé")
        with patch('api.get_pointset_from_manager', side_effect=error):
            response = client.get(f'/triangulation/{pointset_id}')
            assert response.status_code == 404
            assert "PointSet non trouvé" in response.json['error']

    def test_erreur_pointset_manager(self, client):
        pointset_id = str(uuid.uuid4())
        error = PointSetManagerError("Erreur de connexion")
        with patch('api.get_pointset_from_manager', side_effect=error):
            response = client.get(f'/triangulation/{pointset_id}')
            assert response.status_code == 503
            assert "Erreur de connexion" in response.json['error']

    def test_erreur_triangulation_pas_assez_de_points(self, client):
        pointset_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0)])  # Avec 2 points seulement

        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{pointset_id}')
            assert response.status_code == 400
            assert "Besoin d'au moins 3 points" in response.json['error']

    def test_erreur_triangulation_points_dupliques(self, client):
        pointset_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)])  # Dupliquer

        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{pointset_id}')
            assert response.status_code == 400
            assert "points dupliqués" in response.json['error']

    def test_erreur_interne_serveur(self, client):
        pointset_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])

        with patch('api.get_pointset_from_manager', return_value=point_set), \
                patch(
                    'api.Triangulator.triangulate',
                    side_effect=Exception("Unexpected crash")
                ):
            response = client.get(f'/triangulation/{pointset_id}')
            assert response.status_code == 500
            assert "Erreur interne du serveur" in response.json['error']


class TestGetPointSetFromManager:
    def test_get_pointset_succes(self):
        # On récupère bien un PointSet
        pointset_id = "test-id"
        # Simule une réponse 200 OK avec un PointSet sérialisé
        mock_response = MagicMock(status_code=200, content=PointSet([(0, 0)]).serialize())

        with patch('requests.get', return_value=mock_response) as mock_get:
            result = get_pointset_from_manager(pointset_id)

            # Vérifie que l'URL est correcte
            mock_get.assert_called_once_with(f"http://localhost:5001/pointset/{pointset_id}")
            assert isinstance(result, PointSet)

    def test_get_pointset_non_trouve(self):
        # Erreur 404 : le PointSet n'existe pas
        pointset_id = "inconnu"
        with patch('requests.get', return_value=MagicMock(status_code=404)):
            with pytest.raises(PointSetNotFoundError):
                get_pointset_from_manager(pointset_id)

    def test_get_pointset_erreur_serveur(self):
        # Erreur 500 : Erreur du service distant
        pointset_id = "bug"
        with patch('requests.get', return_value=MagicMock(status_code=500)):
            with pytest.raises(PointSetManagerError):
                get_pointset_from_manager(pointset_id)

    def test_get_pointset_erreur_connexion(self):
        # Erreur réseau : Impossible de se connecter
        pointset_id = "disconntect"
        with patch('requests.get', side_effect=requests.RequestException):
            with pytest.raises(PointSetManagerError):
                get_pointset_from_manager(pointset_id)
