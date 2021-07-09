# We import python modules
# numpy : a mathematical function that is very useful!
import numpy as np
import os
# graphs is for the size of the graphs
from graphs import *
from exo import *
from utils import *


def get_files_directory(directory, pattern="AFC", pattern2="AX", pattern3="Oddity"):
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

    # This is the initializing function of any exercise
    # It has only one argument, called "path"
    def __init__(self, base):
        # Here we define the shared attributes of all the students
        # They all have a path, the base of the directory
        self.base = base
        # We search for the directory that contains 
        # the logfiles since they all have logfiles
        self.find_log_dir()
        # All the students have names that we want to retrieve
        self.get_name()
        # All students have done exercises
        self.create_exos()
        
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
                 ("AX", AX),
                 ("Oddity", Oddity)]
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
        # for each exercise in the class Exo
        for exo in self.exos:
            # if the key is designed as "Vowel" and 
            # the exercise is an AX (subclass of Exo)
            if key == "Vowel" and isinstance(exo, AX):
                # we continue the loop and 
                # don't treat the exercise
                continue
            # else/if the key is "Vowel" and 
            # the exercise is an Oddity
            elif key == "Vowel" and isinstance(exo, Oddity):
                # we continue the loop and 
                # don't treat the exercise
                continue
            # if it's none of them
            else:
                # we add to the empty list the 
                # results of their criteria by key
                list_dicos.append(exo.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    
    
    # This function is very useful to avoid making
    # different functions for each particular case.
    # Whether the directory has 0, 1 or 2 "logFiles"
    # files, the function will continue digging,
    # exploring, until it finds the logfiles.
    def find_log_dir(self):
        if self.base[-1] != "/":
            self.base += "/"
        continue_exploring = True
        # the current directory is the path, or 
        # the base given when calling the function.
        current_dir = self.base
        # While we haven't reached the end of the exploration
        while continue_exploring:
            # We retrieve the tree view under the file
            extended_list = os.listdir(current_dir)
            # We check the number of elements in the 
            # tree view, if there is only one element
            if len(extended_list) == 1 and os.path.isdir(current_dir + extended_list[0]):
                # We check that it is a file before proceeding. We
                # concatenate the path of the new file with the
                # previous file so that the exploration can resume.
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
        dico = self.criteria_by_key(key, criteria)
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))[:,0]
        sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_chart(labels[sel_arr], values[sel_arr], title)
            
    def hist_all_exos(self, key, criteria, title, xlabel, ylabel, xrotation=None, yrotation=None):
        dico = self.criteria_by_key(key, criteria)
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))[:,0]
        # This line makes it possible to only
        # display the keys for which at least
        # one mistake has been done by the student
        sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_hist(labels[sel_arr], values[sel_arr], title, xlabel, ylabel, xrotation=xrotation, yrotation=yrotation)
            
    
    def plot_table_by_key(self, key, xscale=0.5, yscale=4, at_least=0.5):
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
            #for val in values:
            #for i, val in enumerate(criteria['NbErreurs']):
            #for i, val in values:
            for i in range(len(values)):
                if i >= at_least:
                    row_values.append(values[i])
                    #row_labels.append(labels[i])
                    

           # for val in values:
               # if val >= at_least:
                  #  row_values.append(val)
                   # row_values = values
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
            #sel_arr = values != 0
            #if np.all(sel_arr == False):
               # pass
            #else:
            plot_table(row_labels, criterias, row_values.T, xscale=xscale, yscale=yscale)
        
        
    def group_bar_hist(self, criterias, title, ylabel, xrotation=None, key="Vowel"):
        # we create an empty list
        values_arr = []
        # for a criteria is the list of criterias
        for criteria in criterias:
            # we create a dictionary thanks to criteria_by_key
            dico = self.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            # We add the proportion, the first 
            # element is divided by the second
            values_arr.append(values[:,0] / values[:,1])
        
        fig, ax = plt.subplots()
        x = np.arange(labels.shape[0])    # the x locations for the labels
        width = (1 / len(criterias)) - 0.1 # the width of the bars
        
        offsets = np.arange(-0.5, 0.5, width) + 0.30
        for i, values in enumerate(values_arr):
            # We skip the occurrences
            ax.bar(x + offsets[i], values, width, label=criterias[i])
        font1 = {'family':'serif','color':'blue','size':50}
        font2 = {'family':'serif','color':'blue','size':30}
        ax.set_title(title, font1)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(title="Criteria:")
        plt.ylabel(ylabel, font2)
        ax.autoscale_view()
        if xrotation:
            plt.tick_params(axis='x', rotation=xrotation)
        plt.show()

        
    def plot_criteria_by_date(self, key, criteria, title, xlabel, ylabel, xrotation=None):
        # We create two empty dictionaries in order
        # to retrieve the dictionaries for all the 
        # exercises and keep aside the dates.
        dicos = []
        dates = []
        for exo in self.exos:
            # If the exercise is an Oddity or an AX, the function 
            # will not treat them. As a reminder, these exercises do 
            # not have vowels. As we greatly recommend using this 
            # function with the key "Vowel", we create a condition: 
            # if the exercise identifies as AX or Oddity, we move on.
            if isinstance(exo, Oddity) or isinstance(exo, AX):
                continue
            # Otherwise, we append to the dicos
            # the information retrieved.
            dicos.append(exo.criteria_by_key(key, criteria))
            dates.append(exo.date)
            
        # We sort the dicos by date 
        dates, dicos = zip(*sorted(zip(dates, dicos)))
        
        # we get all the unique keys in the dicos
        uniques = set(k for dico in dicos for k in dico.keys())
        
        # Now we create an array to be plotted for each key
        values_dico = {}
        # for each unique key
        for k in uniques:
            # we create an empty list which will be filled 
            # with the k values, k being in 'uniques'
            values_dico[k] = []
            # We go over all dates
            for i in range(len(dates)):
                # if the key is inside the dico for the current exo, 
                if k in dicos[i].keys():
                    # we add it to values_dico
                    values_dico[k].append(dicos[i][k][0] / dicos[i][k][1])
                # if this key is not present in the exo, 
                else:
                    # then the criteria value is 0
                    values_dico[k].append(0)
        for k, v in values_dico.items():
            plt.plot(v, label=k, marker='8', ms=15)
            plt.tick_params(axis='x', rotation=90)
            plt.xticks(ticks=range(len(dates)), labels=dates)
            plt.legend()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            print(k)
            plt.show()
