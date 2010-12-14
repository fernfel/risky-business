#!/usr/bin/env python

from pylab import *
#from mpt import *

MAX_WIDTH=8
ACTUAL_W= 24.4
MAX_HEIGHT=7
TITLE= "Returns and Volatility for each Stock in Current Portfolio"
N_GRIDLINES=10

COLORHASH= ['#0600FF','#3D39FD', '#6865FE', '#B4B2FF', '#DFDEFE', '#FFFFFF', '#FDE1E1', '#FFB8B8', '#FE7676', '#FF4848', '#FF0000']



def getGraph(portfolio):
	clientStocks= {}
	for key in portfolio.stocks:
		clientStocks[key]= (portfolio.dataset[key].expectedReturn(), portfolio.dataset[key].annualVol)
		
	bar_graph(clientStocks, graph_title=TITLE, output_name='testSum.png')

#def makeArray(stockList):
#	for i in stocklist:		

def bar_graph(portfolio, graph_title='', output_name='sumVis.png'):
	sortedP= sorted(portfolio) #list of tickers alphabetically
	
	figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
	title(graph_title, size='small')
	space= 0.2
	intrv= ACTUAL_W/double(len(portfolio))-space
	
    # add bars
	for i, key in enumerate(sortedP):
		bar(intrv*(i*(1.0+space) + 0.5), portfolio[key][0], color=COLORHASH[int(10*portfolio[key][1])], width= intrv-space)

    #axis setup
	#(arange(space + w/2.0, len(name_value_dict))
	#arange(space + w/2.0, MAX_WIDTH*5 - space - w/2.0, (MAX_WIDTH*5-space)/double(len(name_value_dict))
	space += 0.2
	xticks(arange(intrv*(1.0+space)/2 + 0.25, ACTUAL_W, intrv + space/2.0),
		[key for key in sortedP],
		size='xx-small', rotation='vertical')
		#[ticker for ticker in portfolio],
	max_value = max(portfolio.values())[0]
	min_value = min(portfolio.values())[0]
	
	tick_range = arange(min_value, max_value, (max_value / (N_GRIDLINES/2)))
	#tick_range= arange(-0.6, 0.6, 0.1)
	
	yticks(tick_range, size='xx-small')
	formatter = FixedFormatter([str(x) for x in tick_range])
	gca().yaxis.set_major_formatter(formatter)
	gca().yaxis.grid(which='major')
   
	savefig(output_name)
	show()


#if __name__ == "__main__":
#	getGraph(portfolio)


