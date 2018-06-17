#lsfr calculator
#imports csv data in form x,y,erry and calculates the lsfr fit and errors
import csv
import numpy as np

def reciprocal_sq(alist):
    """returns the sum of 1/i**2 in the list"""
    return sum(1/i**2 for i in alist)

def mean(x,errx=0):
    try:
        a=0
        b=0
        for i in zip(x,errx):
            a+= i[0]/(i[1]**2)
            b+= 1/(i[1]**2)
        return a
    except:
        return np.mean(x)

        
class data:
    """a class to contain the x, y and xyerr data from a csv file"""
    def __init__(self,filename):
        self.filename = filename        #filename attribute
        self.data = self.get_data()     #data attributes
        self.xdata = self.data[0]
        self.ydata = self.data[1]
        self.yerrdata = self.data[2]

        self.m_x = mean(self.xdata,self.yerrdata)                               #<x> = sum(x_i/e_i**2)
        self.m_y = mean(self.ydata,self.yerrdata)                               #<y>
        self.m_xy = mean(np.multiply(self.xdata,self.ydata),self.yerrdata)      #<xy> 
        self.m_xpow2 = mean(np.multiply(self.xdata,self.xdata),self.yerrdata)   #<x^2>
        #self.redchi2 = self.chi2()/(len(self.ydata)-2)          #reduced chi squared value

        self.e_sq_reciprocal = reciprocal_sq(self.yerrdata)         # sum(1/e_i**2)
        
    def get_data(self):
        """collect data from file and put into lists"""
        x=[]
        y=[]
        yerr=[]
        results=[]
        with open(self.filename,"r") as csvfile:
            data=csv.reader(csvfile)
            for row in data:
                x.append(float(row[0]))
                y.append(float(row[1]))
                yerr.append(float(row[2]))
        results.append(x)
        results.append(y)
        results.append(yerr)
        return results

    #need to calculate the fittings for y = mx+c
    #need to find estimate for m and c
    def gradient(self): 
        a = self.m_x*self.m_y-self.m_xy*reciprocal_sq(self.yerrdata)
        b = self.m_x**2-self.m_xpow2*reciprocal_sq(self.yerrdata)
        return a/b
    
    def intercept(self):
        a = self.m_x*self.m_xy - self.m_y*self.m_xpow2
        b = self.m_x**2 - self.m_xpow2*reciprocal_sq(self.yerrdata)
        return a/b

    def graderr(self):      
        a = self.e_sq_reciprocal
        b = self.m_xpow2 * self.e_sq_reciprocal - self.m_x**2
        return np.sqrt(a/b)

    def intercepterr(self):
        a = self.m_xpow2
        b = self.m_xpow2 * self.e_sq_reciprocal - self.m_x**2
        return np.sqrt(a/b)

    def chi2(self):         #returns the chi squared value https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic#Definition
        a = 0
        for i in range(len(self.ydata)):
            observed = self.ydata[i]
            expected = self.gradient()*self.xdata[i]+self.intercept()
            a+= ((observed - expected)/self.yerrdata[i])**2
        return a

    def redchi2(self):
        return self.chi2()/(len(self.ydata)-2)
