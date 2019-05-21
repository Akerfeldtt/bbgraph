

# File has to have 3 headers at the top, and line of text on the bottom (fix this)



#------------------------------------------------------------------------------#

# Loop over lines and extract variables of interest
# Essentially just taking each column and making it a list for data analysis
def grabdata(f):
    E=[]; dE=[];F=[];dF=[];mF=[];dmF=[];M=[]
    alpha=[E,dE,F,dF,mF,dmF,M]
    for line in f:
        #print "hello world"
        #print line
        line = line.strip()
        columns = line.split()
        #print columns
        for i in range(len(columns)):
            #alpha[i]
            #print alpha[i]
            try:
                alpha[i].append(float(columns[i]))
            except:
                if columns[i]!="NO":
                    alpha[i].append(columns[i])
                else:
                    pass

    return E,dE,F,dF,mF
def filegrab(file):    
    #file = raw_input("Enter the BAT_lc qdp file: ");
    # Open file
    BAT = open(file, 'r')
    header1 = BAT.readline()
    header1 = BAT.readline()
    header1 = BAT.readline()
    BATdata = grabdata(BAT)
    E = BATdata[0]
    dE = BATdata[1]
    F = BATdata[2]
    dF = BATdata[3]
    mF = BATdata[4]

    
    return E,dE,F,dF,mF
#func's above just grabing each column of 14 columns.
#want it all on the graph so...

def grabdata2(f):
    E=[]; dE=[];F=[];dF=[]
    alpha=[E,dE,F,dF]
    for line in f:
        #print "hello world"
        #print line
        line = line.strip()
        columns = line.split()
        #print columns
        for i in range(len(columns)):
            #alpha[i]
            #print alpha[i]
            try:
                alpha[i].append(float(columns[i]))
            except:
                if columns[i]!="NO":
                    alpha[i].append(columns[i])
                else:
                    pass
    return E,dE,F,dF
def filegrab2(file):    
    #file = raw_input("Enter the BAT_lc qdp file: ");
    # Open file
    BAT = open(file, 'r')
    header1 = BAT.readline()
    header1 = BAT.readline()
    header1 = BAT.readline()
    BATdata = grabdata(BAT)
    E = BATdata[0]
    dE = BATdata[1]
    F = BATdata[2]
    dF = BATdata[3]

    
    return E,dE,F,dF



