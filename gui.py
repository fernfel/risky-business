from Tkinter import *
import tkFileDialog
import ttk # support for Tkinter themed widgets

lastx, lasty = 0, 0

class StartScreen:
	def __init__(self):
		self.filepath = None
	
		self.window = Tk()
		self.window.title("Title Goes Here")
		self.window.geometry('600x300+150+130')
		self.window.resizable(FALSE,FALSE)
		
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
		print "Risk Value: " + self.risk_value.get()
		print "Max amount per company: " + str(self.dollars.get()) + "." + str(self.cents.get())
		print "File: " + self.filepath
		GUI(self.risk_value, self.dollars, self.cents, self.filepath)

class GUI:
	def __init__(self, riskVal, d, c, f):
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
		# INSERT MATPLOTLIB GRAPHS HERE???
		f2 = ttk.Frame(tabs); # second page
		tabs.add(f1, text='Portfolio Dashboard')
		tabs.add(f2, text='Stock Recommender')
		
		self.canvas = Canvas(f1)
		self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
		self.canvas.bind("<Button-1>", self.xy)
		self.canvas.bind("<B1-Motion>", self.addLine)
		
		stat_frame = ttk.Frame(window, padding="10 10 10 10")
		stat_frame.grid(column=1, row=0, sticky=(N, W, E, S))
		lf = ttk.Labelframe(stat_frame, text='Key Statistics', padding="10 10 10 10")
		lf.grid(column=0, row=0, sticky=(N, W, E, S))
		
		self.feet = StringVar()
		self.meters = StringVar()
		
		feet_entry = ttk.Entry(lf, width=7, textvariable=self.feet)
		feet_entry.grid(column=2, row=1, sticky=(N, W, E))
		
		ttk.Label(lf, textvariable=self.meters).grid(column=2, row=1, sticky=(W, E))
		ttk.Button(lf, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=(S, W))
		
		ttk.Label(lf, text="feet").grid(column=3, row=0, sticky=NW)
		ttk.Label(lf, text="=").grid(column=1, row=1, sticky=E)
		ttk.Label(lf, text="meters").grid(column=3, row=2, sticky=W)
		
		# iterate over widgets that are children of frame, add padding around each
		for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)
		
		window.bind('<Return>', self.calculate)
		
		
		# Enter event loop (ie run the GUI)
		window.mainloop()
	
	def xy(self, event):
		global lastx, lasty
		lastx, lasty = event.x, event.y

	def addLine(self, event):
		global lastx, lasty
		self.canvas.create_line((lastx, lasty, event.x, event.y))
		lastx, lasty = event.x, event.y
		
	def calculate(self):
		try:
			value = float(self.feet.get())
			self.meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
		except ValueError:
			pass
		
if __name__ == "__main__":
	#StartScreen()
	GUI(4, 122, 9, "file/path/test")