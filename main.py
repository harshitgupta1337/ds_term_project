'''
Project name : FIFO_Comm
Created on : Thu Mar 12 17:46:09 2015
Author : Anant Pushkar
FIFo communication prototype for DS term project
'''
import sys
debug_mode = len(sys.argv)>1 and sys.argv[1]=="DEBUG"
def debug(msg):
	if debug_mode:
		print msg

from node import Node
import time

class TestNode(Node):
	def init(self,arg=None)	:
		print "initializing node:" , self.name
	
	def on_receive(self , msg , sender):
		print "sender:" , sender
		print "msg:" , msg
		print "==========="

syslist = ["tango" , "charlie"]

config = {}
config["TCP_IP"]   = "127.0.0.1"
config["TCP_PORT"] = 7000
config["peers"]    = syslist
config["name"]     = "tango"

test_node1 = TestNode(config)
test_node1.start_session()

config = {}
config["TCP_IP"]   = "127.0.0.1"
config["TCP_PORT"] = 7001
config["name"]     = "charlie"

test_node2 = TestNode(config)
test_node2.send("127.0.0.1" , 7000 , "TEST MSG2" , seq=2)
test_node2.send("127.0.0.1" , 7000 , "TEST MSG1" , seq=1)
test_node2.send("127.0.0.1" , 7000 , "TEST MSG4" , seq=4)
test_node2.send("127.0.0.1" , 7000 , "TEST MSG5" , seq=5)
test_node2.send("127.0.0.1" , 7000 , "TEST MSG3" , seq=3)
