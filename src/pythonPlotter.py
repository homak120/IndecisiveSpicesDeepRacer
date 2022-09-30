import numpy as np
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker
from matplotlib.widgets import Button

img_array = np.load('2022_march_pro.npy')

# PLot
waypointsXInner =[]
waypointsYInner =[]

waypointsXCenter =[]
waypointsYCenter =[]

waypointsXOuter =[]
waypointsYOuter =[]

data = np.load('2022_march_pro.npy')
for points in data:
	for index, point in enumerate(points):
		if index == 0 :
			waypointsXCenter.append(point)
		elif index == 1 :
			waypointsYCenter.append(point)
		elif index == 2 :
			waypointsXInner.append(point)
		elif index == 3 :
			waypointsYInner.append(point)
		elif index == 4 :
			waypointsXOuter.append(point)
		elif index == 5 :
			waypointsYOuter.append(point)

fig, ax = plt.subplots()
ax.scatter(waypointsXCenter,waypointsYCenter, color ='red', s=4)
plt.plot(waypointsXInner,waypointsYInner, color ='black')
plt.plot(waypointsXCenter,waypointsYCenter, color='orange')
plt.plot(waypointsXOuter,waypointsYOuter, color ='black')
klicker = clicker(ax, ["event"], markers=["x"])

# function to save to file
def add(val):
	fileName = input("Enter File Name to Save to: ")
	with open(fileName+'.txt', 'w') as f:
		f.writelines(str(klicker.get_positions()))
	print("Waypoints Saved")
 
axes = plt.axes([0.81, 0.000001, 0.1, 0.075])
bnext = Button(axes, 'Save',color="#97FFFF")
bnext.on_clicked(add)

plt.show()