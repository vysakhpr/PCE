import lib.DataStructures
import lib.PathComputation
import lib.FetchNetwork
import lib.test.BuildNetworkDemo 

#graph_nodes=lib.FetchNetwork.init()
#graph_nodes=lib.test.BuildNetworkDemo.initDemoTwo();
#lib.DataStructures.display_network(graph_nodes)
#print str(lib.DataStructures.no_of_nodes)+"================================================================================================="
#print lib.DataStructures.no_of_nodes
#print graph_nodes[4].get_parent_list()
#source="127.0.0.13"
#destination="127.0.0.1"

source="0200:0000:0000:000a"
destination="0200:0000:0000:0001"

graph_nodes=lib.FetchNetwork.init()
#lib.DataStructures.display_network(graph_nodes)
graph_nodes=lib.DataStructures.format_parents(graph_nodes)
graph_nodes=lib.DataStructures.convert_neighbor_to_parent(graph_nodes)
lib.DataStructures.display_network(graph_nodes)
#lib.DataStructures.display_network(graph_nodes)
#print lib.DataStructures.no_of_nodes
paths=lib.PathComputation.init(source,destination,graph_nodes)




