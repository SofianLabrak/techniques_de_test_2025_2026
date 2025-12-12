from point_set import PointSet


class TestPointSetSerialization:

    def test_serialize_pointset_to_bytes(self):
        ps = PointSet([(1.0, 2.0), (3.0, 4.0)])
        result = ps.serialize()
        # Le résultat doit être du binaire
        assert isinstance(result, bytes)
        # Doit contenir au moins 4 bytes (le nombre de points) + 8 bytes par point
        assert len(result) >= 4 + (2 * 8)

    def test_deserialize_bytes_to_pointset(self):
        ps = PointSet([(1.0, 2.0), (3.0, 4.0)])
        serialized = ps.serialize()
        deserialized = PointSet.deserialize(serialized)
        # Doit récupérer le même nombre de points
        assert deserialized.count() == 2
        # Les points doivent être identiques
        assert deserialized.get_points() == ps.get_points()

    def test_serialize_empty_pointset(self):
        ps = PointSet()
        result = ps.serialize()
        assert isinstance(result, bytes)
        # Juste les 4 bytes pour le nombre de points (0)
        assert len(result) == 4

    def test_deserialize_empty_pointset(self):
        ps = PointSet()
        serialized = ps.serialize()
        deserialized = PointSet.deserialize(serialized)
        assert deserialized.count() == 0


class TestPointSet:

    def test_ajout_point(self):
        ps = PointSet()
        ps.add_point(1.0, 2.0)
        assert ps.count() == 1
        assert ps.get_points() == [(1.0, 2.0)]

    def test_ajout_multiple_points(self):
        ps = PointSet()
        ps.add_point(1.0, 2.0)
        ps.add_point(3.0, 4.0)
        ps.add_point(5.0, 6.0)
        assert ps.count() == 3

    def test_get_points(self):
        points = [(1.0, 2.0), (3.0, 4.0)]
        ps = PointSet(points)
        retrieved = ps.get_points()
        assert retrieved == points

    def test_count_points(self):
        ps = PointSet([(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)])
        assert ps.count() == 3
