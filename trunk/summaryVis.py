#!/usr/bin/env python

from pylab import *
from mpt import *
import random

MAX_WIDTH=8
ACTUAL_W= 24.4
MAX_HEIGHT=7
TITLE= "Returns and Volatility for each Stock in Current Portfolio"
NO_GRIDLINES=10

COLORHASH= ['#0600FF','#3D39FD', '#6865FE', '#B4B2FF', '#DFDEFE', '#FFFFFF', '#FDE1E1', '#FFB8B8', '#FE7676', '#FF4848', '#FF0000']


        



def getGraph(portfolio):
	clientStocks= {}
	print "stocks:", portfolio.stocks
	for key in portfolio.stocks:
		clientStocks[key]= (portfolio.dataset[key].annualVol, portfolio.dataset[key].returns)
		
	bar_graph(clientStocks, graph_title=TITLE, output_name='testSum.png')

#def makeArray(stockList):
#	for i in stocklist:		

def bar_graph(portfolio, graph_title='', output_name='sumVis.png'):
	print "port:", portfolio
	sortedP= sorted(portfolio) #list of tickers alphabetically
	
	figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
	title(graph_title, size='small')
	space= 0.2
	intrv= ACTUAL_W/double(len(portfolio))-space
	
    # add bars
	print "sorted?", sortedP
	for i in sortedP:
		bar(intrv*(i*(1.0+space) + 0.5), portfolio[sortedP[i]][1], color=COLORHASH[int(portfolio[sortedP[i]][0])], width= intrv-space)
		print (portfolio[sortedP[i]])
	#for i, key in zip(range(len(portfolio)), portfolio.keys()):
	#	bar(intrv*(i*(1.0+space) + 0.5), portfolio[key][1], color=COLORHASH[int(portfolio[key][0])], width= intrv-space)
   
    # axis setup
	#(arange(space + w/2.0, len(name_value_dict))
	#arange(space + w/2.0, MAX_WIDTH*5 - space - w/2.0, (MAX_WIDTH*5-space)/double(len(name_value_dict))
	space += 0.2
	xticks(arange(intrv*(1.0+space)/2 + 0.25, ACTUAL_W, intrv + space/2.0),
		[sortedP[i] for i in sortedP],
		size='xx-small', rotation='vertical')
		#[ticker for ticker in portfolio],
	#max_value = max(portfolio.values())
	#min_value = min(portfolio.values())
	
	#tick_range = arange(min_value, max_value, (max_value / (NO_GRIDLINES/2)))
	tick_range= arange(-0.6, 0.6, 0.1)
	
	yticks(tick_range, size='xx-small')
	formatter = FixedFormatter([str(x) for x in tick_range])
	gca().yaxis.set_major_formatter(formatter)
	gca().yaxis.grid(which='major')
   
	savefig(output_name)
	show()


if __name__ == "__main__":
	PORT = PortfolioModel(trainingSet)
	stocks = trainingSet.keys()
	for j in range(7):
		quantity = random.randint(1, 20)
		ticker = random.choice(stocks)
		PORT.addStock(ticker, quantity)

	PORT.updateStatistics()
	getGraph(PORT)


