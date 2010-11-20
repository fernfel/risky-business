import numpy as np
import scipy as sp

class StockModel():
    
    def __init__(self, filename):
        self.historicalPrices = []
        f = open(filename)
        for line in f:        
            date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
            if date.lower() != "date":
                self.historicalPrices.append((date, float(adjClose)))
        f.close()
        self.returns = np.array(self.calculateReturns(self.historicalPrices))
               
    def calculateReturns(self, historicalPrices):
        dayToDayReturns = []
        for i in range(len(historicalPrices)-1):
            percReturn = (historicalPrices[1][i+1] - historicalPrices[1][i]) / historicalPrices[1][i]
            dayToDayReturns.append(percReturn)
        return dayToDayReturns
        
    def getVol(self):
        return self.returns.std()
        
class PortfolioModel():
    
    def __init__(self, filename):
        self.test = 'test'

def calculateCorrelation(x, y):
    return

def calculateReturns(stockPrices):
    return

google = StockModel('historicalPrices/google.csv')
print 'GOOG: ' + str(google.getVol())
print len(google.returns)


autodesk = StockModel('historicalPrices/autodesk.csv')
print 'Autodesk: ' + str(autodesk.getVol())
print len(autodesk.returns)

cocaCola = StockModel('historicalPrices/ko.csv')
print 'CocaCola: ' + str(cocaCola.getVol())
print len(cocaCola.returns)