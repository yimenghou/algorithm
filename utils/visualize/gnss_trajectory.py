#! /usr/bin/env python
# last update 2017.9.17 yimeng
# merge gnss trajectory and kmz generation together
# check gnss trajectory

import rosbag, os, argparse
import numpy as np
import matplotlib.pylab as plt
from matplotlib.ticker import FormatStrFormatter

class plotTrajectory(object):

	def __init__(self, fileName):

		print ">> loading bag file: %s it may take seconds .."%fileName
		self.bag_filename = fileName
		self.bag = rosbag.Bag(fileName, 'r')

		self.gnss_data_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
		self.kmz_lines = []
		self.kmz_path = self.bag_filename[:-3] + "kmz"

		self.height = []
	def collect(self):

		for topic, msg, t in self.bag.read_messages(topics="/nav/fix"):
			if topic == "/nav/fix":
				gnss_data_line = str(msg.longitude)+','+str(msg.latitude)+','+str(msg.altitude)+' '
				self.gnss_data_dict[msg.status.status].append( np.array([msg.longitude, msg.latitude, msg.altitude]) )
				self.kmz_lines.append(gnss_data_line)
				self.height.append( msg.altitude )

		status_num = [0]*8
		for key_name in self.gnss_data_dict.keys():
			status_len = len(self.gnss_data_dict[key_name])
			if status_len == 0:
				continue
			elif status_len == 1:
				self.gnss_data_dict[key_name] = np.array(self.gnss_data_dict[key_name])
			else:
				self.gnss_data_dict[key_name] = np.vstack( self.gnss_data_dict[key_name])
				status_num[key_name] += status_len

		bar_edge = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
		plt.figure()
		plt.subplot(121)
		plt.xlabel("GNSS status")
		plt.ylabel("Points")
		plt.title("Total points: %d"%sum(status_num))
		plt.bar(bar_edge, status_num)
		for i, v in enumerate(status_num):
		    plt.text(bar_edge[i], v, str(v))

		self.color_lst = ['k', 'w', 'm', 'c', 'r', 'o', 'y', 'b']
		handle_lst = []
		plt.subplot(122)
		plt.axis('equal')
		plt.xlabel("Longitude")
		plt.ylabel("Latitude")
		plt.ticklabel_format(useOffset=False)

		for i in range(8):
			if status_num[i] == 0:
				continue
			if i != 7:
				plt_handle, = plt.plot(self.gnss_data_dict[i][:,0], self.gnss_data_dict[i][:,1], \
					"*"+self.color_lst[i],label="status="+str(i), markersize=10)
			else:
				plt_handle, = plt.plot(self.gnss_data_dict[i][:,0], self.gnss_data_dict[i][:,1], \
					"."+self.color_lst[i],label="status="+str(i), markersize=2)
			handle_lst.append(plt_handle)

		plt.legend(handles=handle_lst, loc=2)

		plt.figure()
		plt.xlabel("sample")
		plt.ylabel("Height (m)")
		plt.plot(self.height, linewidth=2)

		plt.show()  

	def writeKmzSyntax(self):

		if os.path.exists(self.kmz_path):
			os.unlink(self.kmz_path)

		with open(self.kmz_path, 'w') as f:

			f.write("""<?xml version="1.0" encoding="UTF-8"?>
			<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
			<Document>
			  <name>"""+self.bag_filename+""".kmz</name>
			  <Style id="s_ylw-pushpin">
			    <IconStyle>
			      <scale>1.1</scale>
			      <Icon>
			        <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			      </Icon>
			      <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
			    </IconStyle>
			  </Style>
			  <StyleMap id="m_ylw-pushpin">
			    <Pair>
			      <key>normal</key>
			      <styleUrl>#s_ylw-pushpin</styleUrl>
			    </Pair>
			    <Pair>
			      <key>highlight</key>
			      <styleUrl>#s_ylw-pushpin_hl</styleUrl>
			    </Pair>
			  </StyleMap>
			  <Style id="s_ylw-pushpin_hl">
			    <IconStyle>
			      <scale>1.3</scale>
			      <Icon>
			        <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			      </Icon>
			      <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
			    </IconStyle>
			  </Style>
			  <Placemark>
			    <name>Untitled Path</name>
			    <styleUrl>#m_ylw-pushpin</styleUrl>
			    <LineString>
			      <tessellate>1</tessellate>
			      <coordinates>
			""")

			for line in self.kmz_lines:
				f.write(line)

			f.write("""     </coordinates>
			    </LineString>
			  </Placemark>
			</Document>
			</kml>
			""")

		print "KMZ file saved into: ", self.kmz_path

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("rosbag_path")
	args = parser.parse_args()

	worker0 = plotTrajectory(args.rosbag_path)
	worker0.collect()
	worker0.writeKmzSyntax()