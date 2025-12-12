import uuid
from unittest.mock import patch

import pytest

from api import PointSetManagerError, PointSetNotFoundError, app
from point_set import PointSet
from triangulator import Triangulator


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestTriangulationAPI:
    
    def test_triangulation_succes(self, client):
        ps_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        
        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{ps_id}')
            
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
        ps_id = str(uuid.uuid4())
        with patch('api.get_pointset_from_manager', side_effect=PointSetNotFoundError("PointSet non trouvé")):
            response = client.get(f'/triangulation/{ps_id}')
            assert response.status_code == 404
            assert "PointSet non trouvé" in response.json['error']

    def test_erreur_pointset_manager(self, client):
        ps_id = str(uuid.uuid4())
        with patch('api.get_pointset_from_manager', side_effect=PointSetManagerError("Erreur de connexion")):
            response = client.get(f'/triangulation/{ps_id}')
            assert response.status_code == 503
            assert "Erreur de connexion" in response.json['error']

    def test_erreur_triangulation_pas_assez_de_points(self, client):
        ps_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0)]) # Only 2 points
        
        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{ps_id}')
            assert response.status_code == 400
            assert "Besoin d'au moins 3 points" in response.json['error']

    def test_erreur_triangulation_points_dupliques(self, client):
        ps_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (0.0, 0.0), (1.0, 1.0)]) # Duplicates
        
        with patch('api.get_pointset_from_manager', return_value=point_set):
            response = client.get(f'/triangulation/{ps_id}')
            assert response.status_code == 400
            assert "points dupliqués" in response.json['error']

    def test_erreur_interne_serveur(self, client):
        ps_id = str(uuid.uuid4())
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        
        with patch('api.get_pointset_from_manager', return_value=point_set):
            with patch('api.Triangulator.triangulate', side_effect=Exception("Unexpected crash")):
                response = client.get(f'/triangulation/{ps_id}')
                assert response.status_code == 500
                assert "Erreur interne du serveur" in response.json['error']
