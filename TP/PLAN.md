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

#### Sérialisation PointSet

**Objectif** : Valider que les PointSets peuvent être convertis en binaire selon la spécification et reconvertis sans perte d'information.

**Approche** :

- **Test de sérialisation PointSet -> Bytes** : Vérifier que le PointSet est correctement converti en binaire
  - Format: 4 bytes (nombre de points) + pour chaque point: 8 bytes (4 pour X float + 4 pour Y float)
- **Test de désérialisation Bytes -> PointSet** : Vérifier que les bytes sont correctement reconvertis en PointSet
- **Test sérialisation/désérialisation** : Sérialiser puis désérialiser doit retourner le même PointSet

#### Sérialisation Triangles

**Objectif** : Valider que les Triangles (ensemble de sommets + triangles) peuvent être sérialisés/désérialisés correctement selon la spécification deux-parties.

**Approche** :

- **Test de sérialisation Triangles -> Bytes** : Vérifier que les triangles sont correctement convertis en binaire
  - Format: 
    - Partie 1 (PointSet): 4 bytes (nombre de points) + pour chaque point: 8 bytes (4 pour X float + 4 pour Y float)
    - Partie 2 (Triangles): 4 bytes (nombre de triangles) + pour chaque triangle: 12 bytes (3 × 4 bytes pour les indices)
- **Test de désérialisation Bytes -> Triangles** : Vérifier que les bytes sont correctement reconvertis en Triangles
- **Test sérialisation/désérialisation** : Sérialiser puis désérialiser doit retourner les mêmes Triangles

> **Note** : Un "Byte" est un octet en français et pas un bit.

### Tests de triangulation

**Objectif** : Valider que l'algorithme de triangulation produit des résultats corrects selon la règle n-2 et respecte les contraintes (minimum 3 points, sans doublons ou point aligné).

**Approche ** : Pour chaque cas, créer un PointSet, invoquer la triangulation, et vérifier le nombre et la validité des triangles obtenue.

**Tests unitaires** :

- **Test avec aucun point** : afin d'avoir une erreur
- **Test avec moins de 3 point** : afin d'avoir une erreur
- **Test avec 3 points** : afin de former un triangle
- **Test avec 4 points** : afin de former un carré et d'obtenir 2 triangles
- **Test des points colinéaire** : ensemble de point qui forme une ligne, doit être en erreur
- **Test de validation** : qui permet de vérifier si les PointSet n'ont pas de points identiques

> **Note** : La triangulation doit respecter la règle suivante, pour n point, on obtient n-2 Triangles.

### Tests de l'API Web

**Objectif** : Valider que l'API WEB du Triangulator respecte lES codes HTTP et formats de réponse.

**Approche ** : Effectuer des requêtes HTTP (GET /triangulation/{pointSetId}) avec différents paramètres et vérifier le code HTTP et le format de la réponse.

#### Test de succès (200)

- **Test avec PointSetID valide et PointSet valide**
  - Objectif: Vérifier que la requête réussit et retourne les Triangles
  - Approche: 
    1. Créer un PointSet auprès du PointSetManager afin d'avoir un pointSetId
    2. Faire une requête GET /triangulation/{pointSetId}
    3. Vérifier et obtenir un code 200
    4. Vérifier que la réponse est bien sérialisé-
    5. Vérifier que les Triangles peuvent être désérialisés

#### Erreurs 400 - Bad Request

**Objectif** : Vérifier que les erreurs de suivante retournent côté client le code 400.

- **Format UUID invalide**
  - Objectif: Rejeter les PointSetID mal formés
  - Approche: Faire une requête avec pointSetId = "invalid-uuid" ou "12345"
  - Vérification: Code 400, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

- **PointSet avec moins de 3 points**
  - Objectif: Rejeter les PointSets trop petits
  - Approche: Enregistrer un PointSet avec 1-2 points, demander la triangulation
  - Vérification: Code 400, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

- **PointSet avec points dupliqués**
  - Objectif: Rejeter les PointSets avec points identiques
  - Approche: Enregistrer un PointSet avec doublons, demander la triangulation
  - Vérification: Code 400, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

#### Erreur 404 - Not Found

- **PointSetID correcte mais inexistant**
  - Objectif: Indiquer que le PointSet n'existe pas
  - Approche: Utiliser un UUID valide mais jamais enregistré
  - Vérification: Code 404, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

