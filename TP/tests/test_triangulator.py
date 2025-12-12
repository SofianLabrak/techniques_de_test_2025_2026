import pytest

from point_set import PointSet
from triangulator import Triangulator


class TestTriangulator:
    def test_triangulation_avec_aucun_points(self):
        point_set = PointSet()
        triangulator = Triangulator(point_set)
        with pytest.raises(ValueError):
            triangulator.triangulate()

    def test_triangulation_avec_moins_de_3_points(self):
        point_set = PointSet([(0.0, 0.0), (1.0, 1.0)])
        triangulator = Triangulator(point_set)
        with pytest.raises(ValueError):
            triangulator.triangulate()

    def test_triangulation_avec_3_points(self):
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)])
        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()
        # Doit retourner une liste de triangles
        assert triangles is not None
        assert len(triangles) == 1

    def test_triangulation_avec_4_points(self):
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()
        # Doit retourner une liste de 2 triangles
        assert triangles is not None
        assert len(triangles) == 2

    def test_triangulation_avec_5_points(self):
        point_set = PointSet([
            (0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (1.0, 1.0), (1.0, -1.0)
        ])
        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()
        # Doit retourner une liste de 3 triangles
        assert triangles is not None
        assert len(triangles) == 3

    def test_triangulation_regle_n_minus_2(self):
        # Vérifie la règle pour n points, on obtient n-2 triangles

        for n in [3, 4, 5]:
            points = [(float(i), 0.0) for i in range(n)]
            point_set = PointSet(points)
            triangulator = Triangulator(point_set)
            triangles = triangulator.triangulate()
            assert len(triangles) == n - 2

    def test_triangulation_avec_points_dupliques(self):
        point_set = PointSet([(1.0, 1.0), (1.0, 1.0), (2.0, 2.0)])
        triangulator = Triangulator(point_set)
        with pytest.raises(ValueError):
            triangulator.triangulate()


class TestTrianglesSerialization:

    def test_serialize_triangles_to_bytes(self):
        # Sérialisation Triangles -> Bytes

        # PointSet avec 3 points
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()
        result = Triangulator.serialize_triangles(point_set, triangles)

        # Le résultat doit être binaire
        assert isinstance(result, bytes)
        # Doit contenir la partie PointSet (4 + 3*8 = 28 bytes)
        # + partie Triangles (4 + 1*12 = 16 bytes) = 44 bytes
        assert len(result) == 28 + 16

    def test_deserialize_bytes_to_triangles(self):
        # Désérialisation Bytes -> Triangles

        # PointSet avec 3 points
        point_set = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
        triangulator = Triangulator(point_set)
        triangles = triangulator.triangulate()
        serialized = Triangulator.serialize_triangles(point_set, triangles)
        ps_deserialized, triangles_deserialized = Triangulator.deserialize_triangles(
            serialized
        )

        # Doit avoir le même nombre de triangles
        assert len(triangles_deserialized) == 1
        # Doit avoir le même nombre de points
        assert ps_deserialized.count() == 3

