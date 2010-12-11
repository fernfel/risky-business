from Tkinter import *
import ttk # support for Tkinter themed widgets

lastx, lasty = 0, 0

class GUI:
	def __init__(self):
		root = Tk()
		root.title("Test GUI")
		
		frame = ttk.Frame(root, padding="10 10 10 10")
		frame.grid(column=0, row=0, sticky=(N, W, E, S))
		
		# Tell the frame to expand automatically if resized by the user. DOESNT WORK?
		#frame.columnconfigure(0, weight=1)
		#frame.rowconfigure(0, weight=1)
		
		tabs = ttk.Notebook(frame)
		tabs.grid(column=1, row=1, sticky=(N, W))
		f1 = ttk.Frame(tabs); # first page, which would get widgets gridded into it
		# INSERT MATPLOTLIB GRAPHS HERE???
		f2 = ttk.Frame(tabs); # second page
		tabs.add(f1, text='Visualization One')
		tabs.add(f2, text='Visualization Two')
		
		self.canvas = Canvas(f1)
		self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))
		self.canvas.bind("<Button-1>", self.xy)
		self.canvas.bind("<B1-Motion>", self.addLine)
		
		
		self.feet = StringVar()
		self.meters = StringVar()
		
		feet_entry = ttk.Entry(frame, width=7, textvariable=self.feet)
		feet_entry.grid(column=3, row=1, sticky=(N, W, E))
		
		ttk.Label(frame, textvariable=self.meters).grid(column=3, row=1, sticky=(W, E))
		ttk.Button(frame, text="Calculate", command=self.calculate).grid(column=3, row=1, sticky=(S, W))
		
		ttk.Label(frame, text="feet").grid(column=4, row=1, sticky=NW)
		ttk.Label(frame, text="=").grid(column=2, row=1, sticky=E)
		ttk.Label(frame, text="meters").grid(column=4, row=1, sticky=W)
		
		# iterate over widgets that are children of frame, add padding around each
		for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)
		
		root.bind('<Return>', self.calculate)
		
		
		# Enter event loop (ie run the GUI)
		root.mainloop()
	
	def xy(self, event):
		global lastx, lasty
		lastx, lasty = event.x, event.y

	def addLine(self, event):
		global lastx, lasty
		self.canvas.create_line((lastx, lasty, event.x, event.y))
		lastx, lasty = event.x, event.y
		
	def calculate(self, *args):
		try:
			value = float(self.feet.get())
			self.meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
		except ValueError:
			pass
		
if __name__ == "__main__":
	g = GUI()
