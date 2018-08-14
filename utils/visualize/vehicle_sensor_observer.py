#! /usr/bin/env python

import rospy
import random
import matplotlib.pylab as plt
import numpy as np

from ws_msgs.msg import vehicleRecvSensor

class observer(object):

    def __init__(self):

        self.sensor_front = []
        self.sensor_back = []

        self.color_front = []
        self.color_back = []
        self.color_vehicle = []

        # self.buff_length = 50
        self.sub = rospy.Subscriber("/vehicle_sensor", vehicleRecvSensor, self.callback)

    def callback(self,data):

        self.sensor_front = [data.s_front_left, data.s_front_mid, data.s_front_right]
        self.sensor_back = [data.s_back_left, data.s_back_mid, data.s_back_right]
        self.sensor_vehicle = [data.v_front_left, data.v_back_left, data.v_front_right, data.v_back_right]

        for item in self.sensor_front:
            if abs(item) <= 2:
                self.color_front.append("r")
            elif abs(item) <= 6:
                self.color_front.append("y")
            elif abs(item) <= 9:
                self.color_front.append("b")                
            else:
                self.color_front.append("k")

        for item in self.sensor_back:
            if abs(item) <= 2:
                self.color_back.append("r")
            elif abs(item) <= 6:
                self.color_back.append("y")
            elif abs(item) <= 9:
                self.color_back.append("b")   
            else:
                self.color_back.append("k")        

        for item in self.sensor_vehicle:
            if abs(item) <= 2:
                self.color_vehicle.append("r")   
            else:
                self.color_vehicle.append("b")  

    def run(self):

        # plt.figure()
        plt.figure(figsize=(15,10))
        plt.ion()
        plt.show()

        bar_edge = [-0.1, 0, 0.1]
        while not rospy.is_shutdown():
            if not self.sensor_front or not self.sensor_back or not self.sensor_vehicle: 
                continue
            plt.gcf().clear()

            plt.subplot(232)
            plt.ylim([0, 15])
            plt.bar(bar_edge, self.sensor_front, width=0.04, color=self.color_front)
            for i, v in enumerate(self.sensor_front):
                plt.text(bar_edge[i], v+1, str(round(v,2)), fontsize=20, bbox=dict(facecolor='brown', alpha=0.6))

            plt.subplot(235)
            plt.ylim([0, 15])
            plt.bar(bar_edge, self.sensor_back, width=0.04,color=self.color_back)
            for i, v in enumerate(self.sensor_back):
                plt.text(bar_edge[i], v+1.5, str(round(v,2)), fontsize=20, bbox=dict(facecolor='brown', alpha=0.6))
            plt.gca().invert_yaxis()

            width = 0.2
            plt.subplot(131)
            plt.xlim([0, 4])
            plt.barh(np.arange(2), self.sensor_vehicle[:2], width, align="center", color=self.color_vehicle[:2])
            for i, v in enumerate(self.sensor_vehicle[:2]):
                plt.text(i, v-2, str(round(-v,2)), fontsize=20, bbox=dict(facecolor='brown', alpha=0.6))

            plt.subplot(133)
            plt.xlim([0, 4])
            plt.barh(np.arange(2), self.sensor_vehicle[2:], width, align="center", color=self.color_vehicle[2:])
            for i, v in enumerate(self.sensor_vehicle[2:]):
                plt.text(i, v-2, str(round(-v,2)), fontsize=20, bbox=dict(facecolor='brown', alpha=0.6))
            plt.gca().invert_xaxis()

            plt.pause(0.01)
            self.color_front = []
            self.color_back = []
            self.color_vehicle = []

rospy.init_node("ob", anonymous=True)
worker0 = observer()
worker0.run()