import unittest
from core.warehouse import Node, Warehouse
from math import sqrt

class TestWarehouse(unittest.TestCase):
    def test_distance(self):
        node1 = Node(0, 0)
        node2 = Node(3, 4)
        warehouse = Warehouse({f"{node1.x},{node1.y}": node1, f"{node2.x},{node2.y}": node2})
        
        # Check distance between nodes (should be 5)
        self.assertEqual(warehouse.get_distance(node1, node2), 5, "Distance should be 5")

    def test_heuristics(self):
        node1 = Node(0, 0)
        node2 = Node(3, 4)
        warehouse = Warehouse({f"{node1.x},{node1.y}": node1, f"{node2.x},{node2.y}": node2})
        warehouse.goal = node2

        # Assign heuristics and check value
        warehouse.assign_heuristics()
        self.assertEqual(node1.heuristic, 5, "Node 1 heuristic should be 5")
        self.assertEqual(node2.heuristic, 0, "Node 2 heuristic should be 0")

if __name__ == "__main__":
    unittest.main()
