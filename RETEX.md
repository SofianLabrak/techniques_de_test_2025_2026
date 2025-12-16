# Retour d'Expérience (RETEX) - Projet de Triangulation

Voici mon retour d'expérience sur le projet de triangulation. Je vais aborder les difficultés rencontrées, mes choix techniques et les évolutions par rapport au plan initial.

## 1. Bilan personnel du projet

Ce projet s'est révélé intéressant et a constitué un bon défi concernant la géométrie algorithmique et l'architecture logicielle. Cependant, j'ai manqué de temps pour mener à bien l'ensemble des objectifs que je m'étais donner. L'architecture est en place, mais je n'ai pas pu implémenter toute la logique souhaitée. C'est regrettable, mais cela fait partie des contraintes de l'exercice.

Il manque principalement un point d'entrée unique (`main`) pour exécuter l'ensemble du programme afin de pouvoir tester directement les différentes méthodes mise en place, ainsi qu'une interface de visualisation (telle que `matplotlib`) pour valider graphiquement les résultats.

## 2. Réalisations techniques

### 2.1. API et Tests (Mocking)
Le développement de l'API et des tests s'est déroulé de manière satisfaisante.
*   **Framework :** Flask.
*   **Configuration du port :** Sur mon environnement macOS, le port 5000 étant réservé par le système (AirDrop), j'ai dû configurer l'application sur le port **5001**.
*   **Tests :** J'ai mocké les classes comme le `PointSetManager` et le `Client`. Cela m'a permis de :
    *   Vérifier que l'API renvoie les réponses attendues.
    *   M'assurer qu'aucune donnée n'est perdue lors des échanges.
    *   Garantir l'intégrité des données récupérées.

**Couverture de code :**
Les efforts et la rigueur sur les tests ont permis d'atteindre une couverture :
*   `api.py` : **98%**
*   `point_set.py` : **92%**
*   `triangulator.py` : **100%**

Quelques ajustements mineurs permettraient d'atteindre une couverture complète sur l'ensemble du projet.

### 2.2. PointSet et Triangulators
J'ai séparé la gestion des données (`PointSet`) de la logique de calcul (`Triangulators`) en deux classes. L'objectif était de pouvoir changer d'algorithme sans impacter la structure du code. Toutefois, n'ayant pas créé de jeux de données réels, il est difficile d'analyser le comportement des algorithmes sur des cas complexes.

## 3. Performances et Complexité

J'ai réalisé des tests de performance, en me concentrant sur le temps d'exécution.
*   **Limite :** J'ai testé le système jusqu'à **10 000 points**.
*   **Analyse :**
    *   La triangulation de Delaunay a une complexité de $O(n \log n)$.
    *   La sérialisation JSON a une complexité de $O(n)$.
    *   Pour maintenir une exécution fluide (inférieure à 1 seconde), le système supporte quelques milliers de points. Au-delà de 10 000 points sur certaines machines, c'est la sérialisation qui commence à montrer ses limites, plutôt que le calcul géométrique. Cela dépend des ressources de la machine utilisée, de mon côté il était totalement faisable de faire la sérialisation de 50000 sans soucis.

## 4. La problématique des "n-2" triangles

J'ai identifié un problème avec ma règle de validation.
*   **Mon approche :** J'ai considéré qu'un polygone de $n$ points génère $n-2$ triangles.
*   **Le problème :** Cette règle est vraie pour un polygone simple, mais pas pour un nuage de points (comme dans une triangulation de Delaunay). Si des points se situent à l'intérieur de l'enveloppe convexe, le nombre de triangles augmente.
*   **Exemple :** Il est possible d'avoir 9 points qui génèrent 9 triangles.
*   **Conclusion :** Ma validation est trop stricte et incorrecte pour des nuages de points. Il faudrait utiliser la formule d'Euler ($V - E + F = 2$).

## 5. Écarts par rapport au Plan initial

J'ai dû adapter certains éléments par rapport à mes intentions de départ :

1.  **Gestion du temps :** J'ai sous-estimé le temps nécessaire pour mettre en place l'environnement de test.
2.  **Architecture :** J'ai d'avantage travaillé sur les simulations (Mocks) pour valider les flux de données chose qui était initalement pas prévu ayant comme objectif de faire un projet au complêt et fonctionnel cette partie était imprévu au plan initial.
3.  **Données :** J'avais prévu plusieurs jeux de données, mais je n'ai pas eu le temps de les constituer, ce qui m'a privé de visualisation.

## 6. Conclusion et perspectives

Si je devais recommencer ce projet :
1.  **Visualisation immédiate :** J'intégrerais `matplotlib` obligatoirement au sein du projet pour visualiser le code en action.
2.  **Rigueur mathématique :** Je corrigerais la validation en utilisant la formule d'Euler plutôt que la règle des $n-2$.
3.  **Création d'un main :** Je créerais un main python pour lancer une triangulation sur un fichier donné déterminer au préalable.

En conclusion, je dispose tout de même d'une base de tests solide et d'une API fonctionnelle, ce qui constitue l'essentiel pour la suite du développement.

