import struct

from point_set import PointSet

Triangle = tuple[int, int, int]


class Triangulator:
    def __init__(self, point_set: PointSet):
        self.point_set = point_set

    def triangulate(self) -> list[Triangle]:
        nombre_points = self.point_set.count()

        if nombre_points == 0:
            raise ValueError("Aucun point à trianguler")
        if nombre_points < 3:
            raise ValueError("Besoin d'au moins 3 points pour trianguler")

        points = self.point_set.get_points()

        points_vus = set()
        for p in points:
            if p in points_vus:
                raise ValueError("Les points dupliqués ne sont pas autorisés")
            points_vus.add(p)

        # On relie le premier point (indice 0) à tous les autres segments (i, i+1)
        liste_triangles = []
        for i in range(1, nombre_points - 1):
            liste_triangles.append((0, i, i + 1))

        return liste_triangles

    @staticmethod
    def serialize_triangles(point_set: PointSet, triangles: list[Triangle]) -> bytes:
        tampon = bytearray()

        tampon.extend(point_set.serialize())

        tampon.extend(struct.pack('>I', len(triangles)))

        for a, b, c in triangles:
            tampon.extend(struct.pack('>III', int(a), int(b), int(c)))

        return bytes(tampon)

    @staticmethod
    def deserialize_triangles(donnees: bytes) -> tuple[PointSet, list[Triangle]]:
        if len(donnees) < 4:
            raise ValueError("Données invalides pour Triangles")

        (nombre_points,) = struct.unpack_from('>I', donnees, 0)
        taille_points = 4 + (nombre_points * 8)

        if len(donnees) < taille_points:
            raise ValueError("Données tronquées pour les points dans Triangles")

        donnees_points = donnees[:taille_points]
        point_set = PointSet.deserialize(donnees_points)

        decalage = taille_points

        if len(donnees) < decalage + 4:
            raise ValueError("Données tronquées : compteur de triangles manquant")

        (nombre_triangles,) = struct.unpack_from('>I', donnees, decalage)
        decalage += 4

        triangles_lus = []
        for _ in range(nombre_triangles):
            if decalage + 12 > len(donnees):
                raise ValueError("Données tronquées pour les triangles")

            a, b, c = struct.unpack_from('>III', donnees, decalage)
            triangles_lus.append((int(a), int(b), int(c)))
            decalage += 12

        return point_set, triangles_lus


__all__ = ["Triangulator"]
