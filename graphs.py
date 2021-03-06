import matplotlib.pyplot as plt
import numpy as np
from exo import *


def plot_chart(labels, values, title):
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.axis('equal')  
    plt.title(title)
    plt.show()
    
    
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



