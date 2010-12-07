# Get some yahoo finance yays

import urllib2
from BeautifulSoup import BeautifulSoup
	

if __name__ == "__main__":
	file = open("S+P.txt")
	tickerList = list()
	while 1:
		line = file.readline()
		if not line:
			break
		tickerList.append(line.strip())	
	file.close()
	
	for ticker in tickerList:
		print ticker
		url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker+"&a=00&b=1&c=1980&d=11&e=6&f=2010&g=d&ignore=.csv"
		data = urllib2.urlopen(url)
		url2 = "http://finance.yahoo.com/q/ks?s="+ticker+"+Key+Statistics"
		page = urllib2.urlopen(url2)
		soup = BeautifulSoup(page)
		data = soup.findAll("td", "yfnc_tabledata1")
		beta =  data[31].text
		
		
		file = open("data/"+ticker+'.csv', 'w')
		
		file.write(beta)
		file.write(data.read())
		file.close()