import annote
from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
	return dot_graph() #parent, currentPortfolio, recPortfolios, onclickFxn, idealRisk)
	
def dot_graph(parent, currPortfolio, recPortfolios, onclickFxn, idealRisk):
	f = Figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions  
	title(graph_title, size='medium')
	ptX=[]
	ptY=[]
	
	for i in recPortfolios:
		ptX.append(recPortfolio[i].expectedReturn())
		ptY.append(recPortfolio[i].annualVol)
	
	#current portfolio
	scatter([currPortfolio.expectedReturn()], [currPortfolio.annualVol], c='#000000')
	
	#recommended portfolios
	scatter(ptX, ptY, c='g', marker='x', alpha=.8)
	
	#
	scatter([1],[idealRisk], s=30, c='g')
	
	
	af = annote.AnnoteFinder(x, y, annotes)
	connect('button_press_event', af)
	show()
	
	
	
if __name__ == "__main__":
	getInteractiveGraph()