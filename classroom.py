import os
import numpy as np
from exo import *
from student import Student
from datetime import timedelta
from utils import merge_list_dicos, average_dico, merge_dicos
from graphs import *

# We define a new class called "Classroom"
class Classroom:
    '''
    This is a description of the class, 
    If you have any problem with it
    you can always write help(Classroom)
    '''
    
    # This is the initializing function of any exercise
    # It has only one argument, called "path"
    def __init__(self, base):
        # Here we define the shared attributes of all the students
        # They all have a path, the base of the directory
        self.base = base
        # A classroom contains several students
        self.create_students()
        
    # As this function is in the __init__ function, 
    # it means that the function will start  
    # any time the class Classroom is called.        
    def create_students(self):
        # in order to avoid error message, we
        # ask the function to add a slash 
        # to the base if there is none.
        if self.base[-1] != "/":
            self.base += "/"
        # we create an empty list
        self.student_list = []
        # list_students corresponds 
        # to all the elements in base
        list_students = os.listdir(self.base)
        # for the path of a student in the list
        for student_path in list_students:
            # a student is an instance which belongs
            # to the class Student which has one attribute,
            # base (or path). The path is the base and
            # the path to the student's exercises.
            student = Student(self.base + student_path)
            self.student_list.append(student)
            
    def criteria_by_key(self, key, criteria):
        res = {}
        # For each exercise, we retrieve the dictionaries
        list_dicos = []
        # for a student in the list of students
        for student in self.student_list:
            # we add to the empty list the 
            # results of their criteria by key
            list_dicos.append(student.criteria_by_key(key, criteria))
        return merge_list_dicos(list_dicos)
    
    
    def print_names(self):
        # for a student in the list of students
        for student in self.student_list:
            # we show their name and surname
            print(student.name, student.surname, f"({len(student.exos)} exercises)")
            
            
    def plot_table_by_key(self, key, xscale=0.5, yscale=4, at_least=0, 
                          target_criteria="NbErreurs"):
        criterias = np.array(["Repetitions", "NbErreurs",  "Response Time"])
        c_index = np.where(criterias == target_criteria)[0][0]
        row_values = []
        row_labels = None
        for criteria in criterias:
            dico = average_dico(self.criteria_by_key(key, criteria))
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            if row_labels is None:
                row_labels = labels
            else:
                for i in range(len(labels)):
                    if row_labels[i] != labels[i]:
                        raise Exception("Uncompatible labels")
            row_values.append(values)
        row_values = np.array(row_values)
        selec_arr = row_values[c_index,:] >= at_least
        row_labels = row_labels[selec_arr]
        #print(row_labels.shape)
        row_values = row_values[:,selec_arr]
        #print(row_values.shape)
        plot_table(row_labels, criterias, row_values.T, xscale=xscale, yscale=yscale)
        
        
    def hist_all_exos(self, key, criteria, title, xlabel, ylabel, xrotation=None, yrotation=None, at_least=0):
        dico = average_dico(self.criteria_by_key(key, criteria))
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))
        #values = np.array(list(dico.values()))[:,0]
        # This line makes it possible to only
        # display the keys for which at least
        # one mistake has been done by the student
        sel_arr = values >= at_least
        #sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_hist(labels[sel_arr], values[sel_arr], title, xlabel, ylabel, xrotation=xrotation, yrotation=yrotation)

    def chart_all_exos(self, key, criteria, title):
        dico = average_dico(self.criteria_by_key(key, criteria))
        labels = np.array(list(dico.keys()))
        values = np.array(list(dico.values()))
        #values = np.array(list(dico.values()))[:,0]
        sel_arr = values != 0
        if np.all(sel_arr == False):
            pass
        else:
            plot_chart(labels[sel_arr], values[sel_arr], title)
            
    def group_bar_hist(self, criterias, title, ylabel, xrotation=None, key="Vowel"):
        values_arr = []
        for criteria in criterias:
            dico = self.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))
            values_arr.append(values[:,0] / values[:,1])
        #c_index = np.where(criterias == target_criteria)[0]
        #values_arr = np.array(values_arr)
        #selec_arr = values_arr[c_index,:] >= at_least
        #values_arr = values_arr[selec_arr]
        #values_arr = values_arr[:,selec_arr]
        #labels = labels[selec_arr]
        
        fig, ax = plt.subplots()
        x = np.arange(labels.shape[0])    # the x locations for the labels
        width = (1 / len(criterias)) - 0.1 # the width of the bars
        offsets = np.arange(-0.5, 0.5, width) + 0.30
        for i, values in enumerate(values_arr):
            ax.bar(x + offsets[i], values, width, label=criterias[i])
        font1 = {'family':'serif','color':'k','size':20}
        font2 = {'family':'serif','color':'k','size':15}
        ax.set_title(title, font1)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(title="Criteria:")
        plt.ylabel(ylabel, font2)
        ax.autoscale_view()
        if xrotation:
            plt.tick_params(axis='x', rotation=xrotation)
        plt.show()
            
            
    def plot_criteria_by_date(self, key, criteria, title, xlabel, ylabel, xrotation=None, days=0):
        list_exos = []
        for student in self.student_list:
            for exo in student.exos:
                if isinstance(exo, Oddity) or isinstance(exo, AX):
                    continue
                list_exos.append(exo)          
        list_exos.sort(key=lambda x: x.date)
        dicos = []
        dates = []
        current_dico = None
        current_date = None
        for exo in list_exos:
            new_cbk = exo.criteria_by_key(key, criteria)
            new_date = exo.date
            if current_dico is None and current_date is None:
                current_dico, current_date = new_cbk, new_date
            else:
                if abs((new_date - current_date).days) <= days:
                    current_dico = merge_dicos(current_dico, new_cbk)
                else:
                    dicos.append(current_dico)
                    dates.append(current_date.date())
                    current_dico, current_date = new_cbk, new_date
        dicos.append(current_dico)
        dates.append(current_date.date())        
        uniques = set(k for dico in dicos for k in dico.keys())
        values_dico = {}
        for k in uniques:
            values_dico[k] = []
            for i in range(len(dates)):
                if k in dicos[i].keys():
                    values_dico[k].append(dicos[i][k][0] / dicos[i][k][1])
                else:
                    values_dico[k].append(0)
        for k, v in values_dico.items():
            plt.plot(v, label=k, marker='o', ms=6)
            plt.tick_params(axis='x', rotation=90)
            plt.xticks(ticks=range(len(dates)), labels=dates)
            plt.legend()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()