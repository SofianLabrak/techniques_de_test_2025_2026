import pytest
import struct

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

    def test_deserialize_header_invalide(self):
        # Données trop courtes (< 4 octets)
        data = b'\x00\x00'
        with pytest.raises(ValueError, match="Données invalides pour Triangles"):
            Triangulator.deserialize_triangles(data)

    def test_deserialize_points_tronques(self):
        # 10 points déclarés + données incomplètes (2 octets contre 80 attendus)
        data = struct.pack('>I', 10) + b'\x00\x00'
        with pytest.raises(ValueError, match="Données tronquées pour les points"):
            Triangulator.deserialize_triangles(data)

    def test_deserialize_compteur_triangles_manquant(self):
        # 0 points, mais manque le compteur de triangles
        data = struct.pack('>I', 0)
        with pytest.raises(ValueError, match="Données tronquées : compteur de triangles manquant"):
            Triangulator.deserialize_triangles(data)

    def test_deserialize_triangles_tronques(self):
        # 0 points + 1 triangle déclaré + données incomplètes (2 octets contre 12 attendus)
        data = struct.pack('>I', 0) + struct.pack('>I', 1) + b'\x00\x00'
        with pytest.raises(ValueError, match="Données tronquées pour les triangles"):
            Triangulator.deserialize_triangles(data)
