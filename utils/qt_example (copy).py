#! /usr/bin/env python

"""
last update: 2018.08.12 by yimeng
"""

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess, time
import os
import signal

# child = subprocess.Popen(["roslaunch","ros_arduino_python","arduino.launch"])
# #child.wait() #You can use this line to block the parent process untill the child process finished.
# print("parent process")
# print(child.poll())

# rospy.loginfo('The PID of child: %d', child.pid)
# print ("The PID of child:", child.pid)

# rospy.sleep(15)

# child.send_signal(signal.SIGINT) #You may also use .terminate() method

def b1_clicked():
   global p
   print "Button 1 clicked"
   p = subprocess.Popen(["roslaunch","spreader_controller","spreader_controller.launch"])
   # p = subprocess.Popen('roslaunch spreader_controller spreader_controller.launch', shell=True)
   # cmd = "roslaunch spreader_controller spreader_controller.launch"
   # p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

def b2_clicked():
   global p
   print "Button 2 clicked"
   try:
      # p.kill()
      p.send_signal(signal.SIGINT) #You may also use .terminate() method
      # os.killpg(os.getpgid(p.pid), signal.SIGINT)  # Send the signal to all the process groups
   except:
      pass

def b3_clicked():
   global p1
   print "Button 3 clicked"
   p1 = subprocess.Popen(["roslaunch","pure_pursuit","pure_pursuit.launch"])
   # cmd = "roslaunch spreader_controller spreader_controller.launch"
   # p = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)


def b4_clicked():
   global p1
   print "Button 4 clicked"
   try:
      # p1.kill()
      p1.send_signal(signal.SIGINT) #You may also use .terminate() method
      # os.killpg(os.getpgid(p1.pid), signal.SIGINT)  # Send the signal to all the process groups
   except:
      pass

# def b3_clicked():
#    global p
#    poll = p.poll()
#    if poll == None:
#       print "still alive"
#    else:
#       print "killed"

# def b3_clicked():
#    global p
#    poll = p.poll()
#    if poll == None:
#       print "still alive"
#    else:
#       print "killed"

hsep = 50
vsep = 50

app = QApplication(sys.argv)
win = QDialog()
b1 = QPushButton(win)
b1.setText("Driver")
b1.move(50,20)
b1.resize(200,50)
QObject.connect(b1,SIGNAL("clicked()"),b1_clicked)

b2 = QPushButton(win)
b2.setText("Localization")
b2.move(50,70)
b2.resize(200,50)
QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)

b3 = QPushButton(win)
b3.setText("Localization")
b3.move(50,120)
b3.resize(200,50)
QObject.connect(b3,SIGNAL("clicked()"),b3_clicked)

b4 = QPushButton(win)
b4.setText("Localization")
b4.move(50,170)
b4.resize(200,50)
QObject.connect(b4,SIGNAL("clicked()"),b4_clicked)

win.setGeometry(0,0,960,540)
win.setWindowTitle("PyQt")
win.show()

# while True:
#    try:
#       if p.poll() == None:
#          b1.setText("open")
#          print "still alive"
#       else:
#          b1.setText("close")
#          print "killed"
#    except:
#       pass



sys.exit(app.exec_())


   # p = subprocess.Popen('roslaunch spreader_controller spreader_controller.launch', shell=True)
   # time.sleep(1)
   # os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Send the signal to all the process groups

   # time.sleep(3)
   # p.terminate() 
   # os.kill(p.pid, signal.SIGTERM) #or signal.SIGKILL 
   # subprocess.Popen.kill(p)
   # time.sleep(3)  

# import os
# import sys 
# from PyQt4.QtCore import * 
# from PyQt4.QtGui import * 
 
# def main(): 
#     app = QApplication(sys.argv) 
#     w = MyWindow() 
#     w.show() 
#     sys.exit(app.exec_()) 
 
# class MyWindow(QWidget): 
#     def __init__(self, *args): 
#         QWidget.__init__(self, *args) 
 
#         # create objects
#         label = QLabel(self.tr("Enter command and press Return"))
#         self.le = QLineEdit()
#         self.te = QTextEdit()

#         # layout
#         layout = QVBoxLayout(self)
#         layout.addWidget(label)
#         layout.addWidget(self.le)
#         layout.addWidget(self.te)
#         self.setLayout(layout) 

