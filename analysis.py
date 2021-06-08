from utils import create_dico
#['Sound File', 'Stimulus', 'Vowel', 'FirstResponse', 'Response Time', 'NbErreurs', 'Repetitions', 'date']
def with_errors(dico, key='Stimulus', at_least=1):
    result = []
    for i, val in enumerate(dico['NbErreurs']):
        if val >= at_least:
            result.append(dico[key][i])
    return result

def count_errors(dico, key='Stimulus', count_one=False):
    result = {}
    for i, val in enumerate(dico['NbErreurs']):
        if dico[key][i] not in result.keys():
            result[dico[key][i]] = 0
        if val > 0:
            if count_one:
                result[dico[key][i]] += 1
            else:
                result[dico[key][i]] += val
    return result

def count_with_criteria(dico, key='Vowel', criteria='Response Time', count_one=False):
    result = {}
    assert criteria in ['NbErreurs', 'Repetitions', 'Response Time']
    for i, val in enumerate(dico[criteria]):
        if dico[key][i] not in result.keys():
            result[dico[key][i]] = 0
        if val > 0:
            if count_one:
                result[dico[key][i]] += 1
            else:
                result[dico[key][i]] += val
    return result


def with_no_errors(dico, key='Stimulus'):
    result = []
    for i, val in enumerate(dico['NbErreurs']):
        if val == 0:
            result.append(dico[key][i])
    return result

def count_right(dico, key='Stimulus'):
    result = {}
    for i, val in enumerate(dico['NbErreurs']):
        if dico[key][i] not in result.keys():
            result[dico[key][i]] = 0
        if val == 0:
            result[dico[key][i]] += 1
    return result

def stat_exo(fichier, key="Vowel"):
    dico_exo = create_dico(fichier)
    err_dico = count_errors(dico_exo, key=key, count_one=False)
    right_dico = count_right(dico_exo, key=key)
    time_dico = count_with_criteria(dico_exo, key=key, criteria='Response Time')

    keys = set(list(err_dico.keys()) + list(right_dico.keys()))
    # Dictionnaire résultat dont chaque élément est
    # key : [attribut1, attribut2, attribut3]
    # On peut rajouter des attributs au besoin
    # attribut 1 = erreurs, attribut2 = right, attribut3 = response time mean
    res = {}
    # pour les moyennes, on initialise les compteurs à 0
    time_counters = {}
    for k in keys:
        time_counters[k] = 0
        
    for k in keys:
        if k in err_dico.keys():
            error = err_dico[k]
        else:
            error = 0
            
        if k in right_dico.keys():
            right = right_dico[k]
        else:
            right = 0
            
        if k in time_dico.keys():
            time = time_dico[k]
            # On incrémente le compteur
            time_counters[k] += 1
        else:
            time = 0
        # Pour le moment on stocke le temps total
        res[k] = [error, right, time]
    
    # On fait la moyenne pour toutes les clés
    for k in keys:
        res[k][2] /= time_counters[k]
    
    return res

def stat_mult_exo(liste_fichiers, key="Vowel"):
    # Dictionnaire résultat dont chaque élément est
    # key : [attribut1, attribut2]
    # On peut rajouter des attributs au besoin
    # attribut 1 = somme des erreurs, attribut2 = somme des bonnes réponses
    dico_res = {}
    for fichier in liste_fichiers:
        # On récupère les statistiques d'un exo
        dico_exo = stat_exo(fichier, key=key)
        # On agrège les données
        for k, v in dico_exo.items():
            # si on a déjà vu passer la clé, on ajoute
            if k in dico_res.keys():
                # on agrège le premier attribut
                dico_res[k][0] += dico_exo[k][0]
                # on agrège le second attribut
                dico_res[k][1] += dico_exo[k][1]
            else:
                # sinon, on setup avec les valeurs correspondant
                # à la clé pour l'exercice courant
                dico_res[k] = dico_exo[k]
        
    return dico_res


def print_stat_exo(dico_exo):
    print("key | errors | right | mean resp time")
    print("--------------------")
    for k, v in dico_exo.items():
        print(f"{k}   |  {v[0]}   | {v[1]} | {v[2]}")
