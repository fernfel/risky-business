import numpy as np
#import scipy as sp
import scipy.stats as stats
import copy
import math
import os, glob
import time

# todo: need more caching
stockModelCache = dict()

class StockModel():
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.dates = []
        self.historicalPrices = []
        f = open('data/' + ticker + '.csv')
        self.beta = f.readline().strip()
        if self.beta == "N/A":
            self.beta = 1
        else:
            self.beta = float(self.beta)
        x = 1
        for line in f:
            if line.strip() != "":
                if x > 1:
                    date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
    				#if date.lower() != "date":
                    self.dates.append(date)
                    self.historicalPrices.append(float(adjClose))
                x+=1                
     
        f.close()
        self.returns = np.array(self.calculateReturns(self.historicalPrices))
        self.updateVol()
        
        stockModelCache[self.ticker] = self
               
    def calculateReturns(self, historicalPrices):
        dayToDayReturns = []
        for i in range(len(historicalPrices)-1):
#            percReturn = (historicalPrices[i+1] - historicalPrices[i]) / historicalPrices[i]
            if historicalPrices[i] == 0 or historicalPrices[i+1] == 0:
                percReturn = 0
            else:
                percReturn = math.log(historicalPrices[i+1]/historicalPrices[i])
            dayToDayReturns.append(percReturn)
        return dayToDayReturns
        
    def expectedReturn(self):
        beta = self.beta
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
        
    def addStock(self, stockTicker, quantity):
        if stockTicker in self.stocks:
            self.stocks[stockTicker] += quantity
        else:
            self.stocks[stockTicker] = quantity
        
    def calculateStockWeight(self):
        
        for ticker in self.stocks.iterkeys():  
        
            stockAssetValue = 0.0
            totalAssetValue = 0.0
            
            for stockTicker, info in self.stocks.iteritems():
                quantity = info
                
                # grab latest price
                model = stockModelCache[stockTicker]
                price = model.historicalPrices[0] 
                
                if ticker == stockTicker:
                    stockAssetValue += quantity * price
                totalAssetValue += quantity * price
            
            self.stockWeights[ticker] = (stockAssetValue/totalAssetValue)
    
    def calculateExpectedReturn(self):
        
        expectedReturn = 0.0
        for ticker, weight in self.stockWeights.iteritems():
            expectedReturn += weight*stockModelCache[ticker].expectedReturn()
        return expectedReturn
        
    def variance(self):
        
        beforeTime = time.time()
        correlationTime = 0
        variance = 0
        
        for iTicker in self.stocks.iterkeys():
            
            iWeight = self.stockWeights[iTicker]
            iStockModel = stockModelCache[iTicker]
            iVol = iStockModel.dailyVol
            
            for jTicker in self.stocks.iterkeys():

                jWeight = self.stockWeights[jTicker]
                jStockModel = stockModelCache[jTicker]
                jVol = jStockModel.dailyVol
                
                start = time.time()
                correlation = calculateCorrelation(iStockModel, jStockModel)
                end = time.time()
                correlationTime += (end-start)
                
                variance += iWeight*jWeight*iVol*jVol*correlation
        
        afterTime = time.time()
        diff = afterTime-beforeTime
#        print 'variance: ' + str(diff)
#        print 'correlation time: ' + str(correlationTime)
#        print 'proportion of correlation on variance: ' + str(correlationTime/float(diff) * 100) + '%'
        
        return variance
    
    def calculateDailyVol(self):
        return np.sqrt(self.variance())
    
    def calculateAnnualizedVol(self):
        return math.sqrt(252) * self.dailyVol()
    
    def covariance(self, s1, s2):
        s1Returns, s2Returns = makeSameSizedArray(s1, s2)
        s1Returns = np.array(s1Returns)
        s2Returns = np.array(s2Returns)
        covariance = 0.0
        
        for i in range(len(s1Returns)):
            s1 = s1Returns[i] - s1Returns.mean()
            s2 = s2Returns[i] - s2Returns.mean()
            
            covariance += s1 * s2 / len(s1Returns)
        return covariance
    
    def updateStatistics(self):
        self.calculateStockWeight()
        self.dailyVol = self.calculateDailyVol()
        self.annualizedVol = self.dailyVol * math.sqrt(252)
        self.expectedReturn = self.calculateExpectedReturn()
        
#    def efficientFrontier(self):
#        w = np.array(self.stockWeights.values())
#        R = np.array([stockModelCache[i].expectedReturn() for i in self.stockWeights.keys()])
#        sigma = []
#        q = 0.8
#        
#        for ticker1 in self.stockWeights.keys():
#            row = []
#            for ticker2 in self.stockWeights.keys():
#                cov = self.covariance(stockModelCache[ticker1], stockModelCache[ticker2])
#                row.append(cov)
#            sigma.append(row)
#        
#        variance = w.transpose() * sigma * w
#        portExpectedReturn = q*R.transpose()*w
#        
#        print variance
#        print portExpectedReturn
#        print variance - portExpectedReturn
#        
#        return  

