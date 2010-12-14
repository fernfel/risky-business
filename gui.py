import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Tkinter import *
import tkFileDialog
import ttk # support for Tkinter themed widgets
import os, glob
import mpt, getData, summaryVis
import interactivePlot

lastx, lasty = 0, 0

class StartScreen:
	def __init__(self):
		self.filepath = None
	
		self.window = Tk()
		self.window.title("Welcome to Risky Business")
		self.window.resizable(FALSE,FALSE)
		
		frame = ttk.Frame(self.window, padding="10 10 10 10")
		frame.grid(column=0, row=0, sticky=(N, W, E, S))
		
		self.lf1 = ttk.Labelframe(frame, text='Step 1')
		self.lf1.grid(column=1, row=1, sticky=EW)
		ttk.Label(self.lf1, text="On a scale of 1 to 5, rate your personal risk tolerance:   ").grid(column=1, row=0, sticky=W)
		self.risk_value = StringVar()
		one = ttk.Radiobutton(self.lf1, text='1   ', variable=self.risk_value, value='1')
		one.grid(column=2, row=0, sticky=E)
		two = ttk.Radiobutton(self.lf1, text='2   ', variable=self.risk_value, value='2')
		two.grid(column=3, row=0, sticky=E)
		three = ttk.Radiobutton(self.lf1, text='3   ', variable=self.risk_value, value='3')
		three.grid(column=4, row=0, sticky=E)
		four = ttk.Radiobutton(self.lf1, text='4   ', variable=self.risk_value, value='4')
		four.grid(column=5, row=0, sticky=E)
		five = ttk.Radiobutton(self.lf1, text='5', variable=self.risk_value, value='5')
		five.grid(column=6, row=0, sticky=E)
		
		self.lf2 = ttk.Labelframe(frame, text='Step 2')
		self.lf2.grid(column=1, row=2, sticky=EW)
		ttk.Label(self.lf2, text="What is the most you are willing to invest in one company?   ").grid(column=1, row=0, sticky=E)
		ttk.Label(self.lf2, text="$").grid(column=2, row=0, sticky=E)
		self.dollars = IntVar()
		dollars_entry = ttk.Entry(self.lf2, width=7, textvariable=self.dollars)
		dollars_entry.grid(column=3, row=0, sticky=E)
		
		self.lf3 = ttk.Labelframe(frame, text='Step 3')
		self.lf3.grid(column=1, row=3, sticky=EW)
		self.browse_button = ttk.Button(self.lf3, text="Browse for your portfolio .csv file", command=self.browse)
		self.browse_button.grid(column=0, row=0, sticky=NE)
		
		ttk.Button(frame, text="Submit", command=self.upload).grid(column=3, row=4, sticky=(S, W))
		
		self.window.mainloop()
		
	def browse(self):
		self.filepath = tkFileDialog.askopenfilename()
		self.browse_button.destroy()
		ttk.Label(self.lf3, text=self.filepath).grid(column=0, row=0, sticky=E)
		
	def upload(self):
		#DEAL WITH INPUT HERE. VALIDATE INPUTS, GIVE MESSAGE BOX IF INVALID, return.
		self.window.destroy()
		if self.risk_value.get() == "":
			GUI("3", self.dollars.get(), self.filepath) # default risk value to 3 if none given.
		else:	
			GUI(self.risk_value.get(), self.dollars.get(), self.filepath)

class GUI:
	def __init__(self, riskVal, d, f):
		self.riskVal = (float(riskVal) * 20 - 10)/100
		self.d = d
		portfolioDict = self.readPortfolio(f)	
		
		path = 'data/'
		for infile in glob.glob( os.path.join(path, '*.csv') ):
			ticker = infile.split('/')[1].split('.')[0]
			stockModel = mpt.StockModel(ticker)
			
			years = len(stockModel.historicalPrices)/float(252)
			if years < 5:
				os.remove(infile)
				print 'Removed due to low data: ' + ticker
				
			else:
				# number of trading days in a year * 4 years (fudge factor)
				divisionPoint = len(stockModel.historicalPrices) - 252*4
				
				trainingModel = mpt.StockModel(ticker, 0, divisionPoint)
				mpt.trainingSet[ticker] = trainingModel
		
		self.portfolio = mpt.PortfolioModel(mpt.trainingSet)
		
		
		for k, v in portfolioDict.iteritems():
			self.portfolio.addStock(k, int(v))
		self.portfolio.updateStatistics()	
		risk = self.portfolio.annualVol
	
		window = Tk()
		window.title("Test GUI")
		#window.geometry('1100x600+150+130')
		window.resizable(FALSE,FALSE)
		
		frame = ttk.Frame(window, padding="10 10 10 10")
		frame.grid(column=0, row=0, sticky=(N, W, E, S))
		
		# Tell the frame to expand automatically if resized by the user. DOESNT WORK?
		#frame.columnconfigure(0, weight=1)
		#frame.rowconfigure(0, weight=1)
		
		tabs = ttk.Notebook(frame)
		tabs.grid(column=1, row=1, sticky=(N, W))
		
		self.f1 = ttk.Frame(tabs); # first page, which would get widgets gridded into it
		tabs.add(self.f1, text='Portfolio Dashboard')
		self.fig1 = summaryVis.getGraph(self.portfolio, self.f1)
		canvas1 = FigureCanvasTkAgg(self.fig1, master=self.f1)
		canvas1.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S))
		canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		canvas1._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
		canvas1.show()
		
		self.f2 = ttk.Frame(tabs); # second page
		tabs.add(self.f2, text='Stock Recommender')
