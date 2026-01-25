from utils import read_data, est_domine, calcul_lorenz
from programmation_dynamique import programmation_dynamique, filtre_lorenz

if __name__ == "__main__":
    mes_objets = read_data('../data/2KP200-TA-0.dat', nb_objets_max=20, nb_objectifs=3)
    W = sum(i['w'] for i in mes_objets) // 2

    #---------------------Programmation Dynamique ---------------------#
    
    # Phase 1 : Pareto
    points_pareto = programmation_dynamique(mes_objets, W)
    
    # Phase 2 : Lorenz
    points_lorenz = filtre_lorenz(points_pareto)
    
    print(f"\nNombre de points Pareto : {len(points_pareto)}")
    print(f"Nombre de points Lorenz : {len(points_lorenz)}")
    
    print("\n--- Échantillon des points Lorenz non dominés ---")
    for i, v in enumerate(points_lorenz[:10]):
        print(f"Point {i+1} : Objectifs {v} | Lorenz {calcul_lorenz(v)}")