from Tkinter import *
import tkFileDialog
import ttk # support for Tkinter themed widgets
import mpt, getData

lastx, lasty = 0, 0

class StartScreen:
	def __init__(self):
		self.filepath = None
	
		self.window = Tk()
		self.window.title("Title Goes Here")
		self.window.geometry('800x400+150+130')
		#self.window.resizable(FALSE,FALSE)
		
		frame = ttk.Frame(self.window, padding="10 10 10 10")
		frame.grid(column=0, row=0, sticky=(N, W, E, S))
		
		# Purpose?
		#frame.columnconfigure(0, weight=1)
		#frame.rowconfigure(0, weight=1)
		
		self.lf1 = ttk.Labelframe(frame, text='Step 1')
		self.lf1.grid(column=1, row=1, sticky=EW)
		ttk.Label(self.lf1, text="Enter your personal risk tolerance:").grid(column=1, row=0, sticky=E)
		self.risk_value = StringVar()
		one = ttk.Radiobutton(self.lf1, text='1   ', variable=self.risk_value, value='1')
		one.grid(column=1, row=1, sticky=E)
		two = ttk.Radiobutton(self.lf1, text='2   ', variable=self.risk_value, value='2')
		two.grid(column=2, row=1, sticky=E)
		three = ttk.Radiobutton(self.lf1, text='3   ', variable=self.risk_value, value='3')
		three.grid(column=3, row=1, sticky=E)
		four = ttk.Radiobutton(self.lf1, text='4   ', variable=self.risk_value, value='4')
		four.grid(column=4, row=1, sticky=E)
		five = ttk.Radiobutton(self.lf1, text='5', variable=self.risk_value, value='5')
		five.grid(column=5, row=1, sticky=E)
		
		self.lf2 = ttk.Labelframe(frame, text='Step 2')
		self.lf2.grid(column=1, row=2, sticky=EW)
		ttk.Label(self.lf2, text="What is the most you would spend towards one company?").grid(column=1, row=0, sticky=E)
		ttk.Label(self.lf2, text="$").grid(column=1, row=1, sticky=E)
		self.dollars = IntVar()
		dollars_entry = ttk.Entry(self.lf2, width=7, textvariable=self.dollars)
		dollars_entry.grid(column=2, row=1, sticky=E)
		ttk.Label(self.lf2, text=".").grid(column=3, row=1, sticky=E)
		self.cents = IntVar()
		cents_entry = ttk.Entry(self.lf2, width=2, textvariable=self.cents)
		cents_entry.grid(column=4, row=1, sticky=E)
		
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
		GUI(self.risk_value.get(), self.dollars.get(), self.cents.get(), self.filepath)

class GUI:
	def __init__(self, riskVal, d, c, f):
		portfolio = self.readPortfolio(f)	
	
		window = Tk()
		window.title("Test GUI")
		window.geometry('1100x600+150+130')
		window.resizable(FALSE,FALSE)
		
		frame = ttk.Frame(window, padding="10 10 10 10")
		frame.grid(column=0, row=0, sticky=(N, W, E, S))
		
		# Tell the frame to expand automatically if resized by the user. DOESNT WORK?
		#frame.columnconfigure(0, weight=1)
		#frame.rowconfigure(0, weight=1)
		
		tabs = ttk.Notebook(frame)
		tabs.grid(column=1, row=1, sticky=(N, W))
		
		f1 = ttk.Frame(tabs); # first page, which would get widgets gridded into it
		tabs.add(f1, text='Portfolio Dashboard')
		
		f2 = ttk.Frame(tabs); # second page
		tabs.add(f2, text='Stock Recommender')
		self.canvas = Canvas(f2)
		self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
		self.canvas.bind("<Button-1>", self.xy)
		self.canvas.bind("<B1-Motion>", self.addLine)
		detail_frame = ttk.Frame(f2, padding="10 10 10 10")
		detail_frame.grid(column=0, row=1, sticky=(N, W, E, S))
		details = ttk.Label(detail_frame, text='Some Details about the selected stock...')
		details.grid(column=0, row=0, sticky=(N, W, E, S))
		add = ttk.Button(detail_frame, text="Add to Portfolio", command=self.add)
		add.grid(column=0, row=2, sticky=SE)
		
		
		stat_frame = ttk.Frame(window, padding="10 10 10 10")
		stat_frame.grid(column=1, row=0, sticky=(N, W, E, S))
		lf = ttk.Labelframe(stat_frame, text='Key Statistics', padding="10 10 10 10")
		lf.grid(column=0, row=0, sticky=(N, W, E, S))
		
		ttk.Label(lf, text="Target Risk: ").grid(column=0, row=0, sticky=W)
		ttk.Label(lf, text=riskVal).grid(column=1, row=1, sticky=E)
		ttk.Label(lf, text="Calculated Risk: ").grid(column=0, row=2, sticky=W)
		ttk.Label(lf, text="blah").grid(column=0, row=3, sticky=E)
		ttk.Label(lf, text="File: ").grid(column=0, row=4, sticky=W)
		ttk.Label(lf, text=f).grid(column=0, row=5, sticky=E)
		
		# iterate over widgets that are children of frame, add padding around each
		for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)
		
		# Enter event loop (ie run the GUI)
		window.mainloop()
	
	def xy(self, event):
		global lastx, lasty
		lastx, lasty = event.x, event.y

	def addLine(self, event):
		global lastx, lasty
		self.canvas.create_line((lastx, lasty, event.x, event.y))
		lastx, lasty = event.x, event.y
		
	def add(self):
		print "added"
		
	def readPortfolio(self, filePath):
		portfolio = dict()
		spSet =  getData.spList()
		f = open(filePath)
		lines = f.readlines()
		for x in range(1, len(lines)):
			line = lines[x].strip()
			ticker,quantity = line.strip().split(',')
			if ticker in spSet: #TODO: account for upper vs lowercase tickers
				portfolio[ticker] = quantity
				print ticker
		return portfolio
		
if __name__ == "__main__":
	StartScreen()
	#GUI(4, 122, 9, "file/path/test")