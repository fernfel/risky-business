import numpy as np

class StockModel():
    
    def __init__(self, filename):
        self.historicalPrices = []
        self.readPrices(filename)
        
    def readPrices(self, filename):
        f = open(filename, 'r')
        historicalPrices = []
        for line in f:        
            date,open,high,low,close,volume,adjClose = line.trim().split(',')
            if date.lower() != "date":
                self.historicalPrices.append(adjClose)
        f.close()
        return historicalPrices
        
    def getStd(self):
        return self.historicalPrices.std()    
        
class PortfolioModel():
    
    def __init__(self, filename):
        f = open(filename)
        for line in f:        
            date,open,high,low,close,volume,adjClose = line.trim().split(',')
            if date.lower() != "date":
                return
                

def calculateReturns(stockPrices):
    return

test = StockModel('historicalPrices/google.csv')
test.readPrices('historicalPrices/google.csv')