def main(file1,file2,file3,file4,numberwang,N,kt,GRB,name):

	import matplotlib
	matplotlib.use('agg')
	import matplotlib.pyplot as plt
	import os
	import numpy as np
	import sys, os

	lol = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	#file1='plotpoints.txt'
	#file2='plotpoints_noabs.txt'
	#file3='ratio.txt'
	#file4='ratio2.txt'
	file=file1
	E,dE,F,dF,mF = filegrab(file)	#plotpoints
	file=file2
	E1,dE1,F1,dF1,mF1 = filegrab(file)#plotpointsnoabs
	file=file3
	E2,dE2,F2,dF2 = filegrab2(file)#ratio
	file=file4
	E3,dE3,F3,dF3 = filegrab2(file)#ratio2
	print E
	print E2
	print mF
	print F2
	
	E=[i*4.1357e-18 for i in E]
	dE=[i*4.1357e-18 for i in dE]
	E1=[i*4.1357e-18 for i in E1]
	dE1=[i*4.1357e-18 for i in dE1]
	plt.figure()
	plt.xscale('log')
	plt.yscale('log')
	plt.minorticks_on()
	plt.tick_params('both', length=20, width=2, which='major')
	plt.tick_params('both', length=10, width=1, which='minor')
	plt.tick_params(axis='y', labelsize=40)
	plt.tick_params(axis= 'x', labelsize=40)
	plt.ylabel(r"$\mathrm{EF_{E}\,(erg\,cm^{-2}\,s^{-1})}$",fontsize=40)    
	plt.xlabel(r"$\mathrm{Energy\,(keV)}$",fontsize=40)
	plt.subplots_adjust(bottom=0.25)  
	plt.subplots_adjust(left=0.24)  
	plt.xlim([1e-1,10])
	plt.ylim([1e-11,1e-6])
	plt.yticks([1e-16,1e-14,1e-12,1e-10,1e-8,1e-6])
	plt.xticks([1e-3,1e-2,1e-1,1])
	dFF=[i*1.60218e-9 for i in dF]
	FF=[i*1.60218e-9 for i in F]
	EE=[i/4.1357e-18 for i in E]
	dEE=[i/4.1357e-18 for i in dE]
	plt.errorbar(EE,FF,dFF,dEE,capsize=1, ls='none',elinewidth=0.7,color='royalblue')
	plt.scatter(EE,FF,color='royalblue')
	

	ratofrat=[]
	ratofraterr=[]
	for i in range(len(F2)):
		a=F2[i]/F3[i]
		ratofrat.append(a)
		b=np.sqrt((dF3[i])**2 + (dF2[i])**2)
		ratofraterr.append(b)

	y=[]
	yerr=[]
	for i in range(len(F)):
		a=F[i]*ratofrat[i]
		b=dF[i]*ratofrat[i]
		y.append(a)
		yerr.append(b)

	modelabs=[]
	for i in range(len(E)):
		a=F[i]/F2[i]
		modelabs.append(a)
	#plt.plot(E,modelabs,color='blue',linewidth=3)

	modelnoabs=[]
	for i in range(len(E)):
		a=F1[i]/F3[i]
		modelnoabs.append(a)

	#plt.plot(E,modelnoabs,color='red',linewidth=3)

	MM=[]
	MMerr=[]
	for i in range(len(modelnoabs)):
		a=modelnoabs[i]*F2[i]*1.60218e-9
		MM.append(a)
		b=modelnoabs[i]*dF2[i]*1.60218e-9
		MMerr.append(b)
	
	plt.errorbar(EE,MM,MMerr,dEE,capsize=1, ls='none',elinewidth=0.7,color='firebrick')
	plt.scatter(EE,MM,color='firebrick')


	file=file1
	#E,dE,F,dF,mF = filegrab(file)	#plotpoints
	Y=[]
	Y2=[]
	P=2.49682
	PN=7.61657e-7
	E=np.linspace(0.001,10,10000)

	def bkpw(Xs,a1,a2,t1,n):
	  y = []
	  for x in Xs:
	    if x<t1: y.append(n*x**(2-a1))
	    else: y.append(n*(t1**(a2-a1))*(x**(2-a2)))
	  if len(y) == 1: y=y[0] # in case we're analyzing a single point. Kludgy?
	  return y
	'''
	for i in range(len(E)):
		a=(N*(1.0344e-3)*(E[i]**4))/(np.exp(E[i]/kt) - 1)
		Y.append(a)

	for i in range(len(E)):
		a=(PN*(E[i]**(2-P)))
		Y2.append(a)
	'''
	#1400.0&   $0.043523\pm0.002192&   $8.691E+14\pm1.325E+14&   $0.0\pm0.0&   $0.0\pm0.0&    139.17/91.0
	'''	

	   1    1   powerlaw   PhoIndex            1.56681      +/-  5.81775E-03  
	   2    1   powerlaw   norm                1.88087      +/-  1.99093E-02  
	   3    2   zbbody     kT         keV      3.26764E-02  +/-  1.65047E-03  
	   4    2   zbbody     Redshift            0.340000     frozen
	   5    2   zbbody     norm                14.7955      +/-  2.22476  
	'''

	P=1.59999
	PN=0.161941
	
	for i in range(len(E)):
		a=(PN*(E[i]**(2-P)))
		Y2.append(a)

	kt=0.117032
	N=1.96146e-3
	z=3.68e-2
	for i in range(len(E)):
		a=( N*(8.0525)*(E[i]**2)*(E[i]*(1+z))**2 )/((1+z)*(kt**4) * ( np.exp((E[i]*(1+z))/kt) - 1   )   )
		Y.append(a)
	print Y
	#E=[i/4.1357e-18 for i in E]
	Y=[1.60218e-9*i for i in Y]
	Y2=[1.60218e-9*i for i in Y2]
	plt.plot(E,Y,c='g',linestyle='-')
	plt.plot(E,Y2,c='magenta',linestyle='--')
	from operator import add
	Y3=list( map(add, Y, Y2) )
	plt.plot(E,Y3,c='black',linestyle='-')
	print 'SED'+str(numberwang)+'.png'
	#plt.savefig('SED'+str(numberwang)+'.png', bbox_inches='tight')
	plt.show()
	
if __name__ =="__main__":
	import sys
	import matplotlib.pyplot as plt
	file1=sys.argv[1]
	file2=sys.argv[2]
	file3=sys.argv[3]
	file4=sys.argv[4]
	numberwang=sys.argv[5]
	N=float(sys.argv[6])
	kt=float(sys.argv[7])
	GRB=sys.argv[8]
	name=sys.argv[9]
	main(file1,file2,file3,file4,numberwang,N,kt,GRB,name)
	plt.show()








