import pytest

from TOOLS.graph_memory import open_graph, seal


def test_graph_round_trip_preserves_nodes_and_edges():
    nodes = {"A": {"state": 0}, "B": {"state": 1}, "C": {"state": 0}}
    edges = [("A", "B", "transition"), ("B", "C", "transition")]
    blob = seal(nodes, edges)
    nodes2, edges2 = open_graph(blob)
    assert nodes2 == nodes
    assert edges2 == edges


def test_graph_round_trip_preserves_exact_edge_order():
    nodes = {"A": {}, "B": {}, "C": {}, "D": {}}
    # Deliberately non-sorted order: this is historical sequence, not a set.
    edges = [
        ("C", "D", "step-3"),
        ("A", "B", "step-1"),
        ("B", "C", "step-2"),
    ]
    blob = seal(nodes, edges)
    nodes2, edges2 = open_graph(blob)
    assert nodes2 == nodes
    assert edges2 == edges


def test_dangling_edge_is_rejected():
    with pytest.raises(ValueError):
        seal({"A": {}}, [("A", "MISSING", "bad")])


def test_corruption_is_not_presented_as_valid_memory():
    nodes = {"A": {}, "B": {}}
    edges = [("A", "B", "link")]
    blob = bytearray(seal(nodes, edges))
    blob[-1] ^= 0x01
    with pytest.raises(ValueError, match="integrity"):
        open_graph(bytes(blob))
