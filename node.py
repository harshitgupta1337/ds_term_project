'''
Project name : FIFO_Comm
Module name  : node
Created on : Thu Mar 12 17:52:53 2015
Author : Anant Pushkar
Abstract class for node
'''
import abc
import socket
import time
import json
from multiprocessing import Process

debug = False
default_name = "unnamed"

class Node:
	__metaclass__ = abc.ABCMeta
	
	def __init__(self , config):
		self.tcp_ip   = config["TCP_IP"]
		self.tcp_port = config["TCP_PORT"]
		self.seq      =  1
		self.buffer_size = config["BUFFER_SIZE"] if "BUFFER_SIZE" in config else 1024
		self.peers   = config["peers"] if "peers" in config else []
		self.name    = config["name"] if "name" in config else default_name
		
		self.exp_seq = {}
		for peer in self.peers: self.exp_seq[peer] = 1
		
		self.peer_buff = {}
		for peer in self.peers: self.peer_buff[peer] = {}
		
		self.listener = Process(target=self.receiver , args=())
		self.init()
	
	def start_session(self):
		if debug: print "Starting session"
		self.listener.start()
		time.sleep(1)
	
	def receiver(self):
		if debug: print "Listener started at",(self.tcp_ip, self.tcp_port)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.tcp_ip, self.tcp_port))
		s.listen(1)
		
		while True:
			conn, addr = s.accept()
			data = ""
			while 1:
				block = conn.recv(self.buffer_size)
				if not block: break
				data += block
			conn.close()
		
			data = json.loads(data)
			if debug: print "received", data
			if not data["sender"] in self.peers: self.on_receive(data["msg"] , data["sender"])
			else:
				if data["seq"] == self.exp_seq[data["sender"]]:
					self.on_receive(data["msg"] , data["sender"])
					self.exp_seq[data["sender"]] += 1
			
					while self.exp_seq[data["sender"]] in self.peer_buff:
						self.on_receive(self.peer_buff[self.exp_seq[data["sender"]]] , data["sender"])
						del(self.peer_buff[self.exp_seq[data["sender"]]])
						self.exp_seq[data["sender"]] += 1
				else:
					self.peer_buff[data["seq"]] = data["msg"]
		
	@abc.abstractmethod
	def on_receive(self , msg , peer):
		pass
	
	@abc.abstractmethod
	def init(self , arg=None):
		pass
	
	def send(self , ip , port , msg , seq=None):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, port))
		
		data = {}
		data["seq"]	= self.seq if seq==None else seq
		self.seq = max(data["seq"],self.seq) + 1
		data["msg"] = msg
		data["sender"] = self.name
		s.send(json.dumps(data))
		
		s.close()
	
	