#### Erreur 500 - Internal Server Error

- **Soucis lors d'une action serveur**
  - Objectif: Gérer les erreurs internes au serveur
  - Approche: Créer des conditions qui causent l'échec côté server (problème de triangulation)
  - Vérification: Code 500, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

#### Erreur 503 - Service Unavailable

- **PointSetManager indisponible**
  - Objectif: Gérer l'absence de PointSetManager
  - Approche: Arrêter le PointSetManager
  - Vérification: Code 503, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

- **Timeout de connexion avec PointSetManager**
  - Objectif: Gérer les délais d'attente et problèmes de connection
  - Approche: Configurer un timeout court afin de le déclencher et utiliser un service qui ne répond pas
  - Vérification: Code 503, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

- **Base de données inaccessible**
  - Objectif: Gérer les erreurs de la base de donnée
  - Approche: Arrêter la base de données ou faire echoué son accès
  - Vérification: Code 503, message d'erreur approprié cf.triangulator.yml et point_set_manager.yml

---

## Tests d'Intégration

**Objectif** : Valider que l'ensemble du système fonctionne correctement avec le PointSetManager.

**Approche** : Tester un workflow complet du client jusqu'au résultat final.

### Test complet

**Étapes** :
1. **Enregistrement d'un PointSet** : POST /pointset (PointSetManager)
   - Créer un PointSet, le sérialiser, l'envoyer au PointSetManager
   - Récupérer le pointSetId retourné
   - Vérification: Code 201, pointSetId valide en format UUID

2. **Récupération du PointSet** : GET /pointset/{pointSetId} (PointSetManager)
   - Vérifier que le PointSet peut être récupéré
   - Vérification: Code 200, données binaires identiques à l'original

3. **Requête de triangulation** : GET /triangulation/{pointSetId} (Triangulator)
   - Demander la triangulation via le Triangulator
   - Le Triangulator récupère le PointSet du PointSetManager en interne
   - Vérification: Code 200, Triangles en binaire

4. **Validation des Triangles** : Désérialisation et vérification
   - Désérialiser les Triangles reçus
   - Vérifier que les indices pointent correctement vers les points originaux
   - Vérification: Nombre de triangles = n-2, indices valides

---

## Tests de Performance

**Objectif** : Mesurer les performances de l'algorithme de triangulation et des opérations de sérialisation/désérialisation afin de connaitre les limites du systèmes.

### Tests de Performance - Triangulation

**Objectif** : Mesurer le temps d'exécution de l'algorithme pour différentes tailles de PointSet.

- **Test avec 10 points**
  - Approche: Créer 10 points aléatoires ou réguliers, mesurer le temps de triangulation
  - Métrique: Temps en ms (baseline)

- **Test avec 100 points**
  - Approche: Créer 100 points aléatoires, mesurer le temps
  - Métrique: Temps en ms

- **Test avec 1 000 points**
  - Approche: Créer 1000 points aléatoires, mesurer le temps
  - Métrique: Temps en ms

- **Test avec 10 000 points**
  - Approche: Créer 10000 points aléatoires, mesurer le temps
  - Métrique: Temps en ms

### Tests de Performance - Sérialisation/Désérialisation PointSet

**Objectif** : Mesurer les performances du cycle sérialisation → désérialisation.

- **Test avec 10 points**
  - Approche: Mesurer le temps pour serialize() + deserialize()
  - Métrique: Temps en ms

- **Test avec 100 points**
  - Approche: Idem
  - Métrique: Temps en ms

- **Test avec 1 000 points**
  - Approche: Idem
  - Métrique: Temps en ms

- **Test avec 10 000 points**
  - Approche: Idem
  - Métrique: Temps en ms

### Tests de Performance - Sérialisation/Désérialisation Triangles

**Objectif** : Mesurer les performances pour les résultats de triangulation.

- **Test avec triangles issus de 100 points (98 triangles)**
- **Test avec triangles issus de 1 000 points (998 triangles)**
- **Test avec triangles issus de 10 000 points (9998 triangles)**
  - Approche: Pour chaque taille, trianguler puis mesurer serialize() + deserialize()
  - Métrique: Temps en ms

> **Note** : Les chiffres et le nombre de tests restent modulables. Les seuils de performance peuvent être ajustés selon les besoins.