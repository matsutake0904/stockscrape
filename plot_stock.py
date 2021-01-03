import matplotlib.pyplot as plt
import numpy as np

path = "/Users/ryo/Documents/StockData/6502_2020-01-01to2020-12-30.csv"
data = np.loadtxt(path, delimiter=",", dtype="int64, U20, float, float, float, float,int64")
date=[]
data_np=np.zeros([len(data),len(data[0])-2])
for i in range(len(data)):
	date.append(data[i][1])
	for j in range(len(data[1])-2):
               data_np[i,j] = data[i][j+2]
plt.plot(date, data_np[:,0], label="open")
plt.plot(date, data_np[:,1], label="high")
plt.plot(date, data_np[:,2], label="low")
plt.plot(date, data_np[:,3], label="close")
plt.show()

print(data)
