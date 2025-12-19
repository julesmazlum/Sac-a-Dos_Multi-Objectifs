from utils import read_data, est_domine, calcul_lorenz
from programmation_dynamique import programmation_dynamique, filtre_lorenz

if __name__ == "__main__":
    fichier = '../data/2KP200-TA-0.dat'

    mes_objets = read_data(fichier, nb_objets_max=20, nb_objectifs=3)
    poids_total = sum(i['w'] for i in mes_objets)
    W = poids_total // 2
    
    resultats = programmation_dynamique(mes_objets, W)
    resultats_lorenz = filtre_lorenz(resultats)
    
    print(f"\n--- Solutions Pareto Optimaux ---")
    for i, sol in enumerate(resultats):
        print(f"Solution {i+1} :")
        print(f"  - Valeurs objectifs : {sol['valeurs']}")
        print(f"  - Vecteur Lorenz    : {calcul_lorenz(sol['valeurs'])}")
        print(f"  - Objets sélectionnés : {sol['objets_choisis']}")
        print("-" * 30)

    print(f"\n\n--- Solutions de Lorenz ---")
    for i, sol in enumerate(resultats_lorenz):
        print(f"Solution {i+1} :")
        print(f"  - Valeurs objectifs : {sol['valeurs']}")
        print(f"  - Vecteur Lorenz    : {calcul_lorenz(sol['valeurs'])}")
        print(f"  - Objets sélectionnés : {sol['objets_choisis']}")
        print("-" * 30)