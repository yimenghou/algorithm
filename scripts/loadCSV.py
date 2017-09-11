import csv
import pylab as plt

lat = []
lon = []
alt = []

n = 0
with open('/home/yimeng/State.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:

		if n != 0:
			lat.append(float(row[0]))
			lon.append(float(row[1]))
			alt.append(float(row[2]))

		n += 1

plt.figure()
plt.plot(lon, lat, '.')
plt.show()