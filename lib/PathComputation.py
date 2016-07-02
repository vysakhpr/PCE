import lib.DataStructures
import operator

temporary_path=[]
full_paths=[]

no_of_paths=0



def init(source_ip, sink_ip,graph_nodes):
	print("<!--------------------------------------------Computing Paths--------------------------------------------!>");
	path={}
	source=graph_nodes[lib.DataStructures.find_node(graph_nodes,source_ip)]
	sink=graph_nodes[lib.DataStructures.find_node(graph_nodes,sink_ip)]
	find_paths(source,sink,graph_nodes)
	no_of_paths=len(full_paths)


	#aggregate_ranks=find_aggregate_rank(full_paths,graph_nodes)
	#print aggregate_ranks
	#aggregate_ranks_sorted = sorted(aggregate_ranks.items(), key=operator.itemgetter(1))
	#print aggregate_ranks_sorted
	#for (k,v) in aggregate_ranks_sorted:
	#	print (full_paths[k],v)

	print("RPL Route--->")
	current_node=source
	while True:
		next_node=find_rpl_parent(current_node,graph_nodes)
		if next_node is None:
			break
		print("\t"+current_node.get_ip_address()+"\twill choose "+next_node.get_ip_address()+"\tas the next hop for all its packets-----Packet Rate:"+str(current_node.get_packet_rate()))
		current_node=next_node

	cost_matrix=find_optimal_route(sink_ip,source_ip,graph_nodes)

	print("PCE Route--->")
	current_index=lib.DataStructures.find_node(graph_nodes,source_ip)
	sink_index=lib.DataStructures.find_node(graph_nodes,sink_ip)
	while current_index!=sink_index:
		next_index=cost_matrix[sink_index][current_index].get_next_hop()
		if next_index==-1:
			next_node=find_rpl_parent(graph_nodes[current_index],graph_nodes)
			if next_node==None:
				print("No Parents Available for node "+str(graph_nodes[current_index].get_ip_address()))
				return
			next_index=graph_nodes.index(next_node)
			print("No alternate routes available......")
			print("Choosing RPL parent as the next hop...")
		print("\t"+graph_nodes[current_index].get_ip_address()+"\twill choose "+graph_nodes[next_index].get_ip_address()+"\tas the next hop for all its packets-----Packet Rate:"+str(graph_nodes[current_index].get_packet_rate()))
		path[graph_nodes[current_index].get_ip_address()]=graph_nodes[next_index].get_ip_address()
		current_index=next_index
	return path,cost_matrix

def find_optimal_route(source_ip,destination_ip,graph_nodes):
	cost_matrix=[[lib.DataStructures.CostMatrixCell() for i in range(len(graph_nodes))] for j in range(len(graph_nodes))]
	#display_cost_matrix(cost_matrix)
	source_index=lib.DataStructures.find_node(graph_nodes,source_ip)
	destination_index=lib.DataStructures.find_node(graph_nodes,destination_ip)
	for i in range(len(graph_nodes)):
		for j in range(len(graph_nodes)):
			cost_matrix=build_matrix(cost_matrix,i,j,graph_nodes)
	#cost_matrix=build_matrix(cost_matrix,source_index,destination_index,graph_nodes)
	#display_cost_matrix(cost_matrix)
	return cost_matrix

	




def display_cost_matrix(cost_matrix):
	for x in cost_matrix:
		for y in x:
			print "("+str(y.get_max_packet_rate())+","+str(y.get_next_hop())+")",
		print ""


def build_matrix(cost_matrix,i,j,graph_nodes):
	if graph_nodes[i].get_rank()<=graph_nodes[j].get_rank():
		if i==j:
			cost_matrix[i][j].visit()
			cost_matrix[i][j].set_max_packet_rate(graph_nodes[i].get_packet_rate())
			cost_matrix[i][j].set_next_hop(i)
		else:
			parent_list=graph_nodes[j].get_parent_list()
			optimal_data_rate_list={}
			for parent_ip in parent_list:
				parent_index=lib.DataStructures.find_node(graph_nodes,parent_ip)
				if not cost_matrix[i][parent_index].is_visited():
					#if (i,j) not in cost_matrix[i][parent_index].get_waiting_list():
						#cost_matrix[i][parent_index].add_to_waiting_list((i,j))
					cost_matrix=build_matrix(cost_matrix,i,parent_index,graph_nodes)
				optimal_data_rate_list[parent_index]=(cost_matrix[i][parent_index].get_max_packet_rate())

			optimal_data_rate_list={ k:v for k, v in optimal_data_rate_list.items() if v!=-1 }
			if optimal_data_rate_list and not cost_matrix[i][j].is_visited():
				minimum_datarate_of_neighbor_index=min(optimal_data_rate_list,key=optimal_data_rate_list.get)
				minimum_datarate_of_neighbor=optimal_data_rate_list[minimum_datarate_of_neighbor_index]
				if minimum_datarate_of_neighbor<=lib.DataStructures.packet_rate_max_threshold:
					cost_matrix[i][j].set_max_packet_rate(max(graph_nodes[j].get_packet_rate(),minimum_datarate_of_neighbor))
					cost_matrix[i][j].set_next_hop(minimum_datarate_of_neighbor_index)
				cost_matrix[i][j].visit()
		#if cost_matrix[i][j].get_waiting_list():
			#for (x,y) in cost_matrix[i][j].get_waiting_list():
				#cost_matrix=build_matrix(cost_matrix,x,y,graph_nodes)
			#cost_matrix[i][j].clear_waiting_list()
	return cost_matrix


def find_rpl_parent(source,graph_nodes):
	parents=source.get_parent_list()
	if not parents:
		return None
	minimum_rank_node_ip=parents[0]
	for parent in parents:
		if lib.DataStructures.find_rank_of_ip(parent,graph_nodes)<lib.DataStructures.find_rank_of_ip(minimum_rank_node_ip,graph_nodes):
			minimum_rank_node_ip=parent
	return graph_nodes[lib.DataStructures.find_node(graph_nodes,minimum_rank_node_ip)]

def find_aggregate_rank(full_paths,graph_nodes):
	rank_index={}
	for path in full_paths:
		#print path
		rank_index[full_paths.index(path)]=0
		for i in range(len(path)):
			node_rank=lib.DataStructures.find_rank_of_ip(path[i],graph_nodes)
			rank_index[full_paths.index(path)]=rank_index[full_paths.index(path)]+node_rank
	return rank_index

def find_paths(source,destination,graph_nodes):
	current_node=source
	for ip in temporary_path:                         #already visited
		if ip==current_node.get_ip_address():
			return
	temporary_path.append(current_node.get_ip_address())
	if current_node.get_ip_address()==destination.get_ip_address():
		full_paths.append(temporary_path[:])
		temporary_path.pop()
		return 
	for parent_ip in current_node.get_parent_list():
		next_node=graph_nodes[lib.DataStructures.find_node(graph_nodes,parent_ip)]
		find_paths(next_node,destination,graph_nodes)
	temporary_path.pop()
	return 

	
