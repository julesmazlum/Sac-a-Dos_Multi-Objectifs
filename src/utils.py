def read_data(nom_fichier, nb_objets_max=20, nb_objectifs=3):
    """
    Prend un fichier, retourne une liste d'objets avec poids et valeurs objectifs.
    [{'id': 1, 'w': 8, 'valeurs': (16, 17, 18)}, 
    {'id': 2, 'w': 18, 'valeurs': (5, 16, 17)}, ... ]
    """
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

def est_domine(v_a, v_b):
    meilleur_partout = True
    for i in range(len(v_a)):
        if v_b[i] < v_a[i]:
            meilleur_partout = False
            break
            
    strictement_meilleur = False
    for i in range(len(v_a)):
        if v_b[i] > v_a[i]:
            strictement_meilleur = True
            break
            
    return meilleur_partout and strictement_meilleur

def filtre_pareto(liste_vecteurs):
    solutions_propres = []
    
    for v_a in liste_vecteurs:
        est_dominee = False
        for v_b in liste_vecteurs:
            if v_a == v_b: continue
            if est_domine(v_a, v_b):
                est_dominee = True
                break 
        
        if not est_dominee and v_a not in solutions_propres:
            solutions_propres.append(v_a)
                
    return solutions_propres

def calcul_lorenz(vecteur):
    v_trie = sorted(list(vecteur))
    v_lorenz = []
    somme = 0
    for val in v_trie:
        somme += val
        v_lorenz.append(somme)
    return tuple(v_lorenz)

def est_lorenz_dominee(v_a, v_b):
    return est_domine(calcul_lorenz(v_a), calcul_lorenz(v_b))