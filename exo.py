# We import python modules
# numpy : a mathematical function that is very useful!
import numpy as np


# We define a new class called "Exo"
class Exo:
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Exo)
    '''
    # This is the initializing function of any exercise
    # It has only one argument, called "path"
    def __init__(self, path):
        # Here we define the shared attributes of all the exercises
        # They all have a path
        self.path = path
        # We can find several numeric keys in those exercises: 
        # Response time, number of mistakes, and repetitions
        self.numeric_keys = ['Response Time', 'NbErreurs', 'Repetitions']
        # All the exercises have lines that 
        # have to be taken, cleansed, and parsed
        self.get_lines()
        self.clean_lines()
        self.parse_lines()
        
    # Here we take the function get_lines that 
    # can be used on any AFC exercise. It gets the 
    # lines of the files and reads them, hence 'r'.
    def get_lines(self):
        f = open(self.path, 'r')
        # We take the lines
        self.lines = f.readlines()
        # We close the file
        f.close()
        
    # This function cleans the lines of the files
    def clean_lines(self):
        # We remove the \n that are then replaced
        # by a space. \n are line breaks.
        for i in range(len(self.lines)):
            self.lines[i] = self.lines[i].replace("\n", "")
        # If the line is empty, we delete it
        # We maka a list which contains all the 
        # empty lines (= to_delete.append(i))
        to_delete = []
        for i in range(len(self.lines)):
            if len(self.lines[i]) == 0:
                to_delete.append(i)
        # then we delete (del) what has been
        # added in to_delete
        for i in to_delete:
            del self.lines[i]   
        
    # We parse the lines so as to assign attributes to lines    
    def parse_lines(self):
        attributs = []
        # We separate lines according to the tabulation
        for l in self.lines:
            attributs.append(l.split('\t'))
        # The date is the first line -> 0
        self.date = attributs[0]
        # The keys are the second line --> 1
        self.keys = np.array(attributs[1])
        # The data is to be found from the third
        # line (2) to the penultimate (-1)
        data = attributs[2:-1]
        # The last line is the number of mistakes
        # and repetitions --> stats_total
        self.stats_total = attributs[-1]
        columns = []
        for j, k in enumerate(self.keys):
            if k in self.numeric_keys:
                columns.append(np.array([float(data[i][j]) for i in range(len(data))]))
            else:
                columns.append(np.array([data[i][j] for i in range(len(data))]))
        # We have defined the content of the columns, now we have 
        # to indicate that it belongs to class Exo, hence 'self'
        self.columns = columns
        # Pour ne pas perdre ses clés !
        self.key_to_index = {}
        for i, k in enumerate(self.keys):
            self.key_to_index[k] = i
        
    def display(self):
        # on parcours les keys
        for i in range(self.keys.shape[0]):
            print(f'{self.keys[i]} {self.columns[i]}')

    
    def criteria_by_key(self, key, criteria, zeros=False):
        if key not in self.keys:
            raise Exception('Key not in my keys !')
        if criteria not in self.keys:
            raise Exception('Criteria not in my keys !')
        #labels, values = exo.criteria_by_key(key, criteria)
        # We retrieve the index number of the key/column
        k_index = self.key_to_index[key]
        # We retrieve the index number of the criteria/column
        c_index = self.key_to_index[criteria]
        # We retrieve the columns
        key_column = self.columns[k_index]
        criteria_column = self.columns[c_index]
        dico = {}
        # For each key, we keep aside its 
        # value and we count the number of 
        # times we come across it.
        # dico[key] -> [valeur_critère, compteur d'occurences]
        for i, k in enumerate(key_column):
            value = criteria_column[i]
            if k not in dico.keys():
                dico[k] = [value, 1]
            else:
                dico[k] = [dico[k][0] + value, dico[k][1] + 1]
        # We return the dictionary
        return dico
    
        
# We define a specific type of exercise: the 2AFC
class AFC2(Exo):
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(AFC2)
    '''
    # This is a specific attribute of AFC2 which lists 
    # the keys that contain numeric quantities
    
    # This is the initializing function of the exercise
    # It has only one argument, called "path"
    def __init__(self, path):
        # Here, we define the attributes that are shared
        # by the AFC2 exercises, they all have a path
        super().__init__(path)

        
