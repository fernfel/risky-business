import numpy as np
import scipy as sp
import scipy.stats as stats
import copy

class StockModel():
    
    def __init__(self, filename):
        self.dates = []
        self.historicalPrices = []
        f = open(filename)
        for line in f:        
            date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
            if date.lower() != "date":
                self.dates.append(date)
                self.historicalPrices.append(float(adjClose))
        f.close()
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

def calculateCorrelation(x, y):
    
    if len(x.returns) == len(y.returns):
        return stats.pearsonr(x.returns, y.returns)
    
    biggerArray = []
    smallerArray = []
    intersectionDates = []
    intersectionPrices = []
    
    if len(x.returns) > len(y.returns):
        biggerArray = copy.deepcopy(x.returns).tolist()
        smallerArray = copy.deepcopy(y.returns).tolist()
        intersectionDates = [val for val in x.dates if val in y.dates]
    elif len(x.returns) < len(y.returns):
        biggerArray = copy.deepcopy(y.returns).tolist()
        smallerArray = copy.deepcopy(x.returns).tolist()
        intersectionDates = [val for val in y.dates if val in x.dates]
    
    for date in intersectionDates:
        index = 0
        if len(x.returns) > len(y.returns):
            index = x.dates.index(date)
        elif len(x.returns) < len(y.returns):
            index = y.dates.index(date)
        intersectionPrices.append(biggerArray[index])
    
    print len(intersectionPrices)
    print len(smallerArray)
    if len(intersectionPrices) != len(smallerArray):
        intersectionPrices.pop()
    
    return stats.pearsonr(intersectionPrices, smallerArray)

google = StockModel('historicalPrices/google.csv')
print 'GOOG: ' + str(google.getVol())
print len(google.returns)

autodesk = StockModel('historicalPrices/autodesk.csv')
print 'Autodesk: ' + str(autodesk.getVol())
print len(autodesk.returns)

cocaCola = StockModel('historicalPrices/ko.csv')
print 'CocaCola: ' + str(cocaCola.getVol())
print len(cocaCola.returns)

print calculateCorrelation(google, autodesk)
print calculateCorrelation(cocaCola, autodesk)