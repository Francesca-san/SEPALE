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

def exo_stat(file, key="Vowel"):
    dico_exo = create_dico(file)
    err_dico = count_errors(dico_exo, key=key, count_one=False)
    right_dico = count_right(dico_exo, key=key)
    time_dico = count_with_criteria(dico_exo, key=key, criteria='Response Time')

    keys = set(list(err_dico.keys()) + list(right_dico.keys()))
    # key : [attribute 1, attribute 2, attribute 3]
    # We can add other attributes if needed
    # attribute 1 = sum of wrong answers, 
    # attribute 2 = sum of right answers, 
    # attribute 3 = mean time
    res = {}
    # for the average, we initialise the counter at 0
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
            # We increase the counter by increments
            time_counters[k] += 1
        else:
            time = 0
        # for the moment we keep aside the total time
        res[k] = [error, right, time]
    
    # We calculate the average for each key
    for k in keys:
        res[k][2] /= time_counters[k]
    
    return res

def stat_mult_exo(list_files, key="Vowel"):
    # key : [attribute 1, attribute 2]
    # attribute 1 = sum of wrong answers, attribute 2 = sum of right answers
    res_dico = {}
    for file in file:
        # We retrieve the statistics for an exercise
        exo_dico = exo_stat(file, key=key)
        # We combine the data
        for k, v in exo_dico.items():
            # If we have already encountered this key, we add the value
            if k in dico_res.keys():
                # we combine the first attribute
                res_dico[k][0] += exo_dico[k][0]
                # we combine the second attribute
                res_dico[k][1] += exo_dico[k][1]
            else:
                # If not, we set up the values corresponding
                # to the key for the current exercise
                res_dico[k] = exo_dico[k]
        
    return res_dico


def print_stat_exo(exo_dico):
    print("key | errors | right | mean resp time")
    print("--------------------")
    for k, v in exo_dico.items():
        print(f"{k}   |  {v[0]}   | {v[1]} | {v[2]}")
