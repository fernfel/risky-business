import numpy as np
#import scipy as sp
#import scipy.stats as stats
import copy
import math

# todo: need more caching

class StockModel():
    
    def __init__(self, filename):
        self.dates = []
        self.historicalPrices = []
        f = open('data/' + filename + '.csv')
        for line in f:        
            date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
            if date.lower() != "date":
                self.dates.append(date)
                self.historicalPrices.append(float(adjClose))
        f.close()
        self.returns = np.array(self.calculateReturns(self.historicalPrices))
        
        self.updateVol()
               
    def calculateReturns(self, historicalPrices):
        dayToDayReturns = []
        for i in range(len(historicalPrices)-1):
#            percReturn = (historicalPrices[i+1] - historicalPrices[i]) / historicalPrices[i]
            percReturn = math.log(historicalPrices[i+1]/historicalPrices[i])
            dayToDayReturns.append(percReturn)
        return dayToDayReturns
    
    def updateVol(self):
        self.dailyVol = self.returns.std()
        self.annualVol = self.dailyVol*math.sqrt(252)
        
class PortfolioModel():
    
    def __init__(self):
        self.stocks = {}
        
    def addStock(self, stockTicker, quantity, price):
        self.stocks[stockTicker] = (quantity, price)
        
    def stockWeight(self, ticker):
        
        stockAssetValue = 0.0
        totalAssetValue = 0.0
        
        for stockTicker, info in self.stocks.iteritems():
            quantity, price = info
            
            # grab latest price
            model = StockModel(stockTicker)
            price = model.historicalPrices[0] 
            
            if ticker == stockTicker:
                stockAssetValue += quantity * price
            totalAssetValue += quantity * price
        
        return (stockAssetValue/totalAssetValue)
        
        
    def variance(self):
        
        variance = 0
        
        for iTicker in self.stocks.iterkeys():
            
            iWeight = self.stockWeight(iTicker)
            iStockModel = StockModel(iTicker)
            iVol = iStockModel.dailyVol
            
            for jTicker in self.stocks.iterkeys():

                jWeight = self.stockWeight(jTicker)
                jStockModel = StockModel(jTicker.lower())
                jVol = jStockModel.dailyVol
                
                correlation = calculateCorrelation(iStockModel, jStockModel)
                
                variance += iWeight*jWeight*iVol*jVol*correlation
        
        return variance
    
    def dailyVol(self):
        return np.sqrt(self.variance())
    
    def annualizedVol(self):
        return math.sqrt(252) * self.dailyVol()

def calculateCorrelation(x, y):
    
    # Returns the Pearson correlation coefficient for p1 and p2
    def sim_pearson(p1,p2):
      # Get the list of mutually rated items
      #si={}
      #for item in p1: 
      #  print "item:", item
      #  if item in p2: 
      #      si[item]=1
      #print "si:", si

      # if they are no ratings in common, return 0
      #if len(si)==0: return 0
	  #----if not the same size arrays:
      if len(p1) != len(p2): return 0
    
      # Sum calculations
      #n=len(si)
      n= len(p1)
      
      # Sums of all the preferences
      sum1=sum(p1)
      sum2=sum(p2)
      
      # Sums of the squares
      sum1Sq=sum([pow(p,2) for p in p1])
      sum2Sq=sum([pow(p,2) for p in p2])    
      
      # Sum of the products
      pSum=sum([p1[it]*p2[it] for it in range(n)])
      
      # Calculate r (Pearson score)
      num=pSum-(sum1*sum2/len(p1))
      den= math.sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
      if den==0: return 0
    
      r=num/den
    
      return r
    
    if len(x.returns) == len(y.returns):
        #return stats.pearsonr(x.returns, y.returns)
        return sim_pearson(x.returns, y.returns)
    
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
        if index < len(biggerArray):
            intersectionPrices.append(biggerArray[index])
    
    #return stats.pearsonr(intersectionPrices, smallerArray)
    return sim_pearson(intersectionPrices, smallerArray)


google = StockModel('GOOG')
print 'GOOG: ' + str(google.dailyVol)
print 'GOOG: ' + str(google.annualVol)

autodesk = StockModel('ADSK')
print 'Autodesk: ' + str(autodesk.dailyVol)

cocaCola = StockModel('KO')
print 'CocaCola: ' + str(cocaCola.dailyVol)

portfolio = PortfolioModel()
portfolio.addStock('KO', 1000, 69.21)
portfolio.addStock('GOOG', 100, 290.21)
portfolio.addStock('ADSK', 1000, 9.21)
print 'Stock Weight of KO: ' + str(portfolio.stockWeight('KO'))
print 'Portfolio Volatility (daily): ' + str(portfolio.dailyVol()) 
print 'Portfolio Volatility (annual): ' + str(portfolio.annualizedVol()) 