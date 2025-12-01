import pytest
from point_set import PointSet
from triangulator import Triangulator


class TestTriangulator:
    def test_triangulation_avec_aucun_points(self):
        # Test avec aucun point

        ps = PointSet()
        triangulator = Triangulator(ps)
        with pytest.raises(Exception):
            triangulator.triangulate()

    def test_triangulation_avec_moins_de_3_points(self):
        # Test avec moins de 3 points

        ps = PointSet([(0.0, 0.0), (1.0, 1.0)])
        triangulator = Triangulator(ps)
        with pytest.raises(Exception):
            triangulator.triangulate()

    def test_triangulation_avec_3_points(self):
        # Test avec 3 points

        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        # Doit retourner un objet Triangles avec 1 triangle
        assert triangles is not None
        assert triangles.count() == 1

    def test_triangulation_avec_4_points(self):
        # Test avec 4 points

        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        # Doit retourner un objet Triangles avec 2 triangles
        assert triangles is not None
        assert triangles.count() == 2

    def test_triangulation_avec_5_points(self):
        # Test avec 5 points

        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (1.0, 1.0), (1.0, -1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        # Doit retourner un objet Triangles avec 3 triangles
        assert triangles is not None
        assert triangles.count() == 3

    def test_triangulation_regle_n_minus_2(self):
        # Vérifie la règle pour n points, on obtient n-2 triangles

        for n in [3, 4, 5]:
            points = [(float(i), 0.0) for i in range(n)]
            ps = PointSet(points)
            triangulator = Triangulator(ps)
            triangles = triangulator.triangulate()
            assert triangles.count() == n - 2

    def test_triangulation_avec_points_dupliques(self):
        # Test de validation : pas de points dupliqués/identiques

        ps = PointSet([(1.0, 1.0), (1.0, 1.0), (2.0, 2.0)])
        triangulator = Triangulator(ps)
        with pytest.raises(Exception):
            triangulator.triangulate()


class TestTrianglesSerialization:

    def test_serialize_triangles_to_bytes(self):
        # Sérialisation Triangles -> Bytes

        # PointSet avec 3 points qui forme un triangle
        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        result = triangles.serialize()

        # Le résultat doit être du binaire
        assert isinstance(result, bytes)
            # Doit contenir au moins 4 bytes (le nombre de triangles) + 12 bytes par triangle
            assert len(result) >= 4 + (1 * 12)

    def test_deserialize_bytes_to_triangles(self):
        # Désérialisation Bytes -> Triangles

        # PointSet avec 3 points qui forme un triangle
        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        serialized = triangles.serialize()
        deserialized = triangles.deserialize(serialized)

        # Doit avoir le même nombre de triangles
        assert deserialized.count() == 1

    def test_triangles_test_serialization_deserialization(self):
        # Test sérialisation puis désérialisation
        ps = PointSet([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        triangulator = Triangulator(ps)
        triangles = triangulator.triangulate()
        serialized = triangles.serialize()
        deserialized = triangles.deserialize(serialized)
        
        assert deserialized.count() == triangles.count()
