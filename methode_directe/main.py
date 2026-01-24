from ut import run_experiments,influence_owa,plot

if __name__ == "__main__":

    print("===== Lancement du programme =====")

    # --------------------- Méthode directe --------------------- #
    # Décommenter si nécessaire
    
    #print(">> Exécution de la méthode directe sur les instances...")
    #run_experiments("../data/2KP200-TA-0.dat")
    #print(">> Fin des expériences de la méthode directe")

    # --------------------- Influence des poids OWA --------------------- #
    # Décommenter si nécessaire


    print(">> Étude de l'influence des poids OWA...")
    influence_owa("../data/2KP200-TA-0.dat")
    print(">> Fin de l'étude OWA")

    # --------------------- Tracé des résultats --------------------- #
    # Décommenter si nécessaire


    # print(">> Génération des graphiques...")
    # plot("results/res_methode_directe.csv")
    # print(">> Graphiques générés")

    print("===== Fin du programme =====")