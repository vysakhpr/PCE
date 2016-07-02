import lib.DataStructures

from coapthon.resources.resource import Resource
from coapthon.client.coap import CoAP
from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.messages.request import Request

import socket

graph_nodes=[]
        
def init():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((lib.DataStructures.nme_ip,lib.DataStructures.nme_port))
	length=s.recv(2)
	s.close()
	lib.DataStructures.no_of_nodes=0
	node=lib.DataStructures.Nodes(1)
	node.set_ip_address("0200:0000:0000:0001")
	node.set_packet_rate(0);
	graph_nodes.append(node)
	lib.DataStructures.no_of_nodes=lib.DataStructures.no_of_nodes+1
	for i in range(int(length)):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((lib.DataStructures.nme_ip,lib.DataStructures.nme_port))
		buff=s.recv(1024)
		contents=buff.split(";")
		node=lib.DataStructures.Nodes(int(contents[1]))
		node.set_ip_address(contents[0])
		node.set_packet_rate(float(contents[2]))
		for ip in contents[3:]:
			if ip.strip()!= "":
				node.add_parent(ip.strip(),0,0)
		graph_nodes.append(node)
		lib.DataStructures.no_of_nodes=lib.DataStructures.no_of_nodes+1
		s.close()
	return graph_nodes






