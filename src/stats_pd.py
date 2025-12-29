import time
import csv
import os
from utils import read_data
from programmation_dynamique import programmation_dynamique, filtre_lorenz
import pandas as pd
import matplotlib.pyplot as plt

def run_benchmarks():
    fichier_data = '../data/2KP200-TA-0.dat'
    fichier_res = '../sol/PD/resultats_bruts.csv'
    
    # Préparer le fichier CSV
    if not os.path.exists(fichier_res):
        with open(fichier_res, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['p', 'n', 'temps', 'nb_pareto', 'nb_lorenz'])

    # On sépare les exécutions par p pour mieux gérer le temps
    configurations = []
    for p in [2, 3, 4, 5, 6]:
        for n in [20, 50, 100, 150, 200]:
            configurations.append((n, p))

    for n, p in configurations:
        print(f"Calcul en cours : p={p}, n={n}...")
        
        # Lecture et calcul de W 
        objets = read_data(fichier_data, nb_objets_max=n, nb_objectifs=p)
        W = sum(i['w'] for i in objets) // 2
        
        # Mesure du temps
        start_time = time.time()
        try:
            # Phase 1 : Génération Pareto
            pareto = programmation_dynamique(objets, W)
            nb_p = len(pareto)
            
            # Phase 2 : Filtrage Lorenz
            lorenz = filtre_lorenz(pareto)
            nb_l = len(lorenz)
            
            duree = time.time() - start_time
            
            # Sauvegarde dans le fichier
            with open(fichier_res, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([p, n, duree, nb_p, nb_l])
            
            print(f"Terminé : {nb_p} Pareto, {nb_l} Lorenz en {duree:.2f}s")
            
        except MemoryError:
            print(f"ERREUR : Mémoire insuffisante pour p={p}, n={n}")
            break # On arrête pour ce p si la mémoire sature

def generate_plots():
    df = pd.read_csv('../sol/PD/resultats_bruts.csv')

    # Graphique des temps de calcul
    plt.figure(figsize=(10, 5))
    for p in df['p'].unique():
        subset = df[df['p'] == p]
        plt.plot(subset['n'], subset['temps'], marker='o', label=f'p={p}')
    
    plt.yscale('log')
    plt.title("Temps de calcul - Méthode Indirecte")
    plt.xlabel("Nombre d'objets (n)")
    plt.ylabel("Temps (secondes)")
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.savefig('../sol/PD/graph_temps.png')
    plt.show()

    # Graphique du nombre de points
    plt.figure(figsize=(10, 5))

    for p in df['p'].unique():
        subset = df[df['p'] == p]
        
        # On trace Pareto en pointillé
        line, = plt.plot(subset['n'], subset['nb_pareto'], '--', label=f'Pareto p={p}')
        color = line.get_color()
        plt.plot(subset['n'], subset['nb_lorenz'], '-', color=color, label=f'Lorenz p={p}')

    plt.title("Nombre de points générés")
    plt.xlabel("n")
    plt.ylabel("Nombre de points")
    plt.legend()
    plt.grid(True)
    plt.savefig('../sol/PD/graph_points.png')
    plt.show()

def plot_2d_space():
    objets = read_data('../data/2KP200-TA-0.dat', nb_objets_max=200, nb_objectifs=2)
    W = sum(i['w'] for i in objets) // 2
    
    print("Calcul des points pour n=200, p=2...")
    pareto = programmation_dynamique(objets, W)
    lorenz = filtre_lorenz(pareto)
    
    px, py = zip(*pareto)
    lx, ly = zip(*lorenz)
    
    plt.figure(figsize=(8, 7))
    plt.scatter(px, py, c='lightgrey', label='Pareto', s=15)
    plt.scatter(lx, ly, c='red', label='Lorenz', s=30, edgecolors='black')
    plt.title("Espace des objectifs (n=200, p=2)")
    plt.xlabel("Objectif 1")
    plt.ylabel("Objectif 2")
    plt.legend()
    plt.savefig('../sol/PD/visualisation_2d.png')
    plt.show()

if __name__ == "__main__":
    #run_benchmarks()
    generate_plots()
    #plot_2d_space()

    