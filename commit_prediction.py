
from matplotlib import pyplot
import numpy as np

import matplotlib.pyplot as plt

from statsmodels.tsa.arima_model import ARIMA #for time series analysis


def pred(l=[], *args):

	train=np.array(l, dtype=np.float)

	model = ARIMA(train, order=(5,1,0))

	model_fit = model.fit(disp=1) #model is prepared on the training data

	output = model_fit.forecast(25)

	#print(output[0])

	y=output[0]

	plt.plot(len(train)+np.arange(1,26),y, color='b')
        plt.xlabel("Weeks")
        plt.ylabel("Commits")

	plt.show()


#train=np.array([4, 16, 22, 32, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 36, 36, 44, 47, 47], dtype=np.float)

pred(train)  #passing a list containing commits history as parameter
