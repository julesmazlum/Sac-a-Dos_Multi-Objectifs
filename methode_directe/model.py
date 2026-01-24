from gurobipy import *
from numpy import random
import time
from load import data


# =====================================
# Calcul du vecteur de Lorenz
# =====================================

def lorenz_vector(y):
    """
    Calcule le vecteur de Lorenz associé à un vecteur y.
    - Trie les composantes de y par ordre croissant
    - Calcule les sommes cumulées
    """

    y_sorted = sorted(y)
    L =[]
    cumul = 0
    for val in y_sorted:
        cumul += val
        L.append(cumul)
    return L

# ---------------------------
# FONCTION POUR RESOUDRE P1
# ---------------------------
def P1(n,p,W,w,v,lambda_):
    """
    Résout le problème P1 (première optimisation).
    Retourne le vecteur des objectifs y si une solution optimale est trouvée.
    """

    model = Model("P1")

    # Variables binaires x_j = 1 si l'objet j est sélectionné, 0 sinon
    x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(n)]
    
    
    # Variables continues r_k
    r= [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(p)]

    # Variables continues b_k_i >= 0 (linéarisation OWA)
    b = [[model.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"b_{k}_{i}") for i in range(p)] for k in range(p)]


    # -------------------
    # Contraintes
    # -------------------

    # Contrainte du sac à dos (capacité maximale)
    model.addConstr(quicksum(w[j]*x[j] for j in range(n)) <= W) #poids de objets <= capacité du sac

    # Contraintes de linéarisation de la fonction OWA
    for k in range(p):
        for i in range(p):
            model.addConstr(r[k] - b[k][i] <= quicksum(v[j][i]*x[j] for j in range(n)))

    
    # -------------------
    # Fonction objectif
    # -------------------
    model.setObjective(quicksum(lambda_[k]*((k+1)*r[k]-quicksum(b[k][i] for i in range(p))) for k in range(p)), GRB.MAXIMIZE)

    model.optimize()

    # -------------------
    # Récupération de la solution
    # -------------------
    if model.status == GRB.OPTIMAL:
        # Valeurs des variables x
        x_val = [x[j].x for j in range(n)]

        # Calcul du vecteur objectif y
        y_val = [sum(v[j][i]*x_val[j] for j in range(n)) for i in range(p)]
        return y_val
    else:
        return None
    


# ---------------------------
# FONCTION POUR RÉSOUDRE PL
# L = liste des vecteurs de Lorenz déjà trouvés
# ---------------------------
def PL(n,p,W,w,v,lambda_,L):
    """
    Résout le problème PL en excluant les solutions précédentes
    grâce aux vecteurs de Lorenz déjà calculés.
    """

    model = Model("PL")

    # Variables binaires de sélection des objets
    x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(n)]
    
    
    # Variables continues r_k
    r= [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(p)]

    # Variables continues b_k_i >= 0
    b = [[model.addVar(vtype=GRB.CONTINUOUS,lb=0, name=f"b_{k}_{i}") for i in range(p)] for k in range(p)]

    # Variables binaires z_s_k pour exclure les solutions précédentes
    z = [[model.addVar(vtype=GRB.BINARY, name=f"z_{s}_{k}") for k in range(p)] for s in range(len(L))]


    # -------------------
    # Contraintes
    # -------------------
    
    # Contrainte du sac à dos
    model.addConstr(quicksum(w[j]*x[j] for j in range(n)) <= W) #poids de objets <= capacité du sac

    # Contraintes de linéarisation OWA
    for k in range(p):
        for i in range(p):
            model.addConstr(r[k] - b[k][i] <= quicksum(v[j][i]*x[j] for j in range(n)))
    
    #Contraintes PL : amélioration par rapport aux points précédents
    for s, Ls in enumerate(L):
        print(f"L{s}=",Ls)
        for k in range(p):
            model.addConstr((k+1)*r[k] - quicksum(b[k][i] for i in range(p)) >= (Ls[k]+1)*z[s][k])

        # Au moins une composante doit être strictement améliorée    
        model.addConstr(quicksum(z[s]) >= 1)


    # -------------------
    # Fonction objectif
    # -------------------
    model.setObjective(quicksum(lambda_[k]*( (k+1)*r[k] - quicksum(b[k][i] for i in range(p)) ) for k in range(p)), GRB.MAXIMIZE)

    model.optimize()

    if model.status == GRB.OPTIMAL:
        x_val = [x[j].x for j in range(n)]
        y_val = [sum(v[j][i]*x_val[j] for j in range(n)) for i in range(p)]
        return y_val
    
    else:
        return None



# =====================================
# Méthode itérative : méthode directe
# =====================================
def methode_directe(n,p,W,w,v,lambda_,L):
    """
    Implémente la méthode directe :
    - Résout P1 pour obtenir une première solution
    - Puis résout PL itérativement pour trouver d'autres solutions
      non dominées selon Lorenz
    - Retourne le nombre total de vecteurs de Lorenz trouvés
    """

    # Première résolution (P1)
    y = P1(n, p, W, w, v, lambda_)
    if y is None:

        return None
        
    # Ajout du premier vecteur de Lorenz
    L.append(lorenz_vector(y))  

    print("Solution P1 :", y)
    print("Lorenz :", lorenz_vector(y))

    # Boucle itérative sur PL
    while True:
        y_new = PL(n, p, W, w, v, lambda_, L)
        if y_new is None:
            break

        # Ajout du nouveau vecteur de Lorenz trouvé
        L.append(lorenz_vector(y_new))
    
    # Retourne le nombre de solutions trouvées
    return len(L)
