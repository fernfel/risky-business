# Get some yahoo finance yays

import urllib2

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
	url = "http://ichart.finance.yahoo.com/table.csv?s="+ticker+"&a=00&b=1&c=1990&d=11&e=6&f=2010&g=d&ignore=.csv"
	page = urllib2.urlopen(url)
	file = open("data/"+ticker+'.csv', 'w')
	file.write(page.read())
	file.close()