import time

import pytest

from point_set import PointSet
from triangulator import Triangulator


class TestTriangulationPerformance:

    @pytest.mark.perf
    def test_triangulation_perf_10_points(self):
        # Triangulation avec 10 points
        points = [(float(i), float(i+1)) for i in range(10)]
        point_set = PointSet(points)
        triangulator = Triangulator(point_set)
        start = time.perf_counter()
        triangles = triangulator.triangulate()
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée 10 points: {duration_ms:.3f} ms")
        assert duration_ms < 100, f"Triangulation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_triangulation_perf_100_points(self):
        # Triangulation avec 100 points
        points = [(float(i), float(i+1)) for i in range(100)]
        point_set = PointSet(points)
        triangulator = Triangulator(point_set)
        start = time.perf_counter()
        triangles = triangulator.triangulate()
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée 100 points: {duration_ms:.3f} ms")
        assert duration_ms < 500, f"Triangulation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_triangulation_perf_1000_points(self):
        # Triangulation avec 1000 points
        points = [(float(i), float(i+1)) for i in range(1000)]
        point_set = PointSet(points)
        triangulator = Triangulator(point_set)
        start = time.perf_counter()
        triangles = triangulator.triangulate()
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée 1000 points: {duration_ms:.3f} ms")
        assert duration_ms < 2000, f"Triangulation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_triangulation_perf_10000_points(self):
        # Triangulation avec 10000 points
        points = [(float(i), float(i+1)) for i in range(10000)]
        point_set = PointSet(points)
        triangulator = Triangulator(point_set)
        start = time.perf_counter()
        triangles = triangulator.triangulate()
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée 10000 points: {duration_ms:.3f} ms")
        assert duration_ms < 5000, f"Triangulation trop lente: {duration_ms:.3f} ms"


class TestSerializationPerformance:

    @pytest.mark.perf
    def test_serialization_perf_10_points(self):
        # Sérialisation/désérialisation avec 10 points
        points = [(float(i), float(i+1)) for i in range(10)]
        point_set = PointSet(points)
        start = time.perf_counter()
        serialized = point_set.serialize()
        deserialized = PointSet.deserialize(serialized)
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée sérialisation 10 points: {duration_ms:.3f} ms")
        assert duration_ms < 50, f"Sérialisation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_serialization_perf_100_points(self):
        # Sérialisation/désérialisation avec 100 points
        points = [(float(i), float(i+1)) for i in range(100)]
        point_set = PointSet(points)
        start = time.perf_counter()
        serialized = point_set.serialize()
        deserialized = PointSet.deserialize(serialized)
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée sérialisation 100 points: {duration_ms:.3f} ms")
        assert duration_ms < 100, f"Sérialisation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_serialization_perf_1000_points(self):
        # Sérialisation/désérialisation avec 1000 points
        points = [(float(i), float(i+1)) for i in range(1000)]
        point_set = PointSet(points)
        start = time.perf_counter()
        serialized = point_set.serialize()
        deserialized = PointSet.deserialize(serialized)
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée sérialisation 1000 points: {duration_ms:.3f} ms")
        assert duration_ms < 500, f"Sérialisation trop lente: {duration_ms:.3f} ms"

    @pytest.mark.perf
    def test_serialization_perf_10000_points(self):
        # Sérialisation/désérialisation avec 10000 points
        points = [(float(i), float(i+1)) for i in range(10000)]
        point_set = PointSet(points)
        start = time.perf_counter()
        serialized = point_set.serialize()
        deserialized = PointSet.deserialize(serialized)
        duration_ms = (time.perf_counter() - start) * 1000.0
        print(f" - Durée sérialisation 10000 points: {duration_ms:.3f} ms")
        assert duration_ms < 1000, f"Sérialisation trop lente: {duration_ms:.3f} ms"