# We define a specific type of exercise: the 5AFC
class AFC5(Exo):
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(AFC5)
    '''
    # This is the initializing function of the exercise
    # It has only one argument, called "path"
    def __init__(self, path):
        # Here, we define the attributes that are shared
        # by the AFC2 exercises, they all have a path
        super().__init__(path)
        
# We define a new class called "AX"
class AX(Exo):
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(AX)
    '''
    # This is the initializing function of any exercise
    # It has only one argument, called "path"
    def __init__(self, path):
        # Here we define the shared attributes of all the exercises
        # They all have a path
        super().__init__(path)
        
        
    def parse_lines(self):
        attributs = []
        # We separate lines according to the tabulation
        for l in self.lines:
            attributs.append(l.split('\t'))
        # The date is the first line -> 0
        date = attributs[0]
        # The keys are the second line --> 1
        self.keys = np.array(['Sound File', 'Stimulus','Response Time', 'NbErreurs', 'Repetitions'])
        # The data is to be found from the third
        # line (2) to the antepenultimate (-2) (empty line at end)
        data_tmp = attributs[2:-2]
        data = []
        for l in data_tmp:
            # splitting soudfile string
            sf = l[0]
            splitted = sf.split('-')
            sleft = splitted[0].split('_')
            sright = splitted[1].split('_')
            vs = sleft[1] + " vs " + sright[1]
            # do not take care of the three
            # following columns
            data.append([sf, vs, l[4], l[5], l[6]])
        # The last line is the number of mistakes
        # and repetitions --> stats_total
        stats_total = attributs[-1]
        columns = []
        for j, k in enumerate(self.keys):
            if k in self.numeric_keys:
                columns.append(np.array([float(data[i][j]) for i in range(len(data))]))
            else:
                columns.append(np.array([data[i][j] for i in range(len(data))]))
        self.columns = columns
        # Pour ne pas perdre ses clés !
        self.key_to_index = {}
        for i, k in enumerate(self.keys):
            self.key_to_index[k] = i

# We define a new class called "Oddity"
class Oddity(Exo):
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Oddity)
    '''
    
    def __init__(self, path):
        # Here we define the shared attributes of all the exercises
        # They all have a path
        super().__init__(path)
        
    def parse_lines(self):
        attributs = []
        # We separate lines according to the tabulation
        for l in self.lines:
            attributs.append(l.split('\t'))
        # The date is the first line -> 0
        date = attributs[0]
        # The keys are the second line --> 1
        self.keys = np.array(['Sound File', 'Stimulus','Response Time', 'NbErreurs', 'Repetitions'])
        # The data is to be found from the third
        # line (2) to the antepenultimate (-2) (empty line at end)
        data_tmp = attributs[2:-2]
        data = []
        for l in data_tmp:
            # splitting soudfile string
            sf = l[0]
            #re.split = ('-|, _', sf)
            #sleft = re.split[0]
            #smiddle = re.split[1]
            #sright = re.split[2]
            #vs = sleft[1] + " vs " + smiddle [1] + " vs " + sright[0]
            splitted = sf.split('-')
            sleft = splitted[0].split('_')
            smiddle = splitted[1].split('_')
            sright = splitted[2].split('_')
            vs = sleft[1] + " vs " + smiddle [1] + " vs " + sright[1]
            #print(vs)
            # do not take care of the three
            # following columns
            data.append([sf, vs, l[5], l[6], l[7]])
        # The last line is the number of mistakes
        # and repetitions --> stats_total
        stats_total = attributs[-1]
        columns = []
        for j, k in enumerate(self.keys):
            if k in self.numeric_keys:
                columns.append(np.array([float(data[i][j]) for i in range(len(data))]))
            else:
                columns.append(np.array([data[i][j] for i in range(len(data))]))
        self.columns = columns
        #print(data)
        # Pour ne pas perdre ses clés !
        self.key_to_index = {}
        for i, k in enumerate(self.keys):
            self.key_to_index[k] = i
            