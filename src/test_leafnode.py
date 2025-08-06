import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_text(self):
        node = LeafNode("p","TestString",{"text-align":"center","color":"red"})
        self.assertEqual(node.value,"TestString")

    def test_no_props(self):
        node = LeafNode("p","TestString")
        self.assertEqual(node.to_html(),"<p>TestString</p>")

    def test_props(self):
        node = LeafNode("p", "TestString", {"text-align": "center", "color": "red"})
        actual_html = node.to_html()
        expected_html = '<p text-align="center" color="red">TestString</p>'
        print(f"Actual:   '{actual_html}'") # Use repr() or quotes to see hidden chars
        print(f"Expected: '{expected_html}'")
        self.assertEqual(actual_html, expected_html)


    

