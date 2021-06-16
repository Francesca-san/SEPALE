# We import python modules
# numpy : a mathematical function that is very useful!
import numpy as np
import os
# graphs is for the size of the graphs
from graphs import *
from exo import *
from utils import *


def get_files_directory(directory, pattern="AFC", pattern2="AX"):
    if directory[-1] != "/":
        directory += "/"
    return [directory + file for file in os.listdir(directory) if  pattern in file]

# We define a new class called "Student"
class Student:
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Student)
    '''

    def __init__(self, base):
        # Here we define the shared attributes of all the students
        # They all have a path, the base of the directory
        self.base = base
        # We search for the directory that contains the logfiles
        # since they all have logfiles
        self.find_log_dir()
        # All the students have names that we want to retrieve
        self.get_name()
        #self.file = file 
        # All students have done exercises
        self.create_exos()
        #self.arr = []
        
    def get_name(self):
        # Parse the base path to get the names
        tmp = self.base.split('/')[-2]
        fullname = tmp.split('_')[0]
        splitted_name = fullname.split(' ')
        # If only one surname
        if len(splitted_name) == 2:
            name, surname = splitted_name
        # If more than one
        else:
            name = splitted_name[0]
            surname = " ".join(e for e in splitted_name[1:])
        self.name = name
        self.surname = surname
        
    def create_exos(self):
        # We create tuples which associate a pattern
        # in a file to a specific type of "Exo", 2AFC or 5AFC.
        # There are two elements in this association:
        # a pattern (ex: "2AFC"), and the Class it belongs to (ex: AFC2)
        assos = [("2AFC", AFC2),
                 ("5AFC", AFC5),
                 ("AX", AX)]
        exos = []
        # For each pattern and class (cl) in the association
        for pattern, cl in assos:
            # We retrieve the paths of the files in the student's 
            # directory in which we can find the pattern
            path_list = get_files_directory(self.directory, pattern=pattern)
            # For each of these paths
            for exo_path in path_list:
                # We associate the path to the type of exercise, to a class
                exo = cl(exo_path)
                # We add this association to a list of exercises
                exos.append(exo)
        # Once the list of exercises is implemented
        # it is associated to its student
        self.exos = exos
        
    def criteria_by_key(self, key, criteria):
        res = {}
        # For each exercise, we retrieve the dictionaries
        list_dicos = []
        for exo in self.exos:
            list_dicos.append(exo.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    

    def find_log_dir(self):
        if self.base[-1] != "/":
            self.base += "/"
        continue_exploring = True
        current_dir = self.base
        # While we haven't reached the end of the exploration
        while continue_exploring:
            # We retrieve the tree view under the file
            extended_list = os.listdir(current_dir)
            # We check the number of elements in the tree view
            # If there is only one element
            if len(extended_list) == 1 and os.path.isdir(current_dir + extended_list[0]):
                # We check that it is a file before proceeding.
                # We concatenate the path of the new file with
                # the previous file so that the exploration can resume.
                current_dir = current_dir + extended_list[0] + '/'
                continue_exploring = True  
            # If there are several elements
            else:
                # We check that those are files
                for element in extended_list:
                    if not os.path.isfile(current_dir + element):
                        # If not, then an error message is raised
                        raise Exception("Wait, this is not a file!")
                # Otherwise, the exploration stops
                continue_exploring = False
        # The directory becomes the current directory
        self.directory = current_dir
    
    def chart_all_exos(self, key, criteria, title):
        for exo in self.exos:
            dico = exo.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))[:,0]
            print(exo.path)
            plot_chart(labels, values, title)
            
    def hist_all_exos(self, key, criteria, title, xlabel, ylabel, xrotation=None, yrotation=None):
        for exo in self.exos:
            dico = exo.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))[:,0]
            
            sel_arr = values != 0
            if np.all(sel_arr == False):
                pass
            else:
                print(exo.path)
                plot_hist(labels[sel_arr], values[sel_arr], title, xlabel, ylabel, xrotation=xrotation, yrotation=yrotation)

    
    def plot_table_by_key(self, key, xscale=0.5, yscale=4):
        criterias = np.array(["Repetitions", "NbErreurs",  "Response Time"])
        row_values = []
        # At the beginning we don't know
        # the labels of the lines
        row_labels = None
        for criteria in criterias:
            dico = average_dico(self.criteria_by_key(key, criteria))
            # If we don't know the labels of the lines
            # at this round, the labels of the lines
            # are the ones we've just retrieved
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            
            if row_labels is None:
                row_labels = labels
            # If we know them, we check that those that
            # we've just retrieved are the same
            else:
                for i in range(len(labels)):
                    if row_labels[i] != labels[i]:
                        # If they are not the same, a 
                        # message of error is raised
                        raise Exception("Uncompatible labels")
            # We add the lines of the table
            row_values.append(values)
        row_values = np.array(row_values)
        plot_table(row_labels, criterias, row_values.T, xscale=xscale, yscale=yscale)
        