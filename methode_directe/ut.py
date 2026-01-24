from model import P1, PL, lorenz_vector, methode_directe
from load import data, instances_n_p
import time
import csv
import matplotlib.pyplot as plt


# ============================
# Test de la méthode directe
# ============================

def run_experiments(filename):
    """
    Applique la méthode directe sur différentes instances du fichier donné.
    Pour chaque couple (n, p), la fonction :
    - extrait les données correspondantes
    - mesure le temps d'exécution de la méthode directe
    - enregistre le nombre de vecteurs de Lorenz générés
    Les résultats sont sauvegardés dans un fichier CSV.
    """

    # Chargement des instances depuis le fichier
    instances=data(filename) 

    Ns = [20,50,100,150,200]  # Liste des nombres d'objets testés
    Ps = [2,3,4,5,6]  # Liste des nombres d'objectifs testés

    results = []

    with open("results/res_methode_directe.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n","p","time_direct","nb_lorenz_direct"])


        for n in Ns:
            for p in Ps:

                w, v = instances_n_p(instances,n,p)
                print(f"\nInstance n={n}, p={p}")

                #Méthode directe
                L = []
                W = sum(w)//2
                #Poids OWA strictement décroissants
                omega = [p-i for i in range(p)]
                print("omega = ",omega)
                lambda_ = [omega[k]-omega[k+1] for k in range(p-1)]+[omega[p-1]]

                try:
                    # Mesure du temps d'exécution
                    start = time.time()
                    res = methode_directe(n,p,W,w,v,lambda_,L)
                    elapsed = time.time() - start

                    
                    t_dir, nb_lorenz_dir = elapsed, res
                
                except Exception as e:
                    print("Erreur : ",e)

                    t_dir, nb_lorenz_dir = None, None

                # Sauvegarde des résultats dans le fichier CSV
                writer.writerow([n,p,t_dir,nb_lorenz_dir])

                results.append({
                    "n" : n,
                    "p" : p,
                    "t_direct" : t_dir,
                    "lorenz_dir" : nb_lorenz_dir

                })

    return results


# ============================================
# Étude de l'influence des poids OWA
# ============================================

def influence_owa(filename):
    """
    Étudie l'influence du choix des poids OWA sur :
    - le temps de calcul
    - le nombre de vecteurs de Lorenz générés

    L'expérience est réalisée sur une instance fixe (n=50, p=3),
    avec différents jeux de poids OWA.
    """

    #On fixe une instance : ici n = 50 et p = 3
    n , p = 50 , 3
    instances = data(filename)
    w, v = instances_n_p(instances,n,p)
    print(f"\nInstance n={n}, p={p}")

    results = []

    # Capacité du sac à dos
    W = sum(w)//2
    
    # Différents jeux de poids OWA
    o1 = [0.7, 0.2, 0.1] # faiblement équitable
    o2 = [0.5, 0.3, 0.2] # équilibré (réf)
    o3 = [0.45, 0.35, 0.25] # fortement équitable (plus contraignant)
  

    omegas = [o1,o2,o3]

    with open("results/results_direct_owa.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n","p","omega","time_direct","nb_lorenz_direct"])


        # Boucle sur les différents jeux de poids OWA
        for omega in omegas:

            mean_time = 0
            it = 5 # Nombre d'itérations pour moyenner le temps

            for i in range(it):

                L = []
                lambda_ = [omega[k]-omega[k+1] for k in range(p-1)]+[omega[p-1]]
                print(f"omega {omega}, lambda {lambda_}")

                try:
                            
                    start = time.time()
                    res = methode_directe(n,p,W,w,v,lambda_,L)
                    elapsed = time.time() - start

                    
                    t_dir, nb_lorenz_dir = elapsed, res
                    mean_time += elapsed
                    print(f"itération {i} mean_time : ",mean_time)
                
                except Exception as e:
                    print("Erreur : ",e)

                    t_dir, nb_lorenz_dir = None, None
        

            # On fait la moyenne sur les différentes itérations
            mean_time = mean_time/it

            #Sauvegarde
            writer.writerow([n,p,omega,mean_time,nb_lorenz_dir])

            results.append({
                "n" : n,
                "p" : p,
                "omega" : omega,
                "t_direct" : mean_time,
                "lorenz_dir" : nb_lorenz_dir

            })

    return res
    

# ============================================
# Lecture et traitement des résultats
# ============================================

def read_results(filename):
    """
    Lit un fichier CSV de résultats et retourne une liste de dictionnaires
    contenant :
    - n : nombre d'objets
    - p : nombre d'objectifs
    - time : temps de calcul
    - nb_lorenz : nombre de vecteurs de Lorenz
    """


    results = []

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            results.append({
                "n": int(row["n"]),
                "p": int(row["p"]),
                "time": float(row["time_direct"]) if row["time_direct"] != "" else None,
                "nb_lorenz": int(row["nb_lorenz_direct"]) if row["nb_lorenz_direct"] != "" else None
            })

    return results



def group_by_p(results):
    """
    Regroupe les résultats par nombre d'objectifs p.
    Ignore les entrées pour lesquelles le temps est None.
    """

    data = {}
    for r in results:
        p = r["p"]
        if r["time"] is None:
            continue
        data.setdefault(p, []).append(r)
    return data


# ============================================
# Tracé des courbes de performance
# ============================================

def plot(filename):
    """
    Trace le temps de calcul de la méthode directe en fonction du nombre
    d'objets n pour différentes valeurs de p.
    Le graphique est sauvegardé dans un fichier PNG.
    """

    res = read_results(filename)
    data_by_p = group_by_p(res)

    plt.figure()

    for p, data in sorted(data_by_p.items()):
        # trier par n pour une courbe propre
        data = sorted(data, key=lambda x: x["n"])

        n_vals = [r["n"] for r in data]
        times = [r["time"] for r in data]

        plt.plot(n_vals, times, marker='o', label=f"p = {p}")

    plt.xlabel("Nombre d'objets (n)")
    plt.ylabel("Temps (secondes)")
    plt.title("Temps de calcul - Méthode directe")
    plt.legend()
    plt.grid(True)
    plt.yscale("log")   # TRÈS recommandé vu l’explosion des temps
    plt.savefig("results/time_methode_directe.png")
    plt.show()



