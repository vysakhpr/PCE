slot_frame_width=31
no_of_channels=16
server_ip_address="127.0.0.1"
server_port=5683
no_of_nodes=0



class Nodes(object):
	"""The Motes or Entities in the Underlying RPL Network"""

	def __init__(self):
		super(Nodes, self).__init__()
		self.battery=0
		self.packet_forwarding_ratio=0
		self.queue_length=0
		self.neighbor_list=[]
		self.parent_list=[]
		

	def set_battery(self,arg):
		self.battery=arg

	def set_packet_forwarding_ratio(self,arg):
		self.packet_forwarding_ratio =arg

	def set_queue_length(self,arg):
		self.queue_length=arg

	def add_neighbor(self,ip,ss,per):
		self.neighbor_list.append(NeighborLinks(ip,ss,per));

	def add_parent(self,ip):
		self.parent_list.append(ip)

	def get_battery(self):
		return self.battery

	def get_packet_forwarding_ratio(self):
		return self.packet_forwarding_ratio

	def get_queue_length(self):
		return self.queue_length

	def get_neighbor_list(self):
		return self.neighbor_list

	def get_parent_list(self):
		return self.parent_list



class NeighborLinks(object):
	"""The Links eminating from a Node--Has IP, Signal Strength, Packet Error Ratio"""
	def __init__(self, ip,ss,per):
		super(NeighborLinks, self).__init__()
		self.neighbor_ip=ip
		self.signal_strength=ss
		self.packet_error_rate=per
		

	def get_neighbor_ip(self):
		return self.neighbor_ip

	def get_signal_strength(self):
		return self.signal_strength

	def get_packet_error_rate(self):
		return self.packet_error_rate




