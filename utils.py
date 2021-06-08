import numpy as np

def get_lines(path):
    f = open(path, 'r')
    # on récupère les lignes
    lines = f.readlines()
    # on ferme le fichier
    f.close()
    return lines

def create_dico(path):
    lines = get_lines(path)
    # Delete \n
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
        
    attributs = []
    for l in lines:
        attributs.append(l.split('\t'))
        
    date = attributs[0]
    keys = attributs[1]
    stats_total = attributs[-1]
    data = attributs[2:-1]
    # On supprime la ligne vide
    for i in range(len(data)):
        if len(data[i]) == 1:
            del data[i]
    numeric = ['Response Time', 'NbErreurs', 'Repetitions']
    dico = {}
    for line in data:
        for i, key in enumerate(keys):
            if key not in dico.keys():
                dico[key] = []

            if key in numeric:
                dico[key].append(float(line[i]))
            else:
                dico[key].append(line[i])
    dico["date"] = date
    for key in dico.keys():
        dico[key] = np.array(dico[key])
    return dico


def merge_list_dicos(dico_list: list):
    if len(dico_list)==0:
        return {}
    # pardon c'est pas opti
    accumulator = dico_list[0]
    for i in range(1, len(dico_list)):
        accumulator = merge_dicos(accumulator, dico_list[i])
    return accumulator

# Attention, cette fonction fait
# uniquement la somme un à un de 
# chaque valeur du tableau pour
# chaque clé
# si l'on veut rajouter une opération
# contacter le service après vente
def merge_dicos(dico1, dico2):
    res = {}
    # On s'assure que les deux dicos
    # ont des éléments de même taille
    for v1, v2 in zip(dico1.values(), dico2.values()):
        if len(v1) != len(v2):
            raise Exception("Uncompatible dicos")
    # on récupère la taille du tableau de valeurs
    all_keys = dico1.keys() | dico2.keys()
    for k in all_keys:
        # si la key est dans les deux dico, on somme
        if k in dico1.keys() and k in dico2.keys():
            res[k] = [v1 + v2 for v1, v2 in zip(dico1[k], dico2[k])]
        # si la key est uniquement dans le premier
        # on ne met que ses valeurs à lui
        elif k in dico1.keys():
            res[k] = dico1[k]
        # sinon la key est forcément uniquement
        # dans le deuxième et on update les valeurs
        else:
            res[k] = dico2[k]
    return res

def average_dico(dico, round_val=3):
    average_dico = {}
    for key, tab_value in dico.items():
        average_dico[key] = round(tab_value[0] / tab_value[1], round_val)
    return average_dico