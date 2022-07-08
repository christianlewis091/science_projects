import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from colorspacious import cspace_converter
import pandas as pd
import seaborn as sns

# general plot parameters
colors = sns.color_palette("rocket", 10)
colors2 = sns.color_palette("mako", 10)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5


def scatter_plot(x1, y1,
                 x2=None, y2=None,
                 x3=None, y3=None,
                 x4=None, y4=None,
                 label1 = None,
                 label2 = None,
                 label3 = None,
                 label4 = None,
                 xmin=None, xmax=None,
                 ymin=None, ymax=None,
                 title=None, xlabel=None,
                 ylabel=None,
                 savename=None,
                 size1 = None,
                 **kwargs):
    plt.scatter(x1, y1, marker='o', label='{}'.format(label1), color=colors[1], s=size1)
    if y2 is None:
        print('') # plt.scatter(x2, y2, marker='o', label='{}'.format(label2), color=colors[3], s=size1)
    else:
        plt.scatter(x2, y2, marker='o', label='{}'.format(label2), color=colors[3], s=size1)

    if y3 is None:
        print('') # nothing happens
    else:
        plt.scatter(x3, y3, marker='o', label='{}'.format(label3), color=colors[5], s=size1)

    if y4 is None:
        print('') # nothing happens
    else:
        plt.scatter(x4, y4, marker='o', label='{}'.format(label4), color=colors[7], s=size1)

    plt.legend()
    plt.title('{}'.format(title))
    if xmin == '':
        print('no specs')
    else:
        plt.xlim([xmin, xmax])
    if ymin == '':
        print('no specs')
    else:
        plt.ylim([ymin, ymax])
    plt.xlabel('{}'.format(xlabel), fontsize=14)
    plt.ylabel('{}'.format(ylabel), fontsize=14)
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/{}.png'.format(savename),
                dpi=300, bbox_inches="tight")
    plt.close()






x = [1,2,3]
y = [3,4,5]
y2 = [6,7,8]
y3 = [9,10,11]
y4 = [12,13,15]
y5 = [10,20,350]

scatter_plot(x,y, x2 = x, y2 = y2, x3 = x, y3=y3, x4 = x, y4 = y4)

plt.show()


# general plot parameters
colors = sns.color_palette("rocket", 10)
colors2 = sns.color_palette("mako", 10)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

