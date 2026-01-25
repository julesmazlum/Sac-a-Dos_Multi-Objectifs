# Sac à dos multi-objectifs — Dominance de Lorenz

Projet académique portant sur la résolution du **problème du sac à dos multi-objectifs** en utilisant la **dominance de Lorenz** afin d’identifier des solutions équilibrées entre plusieurs critères.  
Réalisé dans le cadre du module **MADMC – Master 2**.

---

## Contributeurs
- Jules Mazlum  
- Camélia Bouali  

---

## Description

Le problème du sac à dos multi-objectifs consiste à sélectionner un sous-ensemble d’objets sous contrainte de capacité tout en optimisant simultanément plusieurs critères (profits multiples).

Dans ce projet, deux approches sont étudiées :
- **Méthode indirecte** : génération de l’ensemble des solutions Pareto non dominées, puis filtrage selon la dominance de Lorenz.
- **Méthode directe** : génération directe des solutions Lorenz non dominées par l’optimisation répétée d’une fonction d’agrégation **OWA (Ordered Weighted Averaging)**.

## Méthodes implémentées

### Méthode indirecte (Pareto + Lorenz)
- Programmation dynamique pour générer l’ensemble des solutions Pareto non dominées.
- Filtrage global des solutions selon la dominance de Lorenz.
- Analyse du nombre de solutions Pareto vs Lorenz.

### Méthode directe (OWA)
- Optimisation d’une fonction d’agrégation OWA compatible avec la dominance de Lorenz.
- Linéarisation du modèle en programme linéaire en nombres entiers (PLNE).
- Génération itérative des vecteurs de Lorenz non dominés jusqu’à infaisabilité du modèle.

### Analyse expérimentale
- Étude de l’influence du nombre d’objets `n` et du nombre d’objectifs `p`.
- Comparaison des temps de calcul entre les deux méthodes.
- Analyse de la volumétrie des solutions.
- Étude de l’influence des poids OWA.

---

## Structure du projet

```text
├── data/                           # Fichiers d’instances

├── methode_directe/                # Implémentation de la méthode directe
│   ├── results/                    # Résultats générés (CSV, graphiques, etc.)
│   ├── load.py                     # Chargement des données et gestion des instances
│   ├── main.py                     # Script principal pour exécuter la méthode directe
│   ├── model.py                    # Modèles d’optimisation (P1, PL, méthode directe)
│   └── ut.py                       # Expérimentations et analyse des résultats

├── methode_indirecte/              # Code source (autres méthodes / versions)
│   ├── results/                    # Résultats générés (CSV, graphiques, etc.)
│   ├── benchmark.py                # Expérimentations
│   ├── main.py                     # Script principal pour exécuter la méthode indirecte
│   ├── programmation_indirecte.py  # Les algorithmes de la méthode indirecte
│   ├── utils.py                    # Fonctions utiles (lectures, comparaison, pareto..)

└── README.md
```

## Exécution de la méthode directe

Pour exécuter la méthode directe, se placer dans le dossier **`methode_directe`** et lancer :

```bash
python main.py
```

Les résultats (temps de calcul, solutions, graphiques) sont générés dans le dossier results/.

## Exécution de la méthode indirecte

Pour exécuter la méthode indirecte, se placer dans le dossier **`methode_indirecte`** et lancer :

```bash
python main.py
```

Pour un exemple de résolution sur petite instance.

Et 

```bash
python benchmark.py
```

Pour pouvoir obtenir des résultats numériques et pouvoir tracer les graphiques.

## Dépendances

- Python 3.x
- Gurobi (gurobipy)
- NumPy
- Matplotlib (pour les graphiques)
