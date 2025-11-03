Rendu : 

Au sein de ce projet je prévoie de mettre en place une multitudes de tests.
2 Catégories de tests différents vont être implémenter, la premières seras les tests de comportement, ils permettrons de vérifier le fonctionnement général du projet, la seconde catégorie seras les tests de performance, qui sont charger de vérifier l'optimisation du code et voir ses limites.

Dans un premier temps, des tests unitaire qui vont permettre de tests de comportement de chaque partie du code crer vas être nécéssaire afin de vérifier la conversion vers/depuis le binaire.

Voici les tests de comportement utile à cette vérification :
- PointSet -> Bytes
- Bytes -> PointSet
- Triangle -> Bytes
- Bytes -> Triangle

Attention, un "Byte" est un Octet en Français et pas un Bit.

D'autres tests unitaire vont être nécéssaire, afin de vérifier le comportement de la Triangulation.

Un test avec aucun point, afin d'avoir une erreur.
Un test avec des PointSet simple, 3 points afin de formé un triangle.
Un test avec un seul point afin de provoqué l'erreur.
Un test avec 4 points afin de former un carré et d'obtenir 2 triangles.
Un tsts avec 5 points afin de former un pentagone et d'obtenir 3 triangles.
Un test qui permet de vérifier si les PointSet n'on pas de points dupliqué/identique.

Des tests unitaire sur la partie API Web vas être nécéssaire.

Un test qui vas vérifier la totalité les codes d'erreur des réponses HTTP (400, 404, 503).
Un test qui vas vérifier le succès de la requête et vérifier les informations reçus (200).

Des tests d'intégration sont aussi nécéssaire afin de vérifier le fonctionnement de l'ensemble du code produit.
Cette étape est essentiel et permet de vérifier si la totalité du code produit est compatible et fonctionnel lors qu'ils sont utiliser enssemble.

Un test avec un PointSetManager qui vas vérifier le PointSet, la triangulation, la requête API ainsi que la réponse reçus.


Après avoir effectuer ces tests unitaire et d'intégration, nous allons pouvoir effectuer des tests de performance afin de connaitre la puissance de notre code et son optimisation.

3 à 4 tests peuvent être effectué afin d'obtenir des informations claire concernant les performances.

Un test de triangulation avec 10 points.
Un test de triangulation avec 100 points.
Un test de triangulation avec 1000 points.
Un test de triangulation avec 10000 points.

(Les chiffres et le nombre de test reste modulable)