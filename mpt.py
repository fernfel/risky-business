import numpy as np
#import scipy as sp
#import scipy.stats as stats
import copy
import math

# todo: need more caching

class StockModel():
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.dates = []
        self.historicalPrices = []
        f = open('data/' + ticker + '.csv')
        self.beta = f.readLine()
        x = 0
        for line in f:
        	if x > 1:
				date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
				#if date.lower() != "date":
				self.dates.append(date)
				self.historicalPrices.append(float(adjClose))
			x+=1                
     
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
    
    def calculateBeta(self):
        sp500 = StockModel('S+P')
        sp500Returns, returns = makeSameSizedArray(sp500, self)
        
        sp500Returns = np.array(sp500Returns)
        returns = np.array(returns)
        
        sp500Mean = sp500Returns.mean()
        stockMean = returns.mean()
        covariance = 0.0
        
        for i in range(len(sp500Returns)):
            sp500Dev = sp500Returns[i] - sp500Mean
            stockDev = returns[i] - stockMean
            
            covariance += sp500Dev * stockDev / len(sp500Returns)
        
        beta = covariance / np.var(sp500Returns)
        
        return beta
        
    def expectedReturn(self):
        beta = self.calculateBeta()
        # yield from 10 yr treasury
        riskFreeRateOfInterest = 0.03
        expectedReturnMarket = 0.11
        
        expectedReturn = riskFreeRateOfInterest + beta*(expectedReturnMarket - riskFreeRateOfInterest)
        return expectedReturn
    
    def updateVol(self):
        self.dailyVol = self.returns.std()
        self.annualVol = self.dailyVol*math.sqrt(252)
        
class PortfolioModel():
    
    def __init__(self):
        self.stocks = {}
        self.stockWeights = {}
        
    def addStock(self, stockTicker, quantity, price):
        if stockTicker in self.stocks:
            self.stocks[stockTicker] += quantity
        else:
            self.stocks[stockTicker] = quantity
        self.calculateStockWeight()
        
    def calculateStockWeight(self):
        
        for ticker in self.stocks.iterkeys():  
        
            stockAssetValue = 0.0
            totalAssetValue = 0.0
            
            for stockTicker, info in self.stocks.iteritems():
                quantity = info
                
                # grab latest price
                model = StockModel(stockTicker)
                price = model.historicalPrices[0] 
                
                if ticker == stockTicker:
                    stockAssetValue += quantity * price
                totalAssetValue += quantity * price
            
            self.stockWeights[ticker] = (stockAssetValue/totalAssetValue)
        
        
    def variance(self):
        
        variance = 0
        
        for iTicker in self.stocks.iterkeys():
            
            iWeight = self.stockWeights[iTicker]
            iStockModel = StockModel(iTicker)
            iVol = iStockModel.dailyVol
            
            for jTicker in self.stocks.iterkeys():

                jWeight = self.stockWeights[jTicker]
                jStockModel = StockModel(jTicker.lower())
                jVol = jStockModel.dailyVol
                
                correlation = calculateCorrelation(iStockModel, jStockModel)
                
                variance += iWeight*jWeight*iVol*jVol*correlation
        
        return variance
    
    def dailyVol(self):
        return np.sqrt(self.variance())
    
    def annualizedVol(self):
        return math.sqrt(252) * self.dailyVol()
    
    def efficientFrontier(self):
        q = 0.8
        return 

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
    
    intersectionPrices, smallerArray = makeSameSizedArray(x, y)
    
    #return stats.pearsonr(intersectionPrices, smallerArray)
    return sim_pearson(intersectionPrices, smallerArray)

def makeSameSizedArray(x, y):
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
    else:
        return (x.returns, y.returns)
    
    for date in intersectionDates:
        index = 0
        if len(x.returns) > len(y.returns):
            index = x.dates.index(date)
        elif len(x.returns) < len(y.returns):
            index = y.dates.index(date)
        if index < len(biggerArray):
            intersectionPrices.append(biggerArray[index])
    
    if len(intersectionPrices) > len(smallerArray):
        intersectionPrices.pop()
    
    return (intersectionPrices, smallerArray)

def euclideanDistance(p1, p2):
    
    distance = 0
    for i in range(len(p1)):
        try:
            distance += math.pow((p1[i] - p2[i]), 2)
        except KeyError:
            print p1
            
    distance = math.sqrt(distance)
    
    return distance

def gaussianWeight(distance, sigma=2): 
    
    distance = math.pow(math.e, -distance/2*sigma**2)
    return distance

def knn(dataset, p1, k, idealVol, weightFunc=gaussianWeight, similiarity=euclideanDistance):
    
    # reorder the training set based on distance to p1
    distances = []
    for model in dataset:
        p2 = copy.deepcopy(p1)
        p2.addStock(model.ticker, 100, 100)
        tuple = (similiarity([idealVol], [p2.annualizedVol()]), model.ticker)
        distances.append(tuple)
    distances.sort()
    
    if k > len(dataset):
        k = len(dataset)
        
    recommendedStocks = distances[0:k]
    return recommendedStocks

if __name__ == "__main__":
#	tickers = set()
#	ticker = ""
#	print "When you have finished populating your portfolio, type 'done'"
#	while ticker.lower() != "done":
#		ticker = raw_input("Add a ticker to your portfolio")
#		if ticker not in tickers: # TODO: make sure its in S&P also
#			tickers.add(ticker)
#	
#	portfolio = PortfolioModel()
#	for ticker in tickers:
#		temp = StockModel(ticker)
#		print ticker + ': ' + str(temp.dailyVol)
#		print ticker + ': ' + str(temp.annualVol)	
#		print "" 

    google = StockModel('GOOG')
    print 'GOOG: ' + str(google.dailyVol)
    print 'GOOG: ' + str(google.annualVol)
#    print google.calculateBeta()
#    print google.expectedReturn()
    
    autodesk = StockModel('ADSK')
    print 'Autodesk: ' + str(autodesk.dailyVol)
#    print autodesk.calculateBeta()
#    print autodesk.expectedReturn()
    
    cocaCola = StockModel('KO')
    print 'CocaCola: ' + str(cocaCola.dailyVol)
#    print cocaCola.calculateBeta()
#    print cocaCola.expectedReturn()
    
    portfolio = PortfolioModel()
    portfolio.addStock('KO', 1000, 69.21)
    portfolio.addStock('GOOG', 100, 290.21)
    portfolio.addStock('ADSK', 1000, 9.21)
#    print 'Stock Weight of KO: ' + str(portfolio.stockWeights['KO'])
#    print 'Portfolio Volatility (daily): ' + str(portfolio.dailyVol()) 
#    print 'Portfolio Volatility (annual): ' + str(portfolio.annualizedVol())
    
    ford = StockModel('F')
    nike = StockModel('NKE')
    microsoft = StockModel('MSFT')
    citi = StockModel('C')
    
    dataset = [google, cocaCola, autodesk, ford, nike, microsoft, citi]
    print knn(dataset, portfolio, 5, 0.20)