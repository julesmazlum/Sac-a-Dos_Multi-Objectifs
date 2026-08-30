# Sac à dos multi-objectifs — Dominance de Lorenz

Projet M2 AI2D 2025-2026 — UE Modèles et Algorithmes pour la Décision Multicritères et Collective (MADMC), Sorbonne Université. Auteurs : Jules MAZLUM, Camélia BOUALI.

## Description / Sujet

Le problème du sac à dos multi-objectifs consiste à sélectionner un sous-ensemble d'objets sous contrainte de capacité tout en optimisant simultanément plusieurs critères (profits multiples). Ce projet le résout en utilisant la **dominance de Lorenz** afin d'identifier des solutions équilibrées entre plusieurs critères.

Deux approches sont étudiées :

**Méthode indirecte (Pareto + Lorenz)**
- Programmation dynamique pour générer l'ensemble des solutions Pareto non dominées.
- Filtrage global des solutions selon la dominance de Lorenz.
- Analyse du nombre de solutions Pareto vs Lorenz.

**Méthode directe (OWA)**
- Optimisation d'une fonction d'agrégation OWA (Ordered Weighted Averaging) compatible avec la dominance de Lorenz.
- Linéarisation du modèle en programme linéaire en nombres entiers (PLNE).
- Génération itérative des vecteurs de Lorenz non dominés jusqu'à infaisabilité du modèle.

## Structure du dépôt

```text
.
├── data/                           Fichiers d'instances
├── methode_directe/                Implémentation de la méthode directe
│   ├── results/                    Résultats générés (CSV, graphiques, etc.)
│   ├── load.py                     Chargement des données et gestion des instances
│   ├── main.py                     Script principal pour exécuter la méthode directe
│   ├── model.py                    Modèles d'optimisation (P1, PL, méthode directe)
│   └── ut.py                       Expérimentations et analyse des résultats
├── methode_indirecte/              Implémentation de la méthode indirecte
│   ├── results/                    Résultats générés (CSV, graphiques, etc.)
│   ├── benchmark.py                Expérimentations
│   ├── main.py                     Script principal pour exécuter la méthode indirecte
│   ├── programmation_indirecte.py  Algorithmes de la méthode indirecte
│   └── utils.py                    Fonctions utiles (lecture, comparaison, Pareto...)
├── Projet_MADMC_MAZLUM-BOUALI.pdf  Rapport du projet
└── projetMADMC.pdf                 Énoncé du sujet
```

## Installation / Prérequis

Python 3.x et le solveur Gurobi.

```bash
pip install gurobipy numpy matplotlib
```

## Utilisation

**Méthode directe**, depuis `methode_directe/` :

```bash
python main.py
```

**Méthode indirecte**, depuis `methode_indirecte/` :

```bash
python main.py       # exemple de résolution sur petite instance
python benchmark.py  # résultats numériques et graphiques
```

Les résultats (temps de calcul, solutions, graphiques) sont générés dans le dossier `results/` de chaque méthode.

## Résultats principaux

- Étude de l'influence du nombre d'objets `n` et du nombre d'objectifs `p` sur les deux méthodes.
- Comparaison des temps de calcul entre méthode directe et méthode indirecte.
- Analyse de la volumétrie des solutions (nombre de solutions Pareto vs Lorenz non dominées).
- Étude de l'influence des poids OWA sur la méthode directe.

Le détail est disponible dans le rapport `Projet_MADMC_MAZLUM-BOUALI.pdf`.

## Auteurs

- Jules MAZLUM
- Camélia BOUALI
