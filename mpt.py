import numpy as np
import scipy.stats as stats
import copy
import math
import os, glob
import time
import random

trainingSet = dict()
testSet = dict()

class StockModel():
    
    def __init__(self, ticker, start=0, end=0):
        self.ticker = ticker
        self.dates = []
        self.historicalPrices = []
        if ticker == "S+P":
            f = open(ticker + '.csv')
        else:
            f = open('data/' + ticker + '.csv')
        
        lines = f.readlines()
        self.beta = lines[0].strip()
        if self.beta == "N/A":
            self.beta = 1     # default value if none provided
        else:
            self.beta = float(self.beta)
        
        lines.pop(0)
        lines.pop(0)
        
        if end == 0:
            lines = lines[start:]
        elif start == 0:
            lines = lines[0:end]
        
        for x in range(0, len(lines)):
            line = lines[x].strip()
            if line != "":
                date,openPrice,highPrice,lowPrice,closePrice,volume,adjClose = line.strip().split(',')
                self.dates.append(date)
                self.historicalPrices.append(float(adjClose))        
     
        f.close()
        
        self.updateCalculations()
               
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
    
    def calculateBeta(self):
        
        if self.ticker == "S+P": return 1.0
        
        sp500Returns, returns = makeSameSizedArray(sp500, self)
        # number of trading days in a year * 5 years
        divisionPoint = len(sp500Returns) - 252*5
        
        sp500Returns = np.array(sp500Returns[divisionPoint:])
        returns = np.array(returns[divisionPoint:])
        
        sp500Mean = sp500Returns.mean()
        stockMean = returns.mean()
        
        covarianceMatrix = np.cov(sp500Returns, returns)
        covariance = covarianceMatrix[0][1]
        
        beta = covariance / np.var(sp500Returns)
        return beta    
    def expectedReturn(self):
        beta = self.beta
        # yield from 10 yr treasury
        riskFreeRateOfInterest = 0.03
        expectedReturnMarket = 0.11
        
        expectedReturn = riskFreeRateOfInterest + beta*(expectedReturnMarket - riskFreeRateOfInterest)
        return expectedReturn
    
    def updateCalculations(self):
        self.returns = np.array(self.calculateReturns(self.historicalPrices))
        self.dailyVol = self.returns.std()
        self.annualVol = self.dailyVol*math.sqrt(252)
        self.beta = self.calculateBeta()
        
class PortfolioModel():
    
    def __init__(self, dataset):
        self.stocks = {}
        self.stockWeights = {}
        self.dataset = dataset    
        
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
                model = self.dataset[stockTicker]
                price = model.historicalPrices[0] 
                
                if ticker == stockTicker:
                    stockAssetValue += quantity * price
                totalAssetValue += quantity * price
            
            self.stockWeights[ticker] = (stockAssetValue/totalAssetValue)
    
    def calculateExpectedReturn(self):
        
        expectedReturn = 0.0
        for ticker, weight in self.stockWeights.iteritems():
            expectedReturn += weight*self.dataset[ticker].expectedReturn()
        return expectedReturn
        
    def variance(self):
        
        beforeTime = time.time()
        correlationTime = 0
        variance = 0
        
        for iTicker in self.stocks.iterkeys():
            
            iWeight = self.stockWeights[iTicker]
            iStockModel = self.dataset[iTicker]
            iVol = iStockModel.dailyVol
            
            for jTicker in self.stocks.iterkeys():

                jWeight = self.stockWeights[jTicker]
                jStockModel = self.dataset[jTicker]
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
    
    def updateStatistics(self):
        self.calculateStockWeight()
        self.dailyVol = self.calculateDailyVol()
        self.annualVol = self.dailyVol * math.sqrt(252)
        self.expectedReturn = self.calculateExpectedReturn()

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

def copyPortfolio(p1, dataset):
    
    p2 = PortfolioModel(dataset)
    p2.stocks = copy.deepcopy(p1.stocks)
    
    return p2

def euclideanDistance(p1, p2):
    
    distance = 0
    for i in range(len(p1)):
        distance += math.pow((p1[i] - p2[i]), 2)
            
    distance = math.sqrt(distance)
    
    return distance

def gaussianWeight(distance, sigma=2): 
    
    distance = math.pow(math.e, -distance/2*sigma**2)
    return distance

def knn(dataset, p1, k, idealVol, idealReturn, money, weightFunc=gaussianWeight, similiarity=euclideanDistance):
    
    # reorder the training set based on distance to p1
    distances = []
    for ticker, model in dataset.iteritems():        
        # how much money do you have spend?
        stockPrice = model.historicalPrices[0]
        quantity = int(money/stockPrice)
        if quantity > 0:
            p2 = copyPortfolio(p1, trainingSet)
            p2.addStock(ticker, quantity)
            p2.updateStatistics()
            tuple = (similiarity([idealVol, idealReturn], [p2.annualVol, p2.expectedReturn]), ticker, quantity)
            distances.append(tuple)
    distances.sort()
    
    if k > len(dataset):
        k = len(dataset)
        
    recommendedStocks = distances[0:k]
    return recommendedStocks

