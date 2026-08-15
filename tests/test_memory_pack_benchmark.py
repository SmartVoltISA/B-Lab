from BENCHMARK.memory_pack_benchmark import graph_case
from TOOLS.graph_memory import open_graph, seal


def test_graph_pack_preserves_every_node_and_edge():
    nodes, edges = graph_case()
    restored_nodes, restored_edges = open_graph(seal(nodes, edges))
    assert restored_nodes == nodes
    assert restored_edges == edges
    assert len(restored_nodes) == len(nodes)
    assert len(restored_edges) == len(edges)
