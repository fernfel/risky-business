import annote
from pylab import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

x = range(10)
y = range(10)
annotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

MAX_WIDTH= 5
MAX_HEIGHT= 5
graph_title= "Recommended Stocks"

"""
figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
title(graph_title, size='small')
scatter(x,y)
af =  annote.AnnoteFinder(x,y, annotes)
connect('button_press_event', af)
show()
"""

def getInteractiveGraph(parent, currentPortfolio, recPortfolios, onclickFxn, idealRisk):
	return dot_graph(parent, currentPortfolio, recPortfolios, onclickFxn, idealRisk)
	
def dot_graph(parent, currPortfolio, recPortfolios, onclickFxn, idealRisk):

	f = Figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions
	ax = f.add_subplot(111)
	ax.set_autoscale_on(True)
	ax.set_title(graph_title)
	ax.set_xlabel('Risk')
	ax.set_ylabel('Expected Return')

	ptX=[]
	ptY=[]
	
	for i in recPortfolios.itervalues():
		ptX.append(i.expectedReturn)
		ptY.append(i.annualVol)
	
	#current portfolio
	ax.scatter([currPortfolio.expectedReturn], [currPortfolio.annualVol], c='#000000')
	
	#recommended portfolios
	ax.scatter(ptX, ptY, c='g', marker='x', alpha=.8)
	
	#
	ax.scatter([idealRisk],[1], s=30, c='g')
	
#		#current portfolio
#	ax.scatter([currPortfolio.expectedReturn], [currPortfolio.annualVol], c='#000000')
#	
#	#recommended portfolios
#	ax.scatter(ptX, ptY, c='g', marker='x', alpha=.8)
#	
#	#
#	ax.scatter([1],[idealRisk], s=30, c='g')
	
	af = annote.AnnoteFinder(x, y, annotes)
	connect('button_press_event', af)
	
#	show()
	return f
	
if __name__ == "__main__":
	getInteractiveGraph()