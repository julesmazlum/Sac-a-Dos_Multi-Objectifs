# Récupère les instances depuis un fichier .dat
def data(file_name):
    """
    Lit un fichier contenant des instances et retourne une liste de dictionnaires.
    Chaque instance est composée :
    - d'un poids (weight)
    - d'une liste d'objectifs (objectives)
    Les lignes commençant par 'c' sont ignorées (commentaires).
    """
    global instances 
    instances = [] # Liste qui contiendra toutes les instances lues dans le fichier
    
    n = None

    with open(file_name, "r") as f:
        for line in f:

            # Ignore les lignes vides ou les commentaires
            if not line or line.startswith("c"):
                continue

            # Si la ligne correspond à une instance
            if line.startswith("i"): 
                parts = line.split()
                weight = int(parts[1])
                objectives = list(map(int, parts[2:]))


                # Ajoute l'instance sous forme de dictionnaire
                instances.append({
                    "weight" : weight,
                    "objectives" : objectives
                })

    return instances


# Sélectionne un sous-ensemble d'instances avec n objets et p objectifs
def instances_n_p(instances,n,p):
    """
    Calcule un sous-ensemble d'instances contenant :
    - n objets
    - p objectifs par objet

    Retourne :
    - Wi : liste des poids des n instances
    - vi : liste des vecteurs d'objectifs tronqués à p valeurs
    """

    instances_n_p = [(inst["weight"],inst["objectives"][:p])
    for inst in instances[:n]]

    Wi= [w for w,_ in instances_n_p]
    vi = [v for _,v in instances_n_p]

    return Wi, vi
