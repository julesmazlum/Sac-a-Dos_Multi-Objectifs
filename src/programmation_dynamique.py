from utils import est_domine, additionner_valeurs, filtre_pareto, est_lorenz_dominee

def programmation_dynamique(objets, capacite_max):
    nb_objectifs = len(objets[0]['valeurs'])
    vecteur_nul = tuple([0] * nb_objectifs)
    
    # Table vide + initialisé pour le poids 0
    table_actuelle = [[] for _ in range(capacite_max + 1)]
    table_actuelle[0] = [vecteur_nul]

    print(f"Calcul Pareto en cours ({len(objets)} objets)...")

    # Itération sur les objets
    for objet in objets:
        print(f"  - Traitement de l'objet {objet['id']} (poids={objet['w']}, valeurs={objet['valeurs']})")
        w_obj = objet['w']
        valeurs_obj = objet['valeurs']
        
        # Cas de base ou on prend pas l'objet i, donc on copie la table actuelle
        # OPT(w, i-1)
        nouvelle_table = [liste[:] for liste in table_actuelle]
        
        # On parcours la colonne pour l'objet i, des qu'on peut l'ajouter
        for w in range(w_obj, capacite_max + 1):
            # On récupère OPT(w - w_obj, i-1)
            solutions_precedentes = table_actuelle[w - w_obj]
            
            # Pour toutes les solutions dans OPT(w - w_obj, i-1)
            for v_prev in solutions_precedentes:
                # valeurs_obj + OPT(w - w_obj, i-1)
                nouveaux_vecteurs = additionner_valeurs(v_prev, valeurs_obj)
                # On met à jour la solution
                nouvelle_table[w].append(nouveaux_vecteurs)
            
            # Filtrage
            nouvelle_table[w] = filtre_pareto(nouvelle_table[w])
        
        table_actuelle = nouvelle_table

    # Collecte de tous les points Pareto de toutes les capacités
    toutes_solutions = []
    for liste_sols in table_actuelle:
        toutes_solutions.extend(liste_sols)
        
    return filtre_pareto(toutes_solutions)

def filtre_lorenz(solutions_pareto):
    solutions_finales = []

    for v_a in solutions_pareto:
        dominee = False

        for v_b in solutions_pareto:
            if v_a == v_b: continue

            if est_lorenz_dominee(v_a, v_b):
                dominee = True
                break
                
        if not dominee:
            solutions_finales.append(v_a)
    return solutions_finales