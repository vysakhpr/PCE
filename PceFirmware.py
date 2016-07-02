import lib.DataStructures
import lib.PathComputation
import lib.FetchNetwork
import lib.SetRoutes
import lib.test.BuildNetworkDemo 

#graph_nodes=lib.FetchNetwork.init()
#graph_nodes=lib.test.BuildNetworkDemo.initDemoOne();
#lib.DataStructures.display_network(graph_nodes)
#print str(lib.DataStructures.no_of_nodes)+"================================================================================================="
#print lib.DataStructures.no_of_nodes
#print graph_nodes[4].get_parent_list()
#lib.DataStructures.source="127.0.0.5"
#lib.DataStructures.destination="127.0.0.1"
lib.DataStructures.source="0200:0000:0000:0007"
lib.DataStructures.destination="0200:0000:0000:0001"

graph_nodes=lib.FetchNetwork.init()
#lib.DataStructures.display_network(graph_nodes)
graph_nodes=lib.DataStructures.format_parents(graph_nodes)
graph_nodes=lib.DataStructures.convert_neighbor_to_parent(graph_nodes)
lib.DataStructures.display_network(graph_nodes)
#lib.DataStructures.display_network(graph_nodes)
#print lib.DataStructures.no_of_nodes
#paths,cost_matrix=lib.PathComputation.init(lib.DataStructures.source,lib.DataStructures.destination,graph_nodes)
#lib.SetRoutes.init(paths,graph_nodes,cost_matrix)
for node in graph_nodes[1:]:
	#print node.get_ip_address()
	paths,cost_matrix=lib.PathComputation.init(node.get_ip_address(),lib.DataStructures.destination,graph_nodes)
	lib.SetRoutes.init(paths,graph_nodes,cost_matrix)