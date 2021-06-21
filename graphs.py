import matplotlib.pyplot as plt
import numpy as np
from exo import *

#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        #ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        #        shadow=True, startangle=90)
def plot_chart(labels, values, title):
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(title)
    plt.show()
    

    
def chart_all_exos(self, key, criteria, title):
        for exo in self.exos:
            dico = exo.criteria_by_key(key, criteria)
            labels = np.array(list(dico.keys()))
            values = np.array(list(dico.values()))[:,0]
            sel_arr = values != 0
            if np.all(sel_arr == False):
                pass
            else:
                print(exo.path)
            plot_chart(labels[sel_arr], values[sel_arr], title)
    
    
def plot_hist(labels, values, title, xlabel, ylabel, xrotation=None, yrotation=None):
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xrotation:
        plt.tick_params(axis='x', rotation=xrotation)
    if yrotation:
        plt.tick_params(axis='y', rotation=yrotation)
    plt.show()
    

    
def plot_table(row_labels, column_labels, row_values, xscale=1, yscale=1):
    if len(row_labels) != row_values.shape[0]:
        raise Exception("Invalid row label and value shapes")
    if len(column_labels) != row_values.shape[1]:
        raise Exception("Invalid column labels and value shapes")
    
    # Adding pastel shades to graph
    colors = plt.cm.Greys(np.linspace(22, 3, 1))

    # Reverse colors and text labels to display table contents with
    # color.
    colors = colors[::-1]
    #cell_text.reverse()
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    # Add a table at the bottom
    table = ax.table(cellText=row_values,
             rowLabels=row_labels,
             cellLoc='center',
             colLabels=column_labels,
             colColours=['lightgrey' for _ in range(len(column_labels))],
             rowColours=['lightgrey' for _ in range(len(row_labels))],
             loc='center')
    table.scale(xscale, yscale)
    fig.tight_layout()
    plt.show()



