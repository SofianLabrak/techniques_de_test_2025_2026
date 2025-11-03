# Plan de Tests du Projet

## Vue d'ensemble

Au sein de ce projet, je prévois de mettre en place une multitude de tests. Deux catégories de tests différents vont être implémentées :

1. **Tests de comportement** : ils permettront de vérifier le fonctionnement du projet
2. **Tests de performance** : ils sont chargés de vérifier l'optimisation du code et de voir ses limites

---

## Tests Unitaires

### Tests de sérialisation

Dans un premier temps, des tests unitaires vont permettre de tester le comportement de chaque partie du code créé. 
Ils seront dans un premier temps nécessaires afin de vérifier la sérialisation et la désiarilisation.

Voici les tests utiles à cette vérification :

- Un test de sérialisation PointSet → Bytes
- Un test de désiarilisation Bytes → PointSet
- Un test de sérialisation Triangle → Bytes
- Un test de désiarilisation Bytes → Triangle

> **Note** : Un "Byte" est un octet en français et pas un bit.

### Tests de triangulation

D'autres tests unitaires vont être nécessaires afin de vérifier le comportement de la triangulation :

- **Test avec aucun point** : afin d'avoir une erreur
- **Test avec moins de 3 point** : afin d'avoir une erreur
- **Test avec 3 points** : afin de former un triangle
- **Test avec 4 points** : afin de former un carré et d'obtenir 2 triangles
- **Test avec 5 points** : afin de former un pentagone et d'obtenir 3 triangles
- **Test de validation** : qui permet de vérifier si les PointSet n'ont pas de points dupliqués/identiques

La triangulation doit respecter la règle suivante, pour n point, on obtient n-2 Triangles.

### Tests de l'API Web

Des tests unitaires sur la partie API Web vont être nécessaires :

- **Test des codes d'erreur** : vérifier la totalité des codes d'erreur des réponses HTTP (400, 404, 503)
- **Test de succès** : vérifier le succès de la requête et vérifier les informations reçues (200)

---

## Tests d'Intégration

Des tests d'intégration sont aussi nécessaires afin de vérifier le fonctionnement de l'ensemble du code produit. Cette étape est essentielle et permet de vérifier si la totalité du code produit est compatible et fonctionnel lorsqu'ils sont utilisés ensemble.

**Test complet avec PointSetManager** : 
- Vérification du PointSet
- Vérification de la triangulation
- Vérification de la requête API
- Vérification de la réponse reçue

---

## Tests de Performance

Après avoir effectué ces tests unitaires et d'intégration, nous allons pouvoir effectuer des tests de performance afin de connaître la puissance de notre code et son optimisation.

3 à 4 tests peuvent être effectués afin d'obtenir des informations claires concernant les performances de la Triangulation :

- Test de triangulation avec **10 points**
- Test de triangulation avec **100 points**
- Test de triangulation avec **1 000 points**
- Test de triangulation avec **10 000 points**

Nous allons aussi voir les performance de la sérialisation et désirialisation des PointsSet.

- Test de Sérialisation/Désiarilisation avec **10 points**
- Test de Sérialisation/Désiarilisation avec **100 points**
- Test de Sérialisation/Désiarilisation avec **1000 points**
- Test de Sérialisation/Désiarilisation avec **10000 points**

> **Note** : Les chiffres et le nombre de tests restent modulables.