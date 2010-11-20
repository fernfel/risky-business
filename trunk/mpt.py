import numpy as np

class StockModel():
    
    def __init__(self, filename):
        self.historicalPrices = []
        f = open(filename)
        for line in f:        
            date,openPrice,high,low,close,volume,adjClose = line.strip().split(',')
            if date.lower() != "date":
                self.historicalPrices.append(adjClose)
        f.close()
        
class PortfolioModel():
    
    def __init__(self, filename):
        self.test = 'test'

def calculateReturns(stockPrices):
    return

test = StockModel('historicalPrices/google.csv')