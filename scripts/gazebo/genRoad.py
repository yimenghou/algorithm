
"""
Plugin for generate customized road in world file

Auther: Yimeng
Last update: 2017.07.11

"""

import numpy as np, math, copy
import pylab as plt
import os

class Road_generator(object):

	def __init__(self):

		self.N_prefix_space = 3
		self.world_file_name_input = "./template.world"
		self.world_file_name_output = "/home/yimeng/sim_ws/src/car-demo/car_demo/worlds/road_sim.world"
		self.road_sentence = []
		self.global_xy = []

		try:
			os.unlink(self.world_file_name_output)
		except:
			pass

	def buildGraph(self, route="rrlrrllr"):

		p = np.array([0, 0])
		o = "+x"

		for i in route:
			p, o = self.intepreter(p, o, i)	

		# p, o = self.generateCurve(p, o, 'l', radius=50)	
		# p, o = self.generateCurve(p, o, 'l', radius=100)
		# p, o = self.generateCurve(p, o, 'l', radius=150)

	def viewGraph(self):
		
		xy = np.vstack( self.global_xy )
		plt.figure()
		plt.plot(xy[:,0], xy[:,1], '-r')
		plt.show()

	def worldFileGeneration(self):

		with open(self.world_file_name_input, 'r') as f:
			ll = f.readlines()

			for line in enumerate(ll):
				if "width" in line[1]:
					insert_location = line[0]+1

		with open(self.world_file_name_output, 'a') as f:

			for item in ll[:insert_location]:
				f.write(item)
			for item in self.road_sentence:
				f.write(item)
			for item in ll[insert_location:]:
				f.write(item)

	def intepreter(self, p, o, input_l):

		if input_l == "-":
			p, o = self.generateLine(p, o)
		else:
			p, o = self.generateCurve(p, o, input_l)

		return p, o			

	def generateLine(self, start_point, start_orientation, length=100):

		space = "  "*self.N_prefix_space		
		end_point = copy.deepcopy(start_point)

		if "x" in start_orientation:

			end_point[0] = start_point[0] + length
			end_point[1] = start_point[1]

		if "y" in start_orientation:

			end_point[0] = start_point[0]
			end_point[1] = start_point[1] + length  

		self.global_xy.append( start_point )
		self.global_xy.append( end_point )

		self.road_sentence.extend( space+"<point>%3.3f %3.3f 0.005</point>"%(start_point[0], start_point[1])+"\n" )
		self.road_sentence.extend( space+"<point>%3.3f %3.3f 0.005</point>"%(end_point[0], end_point[1])+"\n" )

		return end_point, start_orientation


	def generateCurve(self, start_point, start_orientation, road_option, radius=100, degree_resolution=1000):

		space = "  "*self.N_prefix_space
		axis = np.linspace(0, 90-10**(-np.log10(degree_resolution)+1), degree_resolution)
		x = np.reshape( radius*np.cos(axis*np.pi/180), (-1,1))
		y = np.reshape( radius*np.sin(axis*np.pi/180), (-1,1))		

		if start_orientation == "+x":
			if road_option == "l":
				final_x = copy.deepcopy(x)
				final_y = copy.deepcopy(radius-y)
				end_point = np.array([radius, radius])
				end_orientation = "+y"
			elif road_option == "r":	
				final_x = copy.deepcopy(x)
				final_y = copy.deepcopy(y-radius)
				end_point = np.array([radius, -radius])	
				end_orientation = "-y"	

		elif start_orientation == "+y":
			if road_option == "l":
				final_x = copy.deepcopy(x-radius)
				final_y = copy.deepcopy(y)
				end_point = np.array([-radius, radius])	
				end_orientation = "-x"			
			elif road_option == "r":
				final_x = copy.deepcopy(radius-x)
				final_y = copy.deepcopy(y)
				end_point = np.array([radius, radius])
				end_orientation = "+x"	

		elif start_orientation == "-x":
			if road_option == "l":
				final_x = copy.deepcopy(-x)
				final_y = copy.deepcopy(y-radius)
				end_point = np.array([-radius, -radius])	
				end_orientation = "-y"			
			elif road_option == "r":
				final_x = copy.deepcopy(-x)
				final_y = copy.deepcopy(radius-y)
				end_point = np.array([-radius, radius]) 
				end_orientation = "+y"	

		elif start_orientation == "-y":
			if road_option == "l":
				final_x = copy.deepcopy(radius-x)
				final_y = copy.deepcopy(-y)
				end_point = np.array([radius, -radius])	
				end_orientation = "+x"

			elif road_option == "r":
				final_x = copy.deepcopy(x-radius)
				final_y = copy.deepcopy(-y)
				end_point = np.array([-radius, -radius])
				end_orientation = "-x"	

		if final_x[0] != 0 or final_y[0] != 0:
			final_x = final_x[::-1]
			final_y = final_y[::-1]

		final_x += start_point[0]
		final_y += start_point[1]

		self.global_xy.append( np.hstack((final_x, final_y)) )

		for line in range(x.shape[0]):
			sentence = space+"<point>%3.3f %3.3f 0.005</point>"%(final_x[line,:], final_y[line,:])+"\n"
			self.road_sentence.extend( sentence )

		return start_point+end_point, end_orientation

if __name__ == "__main__":

	rd = Road_generator()
	rd.buildGraph()
	rd.viewGraph()
	rd.worldFileGeneration()
