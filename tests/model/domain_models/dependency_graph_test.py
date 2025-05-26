import networkx as nx
import pytest

from model.domain_model.spreadsheet.cell_range import CellRange
from model.domain_model.spreadsheet.dependency_graph import DependencyGraph
from model.domain_model.spreadsheet.range_reference import RangeReference, RangeReferenceType


@pytest.fixture
def empty_graph():
    graph = nx.DiGraph()
    return DependencyGraph(graph)


@pytest.fixture
def simple_graph():
    graph = nx.DiGraph()
    a1 = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    b1 = RangeReference('book', 'sheet', 'B1', RangeReferenceType.CELL)
    c1 = RangeReference('book', 'sheet', 'C1', RangeReferenceType.CELL)

    graph.add_node(a1, cell_range=CellRange(a1, '1', '=1'))
    graph.add_node(b1, cell_range=CellRange(b1, '2', '=A1'))
    graph.add_node(c1, cell_range=CellRange(c1, '3', '=B1'))

    graph.add_edge(a1, b1)
    graph.add_edge(b1, c1)

    return DependencyGraph(graph)


def test_get_cell_range(empty_graph):
    dummy = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    assert empty_graph.get_cell_range(dummy) is None


def test_get_cell_ranges(simple_graph):
    cell_ranges = simple_graph.get_cell_ranges()
    assert len(cell_ranges) == 3
    assert all(isinstance(cr, CellRange) for cr in cell_ranges)


def test_has_precedent_and_dependent(simple_graph):
    a1 = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    c1 = RangeReference('book', 'sheet', 'C1', RangeReferenceType.CELL)

    assert not simple_graph.has_precedent(a1)
    assert simple_graph.has_dependent(a1)
    assert simple_graph.has_precedent(c1)
    assert not simple_graph.has_dependent(c1)


def test_resolve_dependents_to_cell_level(simple_graph):
    a1 = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    result = simple_graph.resolve_dependents_to_cell_level(a1)
    refs = {ref.reference for ref in result}
    assert 'B1' in refs
    assert 'C1' not in refs


def test_resolve_precedents_to_cell_level(simple_graph):
    c1 = RangeReference('book', 'sheet', 'C1', RangeReferenceType.CELL)
    result = simple_graph.resolve_precedents_to_cell_level(c1)
    refs = {ref.reference for ref in result}
    assert 'B1' in refs
    assert 'A1' not in refs


def test_get_precedents_and_dependents(simple_graph):
    b1 = RangeReference('book', 'sheet', 'B1', RangeReferenceType.CELL)
    precedents = simple_graph.get_precedents(b1)
    dependents = simple_graph.get_dependents(b1)
    assert any(p.reference == 'A1' for p in precedents)
    assert any(d.reference == 'C1' for d in dependents)


def test_resolve_precedents_with_range():
    graph = nx.DiGraph()
    a1 = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    b1_c1 = RangeReference('book', 'sheet', 'B1:C1', RangeReferenceType.RANGE)
    b1 = RangeReference('book', 'sheet', 'B1', RangeReferenceType.CELL)
    c1 = RangeReference('book', 'sheet', 'C1', RangeReferenceType.CELL)

    graph.add_node(a1, cell_range=CellRange(a1, '1', '=SUM(B1:C1)'))
    graph.add_node(b1_c1, cell_range=CellRange(b1_c1, '', ''))
    graph.add_node(b1, cell_range=CellRange(b1, '2', '=2'))
    graph.add_node(c1, cell_range=CellRange(c1, '3', '=3'))

    graph.add_edge(b1_c1, a1)
    graph.add_edge(b1, b1_c1)
    graph.add_edge(c1, b1_c1)

    dep_graph = DependencyGraph(graph)
    precedents = dep_graph.resolve_precedents_to_cell_level(a1)
    assert b1 in precedents
    assert c1 in precedents


def test_resolve_with_named_range():
    graph = nx.DiGraph()
    a1 = RangeReference('book', 'sheet', 'A1', RangeReferenceType.CELL)
    named = RangeReference('book', None, 'MyNamed', RangeReferenceType.DEFINED_NAME)  # Named range 'referring' to A1
    b1 = RangeReference('book', 'sheet', 'B1', RangeReferenceType.CELL)

    graph.add_node(a1, cell_range=CellRange(a1, '1', '=1'))
    graph.add_node(named, cell_range=CellRange(named, '', ''))
    graph.add_node(b1, cell_range=CellRange(b1, '2', '=MyNamed'))

    graph.add_edge(a1, named)
    graph.add_edge(named, b1)

    dep_graph = DependencyGraph(graph)

    dependents = dep_graph.resolve_dependents_to_cell_level(a1)
    assert b1 in dependents

    precedents = dep_graph.resolve_precedents_to_cell_level(b1)
    assert a1 in precedents
