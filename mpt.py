import numpy as np

class StockModel():
    
    def __init__(self, filename):
        self.historicalPrices = []
        f = open(filename)
        for line in f:        
            date,openPrice,high,low,close,volume,adjClose = line.strip().split(',')
            if date.lower() != "date":
                self.historicalPrices.append(float(adjClose))
        f.close()
        self.historicalPrices = np.array(self.historicalPrices)
        self.returns = np.array(self.calculateReturns(self.historicalPrices))
        
        
    def calculateReturns(self, historicalPrices):
        dayToDayReturns = []
        for i in range(len(historicalPrices)-1):
            percReturn = (historicalPrices[i+1] - historicalPrices[i]) / historicalPrices[i]
            dayToDayReturns.append(percReturn)
        return dayToDayReturns
        
    def getVol(self):
        return self.returns.std()
        
class PortfolioModel():
    
    def __init__(self, filename):
        self.test = 'test'

def calculateReturns(stockPrices):
    return

test = StockModel('historicalPrices/google.csv')
print test.getVol()
print test.returns