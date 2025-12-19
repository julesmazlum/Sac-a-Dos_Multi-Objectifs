def read_data(nom_fichier, nb_objets_max=20, nb_objectifs=3):
    objets = []

    with open(nom_fichier, 'r') as f:
        compteur = 0
        for ligne in f:
            if ligne.startswith('i'):
                if compteur >= nb_objets_max:
                    break
                
                parties = ligne.split()
                w = int(parties[1])
                valeurs = tuple(map(int, parties[2 : 2 + nb_objectifs]))
                
                objets.append({
                    'id': compteur + 1,
                    'w': w, 
                    'valeurs': valeurs
                })
                compteur += 1
    return objets

def additionner_valeurs(v1, v2):
    return tuple(a + b for a, b in zip(v1, v2))

def est_domine(sol_a, sol_b):
    meilleur_partout = True
    for i in range(len(sol_a)):
        if sol_b[i] < sol_a[i]:
            meilleur_partout = False
            break
            
    strictement_meilleur = False
    for i in range(len(sol_a)):
        if sol_b[i] > sol_a[i]:
            strictement_meilleur = True
            break
            
    return meilleur_partout and strictement_meilleur

def filtre_pareto(liste_solutions):
    solutions_propres = []
    
    for sol_a in liste_solutions:
        est_dominee = False
        val_a = sol_a['valeurs']
        
        for sol_b in liste_solutions:
            if sol_a == sol_b: continue
            
            val_b = sol_b['valeurs']
            
            if est_domine(val_a, val_b):
                est_dominee = True
                break 
        
        if not est_dominee:
            deja_present = False
            for s in solutions_propres:
                if s['valeurs'] == val_a:
                    deja_present = True
                    break
            
            if not deja_present:
                solutions_propres.append(sol_a)
                
    return solutions_propres

def calcul_lorenz(vecteur):
    v_trie = sorted(list(vecteur))
    v_lorenz = []
    somme = 0

    for val in v_trie:
        somme += val
        v_lorenz.append(somme)
        
    return tuple(v_lorenz)

def est_lorenz_dominee(sol_a, sol_b):
    lorenz_sujet = calcul_lorenz(sol_a)
    lorenz_comp = calcul_lorenz(sol_b)
    
    return est_domine(lorenz_sujet, lorenz_comp)