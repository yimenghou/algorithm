#! /usr/bin/env python

import rospy
import random
import pylab as plt
import numpy as np

from ws_msgs.msg import vehicleRecvState, vehicleSendCmd

class observer(object):

    def __init__(self):

        self.angle_tar_lst = []
        self.angle_cur_lst = []

        self.speed_tar_lst = []
        self.speed_cur_lst = []

        self.angle_current = 0
        self.angle_target = 0

        self.speed_current = 0        
        self.speed_target = 0        

        self.buff_length = 100

        self.sub0 = rospy.Subscriber("/vehicle_state", vehicleRecvState, self.curSpeedcallback)
        self.sub2 = rospy.Subscriber("/vehicle_cmd_mux", vehicleSendCmd, self.tarSpeedcallback)

    def curSpeedcallback(self,data):
        self.angle_current = data.gantry_angle
        self.speed_current = data.gantry_speed

    def tarSpeedcallback(self,data):
        self.angle_target = data.gantry_angle/100*22.04
        self.speed_target = data.gantry_speed

    def run(self):

        plt.figure()
        plt.ion()
        plt.show()
        r = rospy.Rate(20)
        while not rospy.is_shutdown():

            plt.gcf().clear()
            plt.subplot(211)
            plt.title("Gantry Angle")

            if len(self.angle_tar_lst) >= self.buff_length:
                self.angle_tar_lst.pop(0)
            if len(self.angle_cur_lst) >= self.buff_length:
                self.angle_cur_lst.pop(0)

            self.angle_tar_lst.append(self.angle_target)
            self.angle_cur_lst.append(self.angle_current)

            plt.plot([j for j in range(len(self.angle_cur_lst))], [0]*len(self.angle_cur_lst), "-y*")
            plt.plot([i for i in range(len(self.angle_tar_lst))], self.angle_tar_lst, "-bo")
            plt.plot([i for i in range(len(self.angle_cur_lst))], self.angle_cur_lst, "-rx")

            plt.subplot(212)
            plt.title("Gantry Speed")
            if len(self.speed_tar_lst) >= self.buff_length:
                self.speed_tar_lst.pop(0)
            if len(self.speed_cur_lst) >= self.buff_length:
                self.speed_cur_lst.pop(0)

            self.speed_tar_lst.append(self.speed_target)
            self.speed_cur_lst.append(self.speed_current)

            plt.plot([j for j in range(len(self.speed_cur_lst))], [0]*len(self.speed_cur_lst), "-y*")
            plt.plot([j for j in range(len(self.speed_tar_lst))], self.speed_tar_lst, "-bo")
            plt.plot([i for i in range(len(self.speed_cur_lst))], self.speed_cur_lst, "-rx")
            plt.pause(0.01)

            r.sleep()

rospy.init_node("ob", anonymous=True)
worker0 = observer()
worker0.run()