def testRecommendations(origPort, recommendations, idealPoint, k):
    
#    print 'Original'
    beforeDist = euclideanDistance((origPort.annualVol, origPort.expectedReturn), idealPoint)
    afterPort = copyPortfolio(origPort, testSet)
    afterPort.updateStatistics()
    afterDist = euclideanDistance((afterPort.annualVol, afterPort.expectedReturn), idealPoint)
#    print 'Before: ' + str(beforeDist)
#    print 'After: ' + str(afterDist)
#    print 'Diff:' + str(afterDist - beforeDist)
    
    origPortPoint = (beforeDist, afterDist)
    
    avgPreVA = 0.0
    avgPostVA = 0.0
    
    for beforeDist, ticker, quantity in recommendations:
        print ticker
        port = copyPortfolio(origPort, testSet)
        port.addStock(ticker, quantity)
        port.updateStatistics()
        afterDist = euclideanDistance((port.annualVol, port.expectedReturn), idealPoint) 
#        print 'Training: ' + str(beforeDist)
#        print 'Test: ' + str(afterDist)
#        print 'Diff:' + str(afterDist - beforeDist)
        recomPortPoint = (beforeDist, afterDist)
        
        for i in range(len(origPortPoint)):
            distance = (origPortPoint[i] - recomPortPoint[i]) * 10000
            if i == 0:
#                print 'Training value added: ' + str(distance) + ' bps'
#                avgPreVA += distance
                if distance > 0:
                    avgPreVA += 1
            else:
#                print 'Test value added: ' + str(distance) + ' bps'
#                avgPostVA += distance
                if distance > 0:
                    avgPostVA += 1
    
#    avgPreVA /= k
#    avgPostVA /= k
    return (avgPreVA, avgPostVA)

def evaluateRecommendations(iterations, k=5, idealVol=0.20, idealReturn=1.0, moneyToSpend=1000):
    f = open('performance.csv', 'w')
    f.write('iteration,volGap,pre-testVA,post-testVA\n')
    
    stocks = trainingSet.keys()
    accuracy = 0
    for i in range(iterations):
        
        data = [str(i)]
        portfolio = PortfolioModel(trainingSet)
        
        for j in range(7):
            quantity = random.randint(1, 20)
            ticker = random.choice(stocks)
            portfolio.addStock(ticker, quantity)

        portfolio.updateStatistics()
        print 'Holdings of portfolio: ' + str(portfolio.stocks)
        
        # applying a heuristic to thin out stocks with volatilites that are higher/lower than what we want it to be
        volGap = idealVol - portfolio.annualVol
        
        print "Volatility gap: " + str(volGap)
        data.append(str(volGap))
        
        thinSP = []
        if volGap > 0:
            thinSP = [(model.annualVol, ticker, model) for ticker, model in trainingSet.iteritems() if model.annualVol > portfolio.annualVol]
        elif volGap < 0:
            thinSP = [(model.annualVol, ticker, model) for ticker, model in trainingSet.iteritems() if model.annualVol < portfolio.annualVol]
        thinSP.sort()
        dataset = {item[1]: item[2] for item in thinSP}
        
        recommendedStocks = knn(dataset, portfolio, k, idealVol, idealReturn, moneyToSpend)
        print recommendedStocks
        
        preVA, postVA = testRecommendations(portfolio, recommendedStocks, (idealVol, 1), k)
        print postVA
#        if postVA > 0.5:
        
        accuracy += postVA
        
        data.append(str(preVA))
        data.append(str(postVA))
        
        f.write(",".join(data) + '\n')
    
    print 'Accuracy: ' + str(accuracy)
    accuracy /= (iterations*k)
    print 'Accuracy: ' + str(accuracy)
    
    f.close()    

# returns the number of lines in a file. From Stack Overflow: http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def initalizeData():
    path = 'data/'
    for infile in glob.glob( os.path.join(path, '*.csv') ):
        ticker = infile.split('/')[1].split('.')[0]
        length = file_len(infile)
        
        years = length/float(252)
        if years < 5:
            os.remove(infile)
            print 'Removed due to low data: ' + ticker
            
        else:
            # number of trading days in a year * 4 years (fudge factor)
            divisionPoint = length - 252*4
            
            trainingModel = StockModel(ticker, 0, divisionPoint)
            trainingSet[ticker] = trainingModel
            
            testModel = StockModel(ticker, divisionPoint)
            testSet[ticker] = testModel
            
#            print ticker
#            print 'training vol (annual): ' + str(trainingModel.annualVol)
#            print 'test vol (annual): ' + str(testModel.annualVol)
#            print 'training beta: ' + str(trainingModel.beta)
#            print 'test beta: ' + str(testModel.beta)
#            print 'training return (annual): ' + str(trainingModel.expectedReturn())
#            print 'test return (annual): ' + str(testModel.expectedReturn())

sp500 = StockModel('S+P')
initalizeData()

if __name__ == "__main__":
#    evaluateRecommendations(100, 5, 0.70)
    pass