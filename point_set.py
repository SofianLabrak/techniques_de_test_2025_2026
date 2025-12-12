import struct


class PointSet:
    def __init__(self, points: list[tuple[float, float]] = None):
        self.points = []
        if points:
            for p in points:
                self.add_point(float(p[0]), float(p[1]))

    def add_point(self, x: float, y: float) -> None:
        self.points.append((float(x), float(y)))

    def get_points(self) -> list[tuple[float, float]]:
        return list(self.points)

    def count(self) -> int:
        return len(self.points)

    def serialize(self) -> bytes:
        # 4 octets (entier non signé) : nombre de points
        # pour chaque point : 8 octets (2 floats de 4 octets : x et y)
        tampon = bytearray()
        
        # Écriture du nombre de points
        tampon.extend(struct.pack('>I', self.count()))
        
        # Écriture des coordonnées de chaque point
        for x, y in self.points:
            tampon.extend(struct.pack('>ff', float(x), float(y)))
            
        return bytes(tampon)

    @classmethod
    def deserialize(cls, donnees: bytes) -> 'PointSet':
        # Vérification de la taille minimale (au moins 4 octets pour le compteur)
        if len(donnees) < 4:
            raise ValueError("Données invalides pour PointSet")
            
        decalage = 0
        
        # Lecture du nombre de points
        (nombre_points,) = struct.unpack_from('>I', donnees, decalage)
        decalage += 4
        
        points_lus = []
        for _ in range(nombre_points):
            # Vérification qu'il reste assez de données pour lire un point (8 octets)
            if decalage + 8 > len(donnees):
                raise ValueError("Données tronquées pour les points")
                
            # Lecture des coordonnées x et y
            x, y = struct.unpack_from('>ff', donnees, decalage)
            points_lus.append((float(x), float(y)))
            decalage += 8
            
        return cls(points_lus)

    def __repr__(self) -> str:
        return f"PointSet({self.points!r})"