#         # create connection
#         self.connect(self.le, SIGNAL("returnPressed(void)"),
#                      self.run_command)

#     def run_command(self):
#         cmd = str(self.le.text())
#         stdouterr = os.popen4(cmd)[1].read()
#         self.te.setText(stdouterr)
  
# if __name__ == "__main__": 
#     main()







#! /usr/bin/env python

"""
last update: 2018.08.12 by yimeng
"""

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess, time
import os
import signal
import multiprocessing

# child = subprocess.Popen(["roslaunch","ros_arduino_python","arduino.launch"])
# #child.wait() #You can use this line to block the parent process untill the child process finished.
# print("parent process")
# print(child.poll())

# rospy.loginfo('The PID of child: %d', child.pid)
# print ("The PID of child:", child.pid)

# rospy.sleep(15)

# child.send_signal(signal.SIGINT) #You may also use .terminate() method




class wsdemo(object):

   def __init__(self):

      hsep = 50
      vsep = 50

      self.p = [None]*4
      # self.cmd_map = {0:"roslaunch ws_bringup driver.launch",\
      #                 1:"roslaunch ws_bringup ws_demo.launch",\
      #                 2:"roslaunch task_manager sm_autostart_v3.launch"}

      self.cmd_map = {0:"roslaunch spreader_controller spreader_controller.launch",\
                      1:"rostopic echo /spreader_controller/debug",\
                      2:"roslaunch task_manager sm_autostart_v3.launch"}


      self.app = QApplication(sys.argv)
      self.win = QDialog()
      self.b1 = QPushButton(self.win)
      self.b1.setText("Driver")
      self.b1.move(50,20)
      self.b1.resize(300,50)
      QObject.connect(self.b1,SIGNAL("clicked()"),self.b1_clicked)

      self.b2 = QPushButton(self.win)
      self.b2.setText("Family bucket")
      self.b2.move(50,70)
      self.b2.resize(300,50)
      QObject.connect(self.b2,SIGNAL("clicked()"),self.b2_clicked)

      self.b3 = QPushButton(self.win)
      self.b3.setText("State machine")
      self.b3.move(50,120)
      self.b3.resize(300,50)
      QObject.connect(self.b3,SIGNAL("clicked()"),self.b3_clicked)

      self.b4 = QPushButton(self.win)
      self.b4.setText("Well GNS")
      self.b4.move(50,170)
      self.b4.resize(300,50)
      QObject.connect(self.b4,SIGNAL("clicked()"),self.b4_clicked)

      self.win.setGeometry(0,0,960,540)
      self.win.setWindowTitle("PyQt")
      self.win.show()

      self.p = multiprocessing.Process(target=self.app.exec_())
      self.p.start()

   def b1_clicked(self):
      print "Button 1 clicked"
      if self.p[0] is None:
         self.p[0] = subprocess.Popen(["roslaunch spreader_controller spreader_controller.launch"])  
         self.b1.setText("spreader_controller (click to close)")
      else:
         self.p[0].send_signal(signal.SIGINT) #You may also use .terminate() method                
         self.b1.setText("spreader_controller (click to open)")
         self.p[0] = None

   def b2_clicked(self):
      print "Button 2 clicked"
      if self.p[1] is None:
         self.p[1] = subprocess.Popen([self.cmd_map[1]])  
         self.b2.setText("pure_pursuit (click to close)")
      else:
         self.p[1].send_signal(signal.SIGINT) #You may also use .terminate() method                
         self.b2.setText("pure_pursuit (click to open)")
         self.p[1] = None

   def b3_clicked(self):
      print "Button 2 clicked"
      if self.p[2] is None:
         self.p[2] = subprocess.Popen([self.cmd_map[2]])  
         self.b3.setText("pure_pursuit (click to close)")
      else:
         self.p[2].send_signal(signal.SIGINT) #You may also use .terminate() method                
         self.b3.setText("pure_pursuit (click to open)")
         self.p[2] = None

   def b4_clicked(self):
      print "Button 2 clicked"
      if self.p[3] is None:
         self.p[3] = subprocess.Popen([self.cmd_map[3]])  
         self.b4.setText("pure_pursuit (click to close)")
      else:
         self.p[3].send_signal(signal.SIGINT) #You may also use .terminate() method                
         self.b4.setText("pure_pursuit (click to open)")
         self.p[3] = None


if __name__ == "__main__":
   worker0 = wsdemo()
