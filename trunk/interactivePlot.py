import annote
from pylab import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


MAX_WIDTH= 10
MAX_HEIGHT= 5
graph_title= "Recommended Stocks"

def getInteractiveGraph(parent, currentPortfolio, recPortfolios, onclickFxn, idealRisk):
	return dot_graph(parent, currentPortfolio, recPortfolios, onclickFxn, idealRisk)
	
def dot_graph(parent, currPortfolio, recPortfolios, onclickFxn, idealRisk):

	f = Figure(figsize=(MAX_WIDTH, MAX_HEIGHT)) # image dimensions
#	f = plt.figure()
	ax = f.add_subplot(111)
	ax.set_autoscale_on(True)
	ax.set_title(graph_title)
	ax.set_xlabel('Risk')
	ax.set_ylabel('Expected Return')

	ptX = [v.annualVol for v in recPortfolios.values()]
	ptY = [v.expectedReturn for v in recPortfolios.values()]
	
	tickers = recPortfolios.keys()
	ptXCopy = [v.annualVol for v in recPortfolios.values()]
	ptYCopy = [v.expectedReturn for v in recPortfolios.values()]
	
	
	#current portfolio
	ax.scatter([currPortfolio.expectedReturn], [currPortfolio.annualVol], c='k', s=50)
	
	#recommended portfolios
	ax.scatter(ptX, ptY, c='g', marker='^', s=60, alpha=.3)
	
	#
	ax.scatter([idealRisk],[1], s=60, c='g')
	
#		#current portfolio
#	ax.scatter([currPortfolio.expectedReturn], [currPortfolio.annualVol], c='#000000')
#	
#	#recommended portfolios
#	ax.scatter(ptX, ptY, c='g', marker='x', alpha=.8)
#	
#	#
#	ax.scatter([1],[idealRisk], s=30, c='g')
	
	af = annote.AnnoteFinder(ptXCopy, ptYCopy, tickers)
	connect('button_press_event', af)
	
#	show()
	return f
	
if __name__ == "__main__":
	getInteractiveGraph()