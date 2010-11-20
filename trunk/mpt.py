import numpy

class StockModel():
    
    def __init__(self, filename):
        f = open(filename)
        for line in f:        
            date,open,high,low,close,volume,adjClose = line.trim().split(',')
            if date.lower() != "date":
                
            
        
class PortfolioModel():
    
    def __init__(self, filename):
        f = open(filename)
        for line in f:        
            date,open,high,low,close,volume,adjClose = line.trim().split(',')
            if date.lower() != "date":
                return
                

def calculateReturns(stockPrices):
    return




