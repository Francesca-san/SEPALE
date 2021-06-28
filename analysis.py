from utils import create_dico
#['Sound File', 'Stimulus', 'Vowel', 'FirstResponse', 'Response Time', 'NbErreurs', 'Repetitions', 'date']

# This function displays the keys for which an error was made. We
# can notice that a key is already specified, this means that you
# can modify it when you call the function, but if you do not 
# specify it, then the key will automatically be "Stimulus".
# Same goes for the attributes at_least.
def with_errors(dico, key='Stimulus', at_least=1):
    # we create an empty list
    result = []
    # for the variables i and val
    # in the dictionary "NbErreurs"
    for i, val in enumerate(dico['NbErreurs']):
        # if the value is greater or equal
        # to the value of at_least
        if val >= at_least:
            # we add the value to the dictionary
            result.append(dico[key][i])
    # we return the result
    return result

# This function counts the errors
def count_errors(dico, key='Stimulus', count_one=False):
    # we create an empty dictionary
    result = {}
    # for the variables i and val
    # in the dictionary "NbErreurs"
    for i, val in enumerate(dico['NbErreurs']):
        # if the key is not in result.key
        if dico[key][i] not in result.keys():
            # the value 0 is given to the dictionary
            result[dico[key][i]] = 0
        # if value is greater than 0
        if val > 0:
            # and count_one = True
            if count_one:
                # then we only add 1 to the 
                # dictionary, no matter the value
                result[dico[key][i]] += 1
            # if count_one = False
            else:
                # we add the value to the dictionary
                result[dico[key][i]] += val
    return result

# this functions counts a criterion per vowel
def count_with_criteria(dico, key='Vowel', criteria='Response Time', count_one=False):
    # we create an empty dictionary
    result = {}
    # we define what a criterion can be
    assert criteria in ['NbErreurs', 'Repetitions', 'Response Time']
    # for the variables i and val
    # in the dictionary of criteria
    for i, val in enumerate(dico[criteria]):
        # if the key is not in result.key
        if dico[key][i] not in result.keys():
            # the value 0 is given to the dictionary
            result[dico[key][i]] = 0
        # if value is superior to 0
        if val > 0:
            # and count_one = True
            if count_one:
                # then we only add 1 to the 
                # dictionary, no matter the value
                result[dico[key][i]] += 1
            # if count_one = False
            else:
                # we add the value to the dictionary
                result[dico[key][i]] += val
    return result

# this function shows the words for which no error was made.
def with_no_errors(dico, key='Stimulus'):
    # we create an empty list
    result = []
    # for the variables i and val
    # in the dictionary "NbErreurs"
    for i, val in enumerate(dico['NbErreurs']):
        # if he value is strictly equal to 0
        if val == 0:
            # we add the value to the dictionary
            result.append(dico[key][i])
    return result

# this function counts the number of right answers
def count_right(dico, key='Stimulus'):
    # we create an empty dictionary
    result = {}
    # for the variables i and val
    # in the dictionary "NbErreurs"
    for i, val in enumerate(dico['NbErreurs']):
        # if the key is not in result.key
        if dico[key][i] not in result.keys():
            # the value 0 is given to the dictionary
            result[dico[key][i]] = 0
        # if he value is strictly equal to 0
        if val == 0:
            # we add the value to the dictionary
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
