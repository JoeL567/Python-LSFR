import matplotlib
from functools import partial
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import lsfrcalc
from tkinter import *
from tkinter.filedialog import askopenfilename

class lsfrApp(Tk):
    def __init__(self):
        super(lsfrApp,self).__init__()        #stack frames on top of each other in container
                                               #raise desired frame to top
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand = False)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #attributes to be set by the user
        self.fname = None
        self.xlabel = None
        self.ylabel = None
        
        self.frames = {}
        page_name = StartPage.__name__
        frame = StartPage(parent = self.container, controller = self)
        geometry = "340x350"
        self.frames[page_name] = (frame,geometry)
        frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame("StartPage")

    def create_gframe(self):
        page_name = PageOne.__name__
        frame = PageOne(parent = self.container, controller = self)
        geometry = "800x600"
        self.frames[page_name] = (frame,geometry)
        frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame("PageOne")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame,geometry = self.frames[page_name]
        #change geometry
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()

class StartPage(Frame):         #the first page

    def __init__(self, parent, controller):
        super(StartPage,self).__init__(parent)
        self.grid()
        self.fname = " "
        #greeting instructions
        self.label1 = Label(self, text="""Search for file to produce lsfr fitting:""")
        self.label1.grid(row = 0,column = 0, columnspan = 4,sticky = W)

        #cue for filename
        self.label2 = Label(self, text= "Filename:")
        self.label2.grid(row=1,column = 0, columnspan = 1,sticky=W)

        #text box to show filename
        self.filetext = Text(self,width = 28, height = 1, wrap = WORD)
        self.filetext.grid(row = 1, column = 1, columnspan = 5, sticky =W)

        filegetter = partial(self.getfile,controller)   #get function calls browse operation
        #browse button
        self.button4 = Button(self,text="browse",command = filegetter)
        self.button4.grid(row=2,column=4,sticky=E)

        #x-axis label and text box (row3 and 4)
        self.xlabel = Label(self, text = "x-axis label:")
        self.xlabel.grid(row=3,column = 0, sticky = W)
        self.xtext = Entry(self)
        self.xtext.grid(row=4, column=0,columnspan = 6,sticky = W)
        
        #y-axis label and text box (row 5 and 6)
        self.ylabel = Label(self, text = "y-axis label:")
        self.ylabel.grid(row=5,column = 0, sticky = W)
        self.ytext = Entry(self)
        self.ytext.grid(row=6, column=0,columnspan = 6,sticky = W)

        #empty line before outputs
        self.emptyline = Label(self,text=" ")
        self.emptyline.grid(row=7,column=0,sticky=W)
        
        #outputs for gradient and y-intercept
        self.gradlabel = Label(self,text = "Gradient:")
        self.gradlabel.grid(row=8,column=0,sticky=W)
        self.gradtext = Text(self, width = 10, height = 1, wrap=WORD)
        self.graderrtext = Text(self, width = 10, height = 1, wrap = WORD)
        self.plusminus = Label(self,text = "+/-")
        self.gradtext.grid(row=9,column=0,sticky=W)
        self.plusminus.grid(row=9,column=1,sticky=W)
        self.graderrtext.grid(row=9,column=2,sticky=W)

        self.inlabel = Label(self,text = "\ny-intercept:")
        self.inlabel.grid(row=10,column=0,sticky=W)
        self.intext = Text(self, width = 11, height = 1, wrap=WORD)
        self.inerrtext = Text(self, width = 11, height = 1, wrap = WORD)
        self.plusminus2 = Label(self,text = "+/-")
        self.intext.grid(row=11,column=0,sticky=W)
        self.plusminus2.grid(row=11,column=1,sticky=W)
        self.inerrtext.grid(row=11,column=2,sticky=W)

        #output chi-squared value
        self.chilabel = Label(self, text = "\nchi-squared value:")
        self.chilabel.grid(row=12,column = 0, sticky = W)
        self.chitext = Text(self, width = 11, height = 1, wrap=WORD)
        self.chitext.grid(row=13,column = 0,sticky = W)
        
        #view graph button
        graphview = partial(self.viewgraph,controller)
        self.button3 = Button(self, text="View Graph",command = graphview)
        self.button3.grid(row=15,column=4,sticky=E)

    def getfile(self,controller):
        self.fname = askopenfilename(initialdir = "C:/",title= "Select File",
                                     filetypes = (("csv files","*.csv"),("all files","*.*")))
        
        controller.fname = self.fname
        self.filetext.delete(0.0,END)
        self.filetext.insert(0.0,self.fname)

    def viewgraph(self,controller):
        if controller.fname == None:
            pass
        else:
            controller.xlabel = self.xtext.get()
            controller.ylabel = self.ytext.get()
            controller.create_gframe()

            values=lsfrcalc.data(controller.fname)
        
            self.gradtext.delete(0.0,END)
            self.graderrtext.delete(0.0,END)
            self.intext.delete(0.0,END)
            self.inerrtext.delete(0.0,END)
            self.chitext.delete(0.0,END)

            self.gradtext.insert(0.0,values.gradient())
            self.graderrtext.insert(0.0,values.graderr())
            self.intext.insert(0.0,values.intercept())
            self.inerrtext.insert(0.0,values.intercepterr())
            self.chitext.insert(0.0,values.chi2())
        
            controller.show_frame("PageOne")
        
class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Graph Page!")
        label.pack(pady=10,padx=10)        
        button1 = Button(self, text="Back to Home",
                         command=lambda: controller.show_frame("StartPage"))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        values=lsfrcalc.data(controller.fname)
        x = values.xdata
        y = values.ydata
        yerror = values.yerrdata
        a.errorbar(x,y,yerr=yerror,marker = "x",linestyle = "None",capsize = 5)

        #create fitting
        fit = [values.gradient()*i+values.intercept() for i in x]
        
        #plot fitting (need different plot styles depending on the value of redchi2
        if(values.redchi2() > 10):
            a.plot(x,fit,marker = None, linestyle = "--",color = "r")
            print("""WARNING: Reduced Chi squared value is very large. The uncertainties may have been underestimated or a linear fit is a poor choice.""")

        elif (values.redchi2() < 0.1):
            a.plot(x,fit,marker = None, linestyle = "--",color = "r")
            print("""WARNING: Reduced Chi squared value is very small. The uncertainties may have been overestimated or a linear fit is a poor choice.""")
        
        elif (values.redchi2() >1.5):
            a.plot(x,fit,marker = None, linestyle = "-",color = "y")
            print("""WARNING: Reduced Chi squared value is slightly outside the acceptable bounds. The uncertainties may have been underestimated.""")

        elif (values.redchi2() <0.5):
            a.plot(x,fit,marker = None, linestyle = "-",color = "y")
            print("""WARNING: Reduced Chi squared value is slightly outside the acceptable bounds. The uncertainties may have been overestimated.""")

        else:
            a.plot(x,fit,marker = None, linestyle = "-",color = "b")
        a.set_xlabel(controller.xlabel)
        a.set_ylabel(controller.ylabel)
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        
app = lsfrApp()
app.title("lsfr fitting")
app.mainloop()
