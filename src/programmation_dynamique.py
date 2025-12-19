from utils import est_domine, additionner_valeurs, filtre_pareto, est_lorenz_dominee

def programmation_dynamique(objets, capacite_max):

    nb_objectifs = len(objets[0]['valeurs'])
    vecteur_nul = tuple([0] * nb_objectifs)
    
    # Initialisation de la table
    solution_initiale = {
        'valeurs': vecteur_nul,
        'objets_choisis': []
    }
    
    # Table vide + initialisé pour le poids 0
    table_actuelle = [[] for _ in range(capacite_max + 1)]
    table_actuelle[0] = [solution_initiale]

    print(f"Calcul en cours avec {len(objets)} objets...")

    # Itération sur les objets
    for idx, objet in enumerate(objets):
        w_obj = objet['w']
        valeurs_obj = objet['valeurs']
        id_obj = objet['id']
        
        # Cas de base ou on prend pas l'objet i, donc on copie la table actuelle
        # OPT(w, i-1)
        nouvelle_table = [liste[:] for liste in table_actuelle]
        
        # On parcours la colonne pour l'objet i
        for w in range(capacite_max + 1):
            # Si on peut prendre l'objet i
            if w >= w_obj:
                # On récupère OPT(w - w_obj, i-1)
                solutions_precedentes = table_actuelle[w - w_obj]
                
                # Pour toutes les solutions dans OPT(w - w_obj, i-1)
                for sol in solutions_precedentes:
                    # On additione les valeurs de l'objet i
                    # valeurs_obj + OPT(w - w_obj, i-1)
                    nouvelles_valeurs = additionner_valeurs(sol['valeurs'], valeurs_obj)
                    
                    # On met à jour les objets choisis et la solution
                    nouveaux_objets = sol['objets_choisis'] + [id_obj]
                    nouvelle_sol = {
                        'valeurs': nouvelles_valeurs,
                        'objets_choisis': nouveaux_objets
                    }
                    
                    nouvelle_table[w].append(nouvelle_sol)
                
                # Appliquer le filtre de Pareto
                nouvelle_table[w] = filtre_pareto(nouvelle_table[w])
        
        table_actuelle = nouvelle_table

    toutes_solutions = []
    for liste_sols in table_actuelle:
        toutes_solutions.extend(liste_sols)
        
    return filtre_pareto(toutes_solutions)

def filtre_lorenz(solutions_pareto):
    solutions_finales = []
    
    for sol_a in solutions_pareto:
        dominee = False
        
        for sol_b in solutions_pareto:
            if sol_a == sol_b: continue
            
            if est_lorenz_dominee(sol_a['valeurs'], sol_b['valeurs']):
                dominee = True
                break
        
        if not dominee:
            if sol_a not in solutions_finales:
                solutions_finales.append(sol_a)
            
    return solutions_finales