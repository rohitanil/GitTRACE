import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt




def show_plot(dates,commits):
	linear_mod = linear_model.LinearRegression()
	dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
	commits = np.reshape(commits,(len(commits),1))
	linear_mod.fit(dates,commits) #fitting the data points in the model
	"""plt.scatter(dates,commits,color='yellow') #plotting the initial datapoints 
	plt.plot(dates,linear_mod.predict(dates),color='blue',linewidth=1) #plotting the line made by linear regression
	plt.show()"""
	return

def predict_commits(dates,commits,x):
	linear_mod = linear_model.LinearRegression() #defining the linear regression model
	dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
	commits = np.reshape(commits,(len(commits),1))
	linear_mod.fit(dates,commits) #fitting the data points in the model
	predicted_commits =linear_mod.predict(x)
	return predicted_commits[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]



 


  
