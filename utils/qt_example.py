import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import subprocess, time
import os
import signal
import multiprocessing

class wsdemo(QWidget):

	def __init__(self):
		super(wsdemo, self).__init__()

		hsep = 50
		vsep = 50

		self.p = [None]*4
		try:
			self.num = str(os.environ['ws_id'])
		except:
			self.num = "??"

		# self.cmd_map = {0:"roslaunch ws_bringup driver.launch",\
		#                 1:"roslaunch ws_bringup ws_demo.launch",\
		#                 2:"roslaunch task_manager sm_autostart_v3.launch"}

		self.cmd_map = {0:"roslaunch spreader_controller spreader_controller.launch",\
					    1:"rostopic echo /spreader_controller/debug",\
					    2:"roslaunch task_manager sm_autostart_v3.launch",\
					    3:"rviz"}

		self.in_map = {0:"Driver (click to open)",\
					   1:"Family Bucket (click to open)",\
					   2:"State Machine (click to open)",\
					   3:"Rviz (click to open)"}

		self.out_map = {0:"Driver (click to close)",\
					    1:"Family Bucket (click to close)",\
					    2:"State Machine (click to close)",\
					    3:"Rviz (click to close)"}

		self.setWindowTitle('Straddle Carrier #' + self.num)

		# self.textField = QTextEdit()
		# self.textField.setPlainText("Terminal outputs goes here")
		# self.textField.setReadOnly(True)

		# self.connect(self.textField, SIGNAL("returnPressed(void)"), self.run_command)


		self.b1 = QPushButton()
		self.b1.setText(self.in_map[0])
		self.b1.clicked.connect(self.b1_clicked)

		self.b2 = QPushButton()
		self.b2.setText(self.in_map[1])
		self.b2.clicked.connect(self.b2_clicked)

		self.b3 = QPushButton()
		self.b3.setText(self.in_map[2])
		self.b3.clicked.connect(self.b3_clicked)

		self.b4 = QPushButton()
		self.b4.setText(self.in_map[3])
		self.b4.clicked.connect(self.b4_clicked)

		layout = QVBoxLayout()
		layout.addWidget(self.b1)
		layout.addWidget(self.b2)
		layout.addWidget(self.b3)
		layout.addWidget(self.b4)
		# layout.addWidget(self.textField)
		self.setLayout(layout)
		self.show()

		# self.te = QTextEdit(self.win)
		# self.te.move(500, 20)
		# self.te.resize(400,800)
		# # self.te.setText(stdouterr)

		# self.b1 = QPushButton(self.win)
		# self.b1.setText("Driver")
		# self.b1.move(50,20)
		# self.b1.resize(300,50)
		# QObject.connect(self.b1,SIGNAL("clicked()"),self.b1_clicked)

		# self.b2 = QPushButton(self.win)
		# self.b2.setText("Family bucket")
		# self.b2.move(50,70)
		# self.b2.resize(300,50)
		# QObject.connect(self.b2,SIGNAL("clicked()"),self.b2_clicked)

		# self.b3 = QPushButton(self.win)
		# self.b3.setText("State machine")
		# self.b3.move(50,120)
		# self.b3.resize(300,50)
		# QObject.connect(self.b3,SIGNAL("clicked()"),self.b3_clicked)

		# self.b4 = QPushButton(self.win)
		# self.b4.setText("Well GNS")
		# self.b4.move(50,170)
		# self.b4.resize(300,50)
		# QObject.connect(self.b4,SIGNAL("clicked()"),self.b4_clicked)

		# self.win.setGeometry(0,0,960,540)
		# self.win.show()

	# def run_command(self):
	# 	n = 0
	# 	while True:
	# 		print "1"
	# 		self.textField.setText(str(n))
	# 		n += 1
	# 		time.sleep(1)

	# @pyqtSlot()
	# def on_click(self):
	# 	while True:
	# 		print "!"
	# 		out = self.p[2].stdout.read(1000)
	# 		if out == '' and process.poll() != None:
	# 			break
	# 		if out != '':
	# 			self.te.setText(out)


	def b1_clicked(self):
		print "Button 1 clicked"
		if self.p[0] is None:
			self.p[0] = subprocess.Popen(self.cmd_map[0].split(" "))  
			self.b1.setText(self.in_map[0])
		else:
			self.p[0].send_signal(signal.SIGINT) #You may also use .terminate() method                
			self.b1.setText(self.out_map[0])
			self.p[0] = None

	def b2_clicked(self):
		print "Button 2 clicked"
		if self.p[1] is None:
			self.p[1] = subprocess.Popen(self.cmd_map[1].split(" "))  
			self.b2.setText(self.in_map[1])
		else:
			self.p[1].send_signal(signal.SIGINT) #You may also use .terminate() method                
			self.b2.setText(self.out_map[1])
			self.p[1] = None

	def b3_clicked(self):
		print "Button 3 clicked"
		if self.p[2] is None:
			self.p[2] = subprocess.Popen(self.cmd_map[2].split(" "))  
			self.b3.setText(self.in_map[2])
		else:
			self.p[2].send_signal(signal.SIGINT) #You may also use .terminate() method                
			self.b3.setText(self.out_map[2])
			self.p[2] = None

	def b4_clicked(self):
		print "Button 4 clicked"
		if self.p[3] is None:
			self.p[3] = subprocess.Popen(self.cmd_map[3].split(" "))  
			self.b4.setText(self.in_map[3])
		else:
			self.p[3].send_signal(signal.SIGINT) #You may also use .terminate() method                
			self.b4.setText(self.out_map[3])
			self.p[3] = None


if __name__ == "__main__":
   app = QApplication(sys.argv)
   worker0 = wsdemo()
   app.exec_()
