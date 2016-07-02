import lib.DataStructures
import lib.PathComputation
import time
from lib.coapthon.client.coap import CoAP
from lib.coapthon.client.helperclient import HelperClient

def init(paths,graph_nodes,cost_matrix):
	for path in paths:
		i=0
		while(i<1):
			lib.DataStructures.timed_out_flag=0
			ratio=find_ratio(path,graph_nodes,cost_matrix)
			if not(path in lib.DataStructures.visited):
				lib.DataStructures.visited.append(path)
				send_next_hop(path,paths[path],ratio)
				time.sleep(2)
			if lib.DataStructures.timed_out_flag==0:
				break
			#time.sleep(2)
			i=i+1
		#time.sleep(5)



def send_next_hop(node_ip, next_hop_ip,ratio):
	node_ip=format_ip(node_ip)
	host=lib.DataStructures.prefix+node_ip
	port=5684
	payload=str(ratio)+";fe80::"+next_hop_ip
	print payload
	client = HelperClient(server=(host, port))
	client.post("Set-Parent",payload)
	client.stop()

def format_ip(ip):
	ip_sections=ip.split(':')
	ip=""
	#print ip_sections
	for section in ip_sections:
		if section=="0000":
			ip=ip+"0:"
		else:
			i=0
			while(section[i]=="0"):
				i=i+1
			ip=ip+section[i:]+":"
	return ip[:-1]

def find_ratio(node_ip,graph_nodes,cost_matrix):
	node=graph_nodes[lib.DataStructures.find_node(graph_nodes,node_ip)]

	current_node=node
	rpl_max_packet_rate=current_node.get_packet_rate()
	while True:
		next_node=lib.PathComputation.find_rpl_parent(current_node,graph_nodes)
		if next_node is None or next_node==graph_nodes[lib.DataStructures.find_node(graph_nodes,lib.DataStructures.destination)]:
			break
		if rpl_max_packet_rate<next_node.get_packet_rate():
			rpl_max_packet_rate=next_node.get_packet_rate()
		current_node=next_node
	current_index=lib.DataStructures.find_node(graph_nodes,node_ip)
	sink_index=lib.DataStructures.find_node(graph_nodes,lib.DataStructures.destination)
	pce_max_packet_rate=graph_nodes[current_index].get_packet_rate()
	while True:
		next_index=cost_matrix[sink_index][current_index].get_next_hop()
		if next_index==-1 or next_index==sink_index:
			break
		#print "-----------------"+str(graph_nodes[next_index].get_packet_rate())
		if pce_max_packet_rate<graph_nodes[next_index].get_packet_rate():
			pce_max_packet_rate=graph_nodes[next_index].get_packet_rate()
		current_index=next_index
	print pce_max_packet_rate, rpl_max_packet_rate
	return int((pce_max_packet_rate/(rpl_max_packet_rate+pce_max_packet_rate))*100)