def calculateCorrelation(x, y):
    
    # Returns the Pearson correlation coefficient for p1 and p2
    def sim_pearson(p1,p2):
      
      start = time.time()
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
      if den==0:
          end = time.time()
          print 'Correlation time: ' + str(end-start) 
          return 0
    
      r=num/den
      
      end = time.time()
      print 'Correlation time: ' + str(end-start) 
      return r

    if len(x.returns) == len(y.returns):
        return stats.pearsonr(x.returns, y.returns)[0]
#        return sim_pearson(x.returns, y.returns)
    
    beforeTime = time.time()
    intersectionPrices, smallerArray = makeSameSizedArray(x, y)
    afterTime = time.time()
#    print 'Intersection array time: ' + str(afterTime-beforeTime)
    
    return stats.pearsonr(intersectionPrices, smallerArray)[0]
#    return sim_pearson(intersectionPrices, smallerArray)

def makeSameSizedArray(x, y):
    
    #based on the assumption that every company has prices up to today...
    cutArray = []
    smallArray = []
    
    if len(x.returns) > len(y.returns):
        index = len(x.returns) - len(y.returns)
        cutArray = x.returns[index:]
        smallArray = y.returns
    elif len(x.returns) < len(y.returns):
        index = len(y.returns) - len(x.returns)
        cutArray = y.returns[index:]
        smallArray = x.returns
    else:
        return (x.returns, y.returns)
    
    return (cutArray, smallArray)

def euclideanDistance(p1, p2):
    
    distance = 0
    for i in range(len(p1)):
        distance += math.pow((p1[i] - p2[i]), 2)
            
    distance = math.sqrt(distance)
    
    return distance

def gaussianWeight(distance, sigma=2): 
    
    distance = math.pow(math.e, -distance/2*sigma**2)
    return distance

def knn(dataset, p1, k, idealVol, money, weightFunc=gaussianWeight, similiarity=euclideanDistance):
    
    # reorder the training set based on distance to p1
    distances = []
    for ticker in dataset:        
        # how much money do you have spend?
        stockPrice = stockModelCache[ticker].historicalPrices[0]
        quantity = int(money/stockPrice)
        if quantity > 0:
            p2 = copy.deepcopy(p1)
            p2.addStock(ticker, quantity)
            p2.updateStatistics()
            tuple = (similiarity([idealVol, 0.15], [p2.annualizedVol, p2.expectedReturn]), ticker, quantity)
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
    
    idealVol = 0.20
    moneyToSpend = 1000
    k = 5
    
    path = 'data/'
    for infile in glob.glob( os.path.join(path, '*.csv') ):
        ticker = infile.split('/')[1].split('.')[0]
        stockModel = StockModel(ticker)
        years = len(stockModel.historicalPrices)/float(252)
        if years < 5:
            os.remove(infile)
            print 'Removed due to low data: ' + ticker
         
    f = open('recommendedPorts.csv', 'w')
    f.write('Ticker,AnnualRisk,ExpReturn\n')
    
    portfolio = PortfolioModel()
    portfolio.addStock('KO', 20)
    portfolio.addStock('GOOG', 20)
    portfolio.addStock('ADSK', 20)
    portfolio.addStock('C', 20)
    portfolio.addStock('F', 20)
    portfolio.updateStatistics()
    
    f.write('None' + ',' + str(portfolio.annualizedVol) + ',' + str(portfolio.expectedReturn) + '\n')
    
    # applying a heuristic to thin out stocks with volatilites that are higher/lower than what we want it to be
    volGap = idealVol - portfolio.annualizedVol
    thinSP = []
    if volGap > 0:
        thinSP = [(model.annualVol, ticker) for ticker, model in stockModelCache.iteritems() if model.annualVol > portfolio.annualizedVol]
    elif volGap < 0:
        thinSP = [(model.annualVol, ticker) for ticker, model in stockModelCache.iteritems() if model.annualVol < portfolio.annualizedVol]
    thinSP.sort()
    dataset = [item[1] for item in thinSP]
    
#    print 'Stock Weight of KO: ' + str(portfolio.stockWeights['KO'])
#    print 'Portfolio Volatility (daily): ' + str(portfolio.dailyVol()) 
#    print 'Portfolio Volatility (annual): ' + str(portfolio.annualizedVol())
#    print 'Expected Return: ' + str(portfolio.expectedReturn())

#    google = stockModelCache['GOOG']    
#    autodesk = stockModelCache['ADSK']   
#    cocaCola = stockModelCache['KO']
#    ford = stockModelCache['F']
#    nike = stockModelCache['NKE']
#    microsoft = stockModelCache['MSFT']
#    citi = stockModelCache['C']
#    
#    dataset = stockModelCache.keys()
    
    beforeTime = time.time()
    recommendedStocks = knn(dataset, portfolio, k, idealVol, moneyToSpend)
    afterTime = time.time()
    diff = afterTime-beforeTime
    print 'seconds that have elapsed: ' + str(diff)
    
    print recommendedStocks
    
    for item in recommendedStocks:
        ticker = item[1]
        quantity = item[2]
        p2 = copy.deepcopy(portfolio)
        p2.addStock(ticker, quantity)
        p2.updateStatistics()
        f.write(ticker + ',' + str(p2.annualizedVol) + ',' + str(p2.expectedReturn) + '\n')
    f.close()
    