#		self.canvas2 = Canvas(self.f2)
#		self.canvas2.grid(column=0, row=0, sticky=(N, W, E, S))
#		self.canvas2.bind("<Button-1>", self.xy)
#		self.canvas2.bind("<B1-Motion>", self.addLine)
		
		recommendations = mpt.knn(mpt.trainingSet, self.portfolio, 5, self.riskVal, 1, self.d)
		self.recommendDict = dict()
		
		for beforeDist, ticker, quantity in recommendations:
			newPort = mpt.copyPortfolio(self.portfolio, mpt.testSet)
			newPort.addStock(ticker, quantity)
			newPort.updateStatistics()
			self.recommendDict[ticker] = newPort
        	
		self.fig2 = interactivePlot.getInteractiveGraph(self.f2, self.portfolio, recommendDict, "<Button-1>", self.riskVal)
#		recommendedFrame = ttk.Frame(self.f2)
#		recommendedFrame.grid(column=0, row=1, sticky=(N, W, E, S))
		canvas2 = FigureCanvasTkAgg(self.fig2, master=self.f2)
		canvas2.get_tk_widget().grid(column=0, row=0, sticky=(N, W, E, S))
#		canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
#		canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
		canvas2.show()
				
		detail_frame = ttk.Frame(self.f2, padding="10 10 10 10")
		detail_frame.grid(column=0, row=1, sticky=(N, W, E, S))
		details = ttk.Label(detail_frame, text='Some Details about the selected stock...')
		details.grid(column=0, row=0, sticky=(N, W, E, S))

		m = 3
		for beforeDist, ticker, quantity in recommendations:
			ttk.Button(detail_frame, text="Add "+ticker+" to Portfolio", command=lambda n=ticker, q=quantity: self.add(n, q)).grid(column=0, row=m, sticky=SE)
			m+=1
		
		stat_frame = ttk.Frame(window, padding="10 10 10 10")
		stat_frame.grid(column=1, row=0, sticky=(N, W, E, S))
		lf = ttk.Labelframe(stat_frame, text='Key Statistics', padding="10 10 10 10")
		lf.grid(column=0, row=0, sticky=(N, W, E, S))
		
		ttk.Label(lf, text="Target Risk: ").grid(column=0, row=0, sticky=W)
		ttk.Label(lf, text=self.riskVal).grid(column=1, row=1, sticky=E)
		ttk.Label(lf, text="Calculated Risk: ").grid(column=0, row=2, sticky=W)
		self.calc = ttk.Label(lf, text=risk)
		self.calc.grid(column=0, row=3, sticky=E)
		ttk.Label(lf, text="File: ").grid(column=0, row=4, sticky=W)
		ttk.Label(lf, text=f).grid(column=0, row=5, sticky=E)
		
		# iterate over widgets that are children of frame, add padding around each
		for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)
		
		# Enter event loop (ie run the GUI)
		window.mainloop()
	
	def add(self, ticker, quantity):
		print "added " + ticker
		self.portfolio.addStock(ticker, quantity)
		self.portfolio.updateStatistics()
		risk = self.portfolio.annualVol
		self.calc = ttk.Label(lf, text=risk)
		self.fig1 = summaryVis.getGraph(self.portfolio, self.f1)
		recommendations = mpt.knn(mpt.trainingSet, self.portfolio, 5, self.riskVal, 1, self.d)
		self.recommendDict = dict()
		
		for beforeDist, ticker, quantity in recommendations:
			newPort = mpt.copyPortfolio(self.portfolio, mpt.testSet)
			newPort.addStock(ticker, quantity)
			newPort.updateStatistics()
			self.recommendDict[ticker] = newPort
		self.fig2 = interactivePlot.getInteractiveGraph(self.f2, self.portfolio, self.recommendDict, "<Button-1>", self.riskVal)
		
		
		
	def readPortfolio(self, filePath):
		portfolio = dict()
		spSet =  getData.spList()
		f = open(filePath)
		lines = f.readlines()
		for i in range(1, len(lines)):
			line = lines[i].strip()
			ticker,quantity = line.strip().split(',')
			if ticker in spSet: #TODO: account for upper vs lowercase tickers
				portfolio[ticker] = quantity
			else: 
				print "Unfortunately, " + str(ticker) + " is not in our data set."
		return portfolio
		
if __name__ == "__main__":
#	StartScreen()
	GUI(4, 500, "jeff_profile.csv")