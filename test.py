import annote
from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

x = range(10)
y = range(10)
annotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

MAX_WIDTH= 10
MAX_HEIGHT= 7
graph_title= "Recommended Stocks"

x= [.3, .4, .2, .2, .35, .3]
y= [.8, .2, .95, .1, .25, .4]
annotes= ["GOOG", "DISCA", "GE", "YHOO", "AA", "DELL"]
figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
title(graph_title, size='small')
scatter([.2], [.1], c='k', s=60)
scatter(x,y, c='g', marker='^', s=60, alpha=.3)
af =  annote.AnnoteFinder(x,y, annotes)
connect('button_press_event', af)
scatter(.4, 1, c='g', s=60)
show()



















"""Produce custom labelling for a colorbar.
http://matplotlib.sourceforge.net/examples/pylab_examples/colorbar_tick_labelling_demo.html
Contributed by Scott Sinclair
""

import matplotlib.pyplot as plt
import numpy as np

from pylab import *
from numpy import outer
from numpy.random import randn




# Make plot with vertical (default) colorbar
fig = plt.figure()
ax = fig.add_subplot(111)

data = np.clip(randn(250, 250), -1, 1)

cax= plot(data)
#cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Gaussian noise with vertical colorbar')

# Add colorbar, make sure to specify tick locations to match desired ticklabels
cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
cbar.ax.set_yticklabels(['< -1', '0', '> 1'])# vertically oriented colorbar
plt.show()
""
# Make plot with horizontal colorbar
fig = plt.figure()
ax = fig.add_subplot(212)

data = np.clip(randn(250, 250), -1, 1)

cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Gaussian noise with horizontal colorbar')

cbar = fig.colorbar(cax, ticks=[-1, 0, 1], orientation='horizontal')
cbar.ax.set_xticklabels(['Low', 'Medium', 'High'])# horizontal colorbar

plt.show()




""
rc('text', usetex=False)
a=outer(arange(0,1,0.01),ones(10))
figure(figsize=(10,5))
subplots_adjust(top=0.8,bottom=0.05,left=0.01,right=0.99)
maps=[m for m in cm.datad if not m.endswith("_r")]
maps.sort()
l=len(maps)+1

for i, m in enumerate(maps):
	print m
	subplot(1,l,i+1)
	axis("off")
	imshow(a,aspect='auto',cmap=get_cmap(m),origin="lower")
	title(m,rotation=90,fontsize=10)
	savefig("colormaps.png",dpi=100,facecolor='gray')
"""
