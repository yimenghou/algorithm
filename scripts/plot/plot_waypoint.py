import pylab as plt
from scipy import signal

filePath = "/media/yimeng/0ade5f79-daf5-43f5-9b3f-fbad02d13a32/dataset/rosbag/2017-04-21_parking_lot/waypoints/waypoints_outdoor0421.txt"
filterCurve = True

def LPFilter(x,y):

	order = 2 # low pass filter order
	stopBandAttenuation = 10 # in dB unit
	passBandCutOffFreq = 0.1 # in normalized frequency scale

	b, a = signal.butter(order, passBandCutOffFreq)
	y_flt = signal.filtfilt(b, a, y)
	x_flt = signal.filtfilt(b, a, x)

	return x_flt, y_flt

with open(filePath) as f:
    content = f.readlines()

pose_x = []
pose_y = []

for line in enumerate(content):

	if line[0] == 0:
		continue
	waypoint_temp = line[1].strip().split(' ')
	pose_x.append(float(waypoint_temp[0]))
	pose_y.append(float(waypoint_temp[1]))

if filterCurve:
	pose_x, pose_y = LPFilter(pose_x, pose_y)

plt.figure()
plt.plot(pose_x, pose_y, 'b', pose_x[0], pose_y[0], 'rx', pose_x[-1], pose_y[-1], 'ro')
plt.show()