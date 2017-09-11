import pylab as plt
import multiprocessing

def pointFlt(x, y, s):
	x /= 100
	y/= 100
	if abs(x) > 180 or abs(x) == 0 or abs(y) > 90 or abs(y) == 0:
		pass
	else:
		if s == 4:
			return 0
		else:
			return 1

def plotNavFix(filePath):

	with open(filePath) as f:
	    content = f.readlines()

	nav_latitude = [[],[]]
	nav_longitude= [[],[]]

	for line in enumerate(content):
		waypoint_temp = line[1].strip().split(',')
		if waypoint_temp[0] != '$GPGGA':
			continue

		point_lat = float(waypoint_temp[2])
		point_long = float(waypoint_temp[4])
		point_status = int(waypoint_temp[6])

		isValidPoint = pointFlt(point_long, point_lat, point_status)

		if isValidPoint == 0:
			nav_latitude[0].append(point_lat)
			nav_longitude[0].append(point_long)
		elif isValidPoint == 1:
			nav_latitude[1].append(point_lat)
			nav_longitude[1].append(point_long)
		else:
			pass

	accTimeAvailability = float(len(nav_latitude[0]))/len(nav_latitude[0]+nav_latitude[1])
	print "FilePath: ", filePath
	print "accTimeAvailability: ", accTimeAvailability

	plt.figure()
	plt.title(filePath)
	plt.xlabel("Longitude")
	plt.ylabel("Latitude")
	plt.plot(nav_longitude[0], nav_latitude[0], '.b')
	plt.plot(nav_longitude[1], nav_latitude[1], '.r')
	plt.show()

if __name__ == "__main__":

	filePath = ["/home/yimeng/Documents/sinan/11.30smallcircle.txt", \
				"/home/yimeng/Documents/sinan/11.55largecircle.txt"]
	p1 = multiprocessing.Process(target=plotNavFix, args=(filePath[0], ))
	p2 = multiprocessing.Process(target=plotNavFix, args=(filePath[1], )) 

	p1.start()
	p2.start()
