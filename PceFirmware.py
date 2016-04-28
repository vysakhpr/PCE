from lib.DataStructures import *
from lib.NetworkLearning import *
from lib.PathComputation import *
"""
import threading
import time
class NetworkLearningThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Building Network")
		network_learning()


class PathComputationThread (threading.Thread):
    def __init__(self):
		threading.Thread.__init__(self)
    def run(self):
		print("ComputingPath")
		path_computation();

network_learning_thread=NetworkLearningThread()
path_computation_thread=PathComputationThread()

network_learning_thread.start()
path_computation_thread.start()

"""



network_learning()