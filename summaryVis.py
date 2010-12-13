#!/usr/bin/env python

from pylab import *
from mpt import StockModel

MAX_WIDTH=8
ACTUAL_W= 24.4
MAX_HEIGHT=7
TITLE= "Returns and Volatility for each Stock in Current Portfolio"
NO_GRIDLINES=10

EX = {'A': -.5, 'AA': 0, 'ABC': .12, 'ADBE': -.3, 'AIV': -.03, 'DISCA': 0.2, 'EBAY': 0.3, 'GE': 0.45, 'GOOG': 0.5, 'YHOO': -0.1, 'LOLOL': -.5, 'TL;DR': 0, 'GTA': .12, 'DBZ': -.3, 'TCAT': -.03, 'WCT': 0.2, 'XXX': 0.3, 'ZZY': 0.45, 'ZZ': 0.5, 'Z': -0.1}
DERP= array([4, 6, 1, 8, 7, 3, 8, 2,5 ,8, 2, 4,5, 0, 2, 4, 4, 9, 6, 2])

COLORHASH= ['#0600FF','#3D39FD', '#6865FE', '#B4B2FF', '#DFDEFE', '#FFFFFF', '#FDE1E1', '#FFB8B8', '#FE7676', '#FF4848', '#FF0000']


def getGraph(stockList=EX):  
	bar_graph(EX, graph_title=TITLE, output_name='testSum.png')

#def makeArray(stockList):
#	for i in stocklist:		

def bar_graph(name_value_dict, graph_title='', output_name='bargraph.png'):
	figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
	title(graph_title, size='small')
	space= 0.2
	intrv= ACTUAL_W/double(len(name_value_dict))-space
	w= intrv
    # add bars
	for i, key in zip(range(len(name_value_dict)), name_value_dict.keys()):
		bar(intrv*(i*(1.0+space) + 0.5), name_value_dict[key], color=COLORHASH[int(DERP[i])], width= intrv-space)
   
    # axis setup
	#(arange(space + w/2.0, len(name_value_dict))
	#arange(space + w/2.0, MAX_WIDTH*5 - space - w/2.0, (MAX_WIDTH*5-space)/double(len(name_value_dict))
	space += 0.2
	xticks(arange(intrv*(1.0+space)/2 + 0.25, ACTUAL_W, intrv + space/2.0),
		[name for name, value in zip(name_value_dict.keys(), name_value_dict.values())],
		size='xx-small', rotation='vertical')
	max_value = max(name_value_dict.values())
	min_value = min(name_value_dict.values())
	
	#tick_range = arange(min_value, max_value, (max_value / (NO_GRIDLINES/2)))
	tick_range= arange(-0.6, 0.6, 0.1)
	
	yticks(tick_range, size='xx-small')
	formatter = FixedFormatter([str(x) for x in tick_range])
	gca().yaxis.set_major_formatter(formatter)
	gca().yaxis.grid(which='major')
   
	savefig(output_name)
	show()


if __name__ == "__main__":
	getGraph()


