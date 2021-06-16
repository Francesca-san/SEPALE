# We import python modules
import os
import numpy as np
from utils import create_dico


# We define a new class called "AX"
class AX:
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
        self.path = path
        # We can find several numeric keys in those exercises: 
        # Response time, number of mistakes, and repetitions
        self.numeric_keys = ['Response Time', 'NbErreurs', 'Repetitions']
        self.keys = ['Sound File', 'Stimulus','Response Time', 'NbErreurs', 'Repetitions']
        # All the exercises have lines that 
        # have to be taken, cleansed, and parsed
        self.get_lines()
        self.clean_lines()
        self.parse_lines()
        
    # Here we take the function get_lines that 
    # can be used on any AX exercise. It gets the 
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
            l = l.replace("\n", "")
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
        for i in range(len(data)):
            if len(data[i]) == 1:
                del data[i]
        #numeric = ['Response Time', 'NbErreurs', 'Repetitions']
        dico = {}
        for line in data:
            for i, key in enumerate(self.keys):
                if key not in dico.keys():
                    dico[key] = []
                if key in self.numeric_keys:
                    dico[key].append(float(line[i]))
                else:
                    dico[key].append(line[i])
        dico["date"] = self.date
        for key in dico.keys():
            dico[key] = np.array(dico[key])
        return dico
        
        
        
    def display(self):
        # The keys are the second line --> 1
        attributs = []
        self.keys = np.array(attributs[1])
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
        # We have defined the content of the columns, now we have 
        # to indicate that it belongs to class Exo, hence 'self'
        self.columns = columns
        # Pour ne pas perdre ses clés !
        self.key_to_index = {}
        for i, k in enumerate(self.keys):
            self.key_to_index[k] = i
        return np.array(columns)
        
    def change_key_dico(self, file_dico, new_key, old_key):
        file_dico[new_key] = file_dico.pop(old_key)
        self.file_dico = file_dico
        return file_dico
    