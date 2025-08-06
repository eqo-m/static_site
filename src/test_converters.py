import unittest
from textnode import TextNode,TextType
from leafnode import LeafNode
from block import BlockType
from converters import text_node_to_html_node,extract_markdown_images,extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes,markdown_to_blocks, block_to_block_type, markdown_to_html_node, block_to_html


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


if __name__ == "__main__":
    unittest.main()

class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_single_image(self):
        node = TextNode("![alt text](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode("![start image](https://example.com/start.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("Text before ![end image](https://example.com/end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and another [second link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_single_link(self):
        node = TextNode("[click here](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_split_link_at_start(self):
        node = TextNode("[start link](https://example.com/start) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start link", TextType.LINK, "https://example.com/start"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode("Text before [end link](https://example.com/end)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end link", TextType.LINK, "https://example.com/end"),
            ],
            new_nodes,
        )

    def test_split_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_empty_link_text(self):
        node = TextNode("Check out [](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_complex_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_multiple_formatting(self):
        text = "**Bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is just a regular paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a h6 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> This is a quote\n> with multiple lines\n> all starting with >"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_incremental(self):
        block = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_not_all_lines(self):
        block = "> This is a quote\nThis line is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_not_all_lines(self):
        block = "- First item\nNot a list item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_not_ending(self):
        block = "```\nprint('hello')\nprint('world')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### This has too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestBlockToHTML(unittest.TestCase):
    def test_paragraph_to_html(self):
        block = "This is a paragraph"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].value, "This is a paragraph")

    def test_heading_to_html(self):
        block = "# This is a heading"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "h1")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].value, "This is a heading")

    def test_code_to_html(self):
        block = "```\nprint('hello')\n```"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(html_node.children[0].tag, "code")

    def test_quote_to_html(self):
        block = "> This is a quote"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "blockquote")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].value, "This is a quote")

    def test_unordered_list_to_html(self):
        block = "- First item\n- Second item"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "ul")
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "li")
        self.assertEqual(html_node.children[0].children[0].value, "First item")

    def test_ordered_list_to_html(self):
        block = "1. First item\n2. Second item"
        html_node = block_to_html(block)
        self.assertEqual(html_node.tag, "ol")
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "li")
        self.assertEqual(html_node.children[0].children[0].value, "First item")


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_simple_markdown(self):
        markdown = "# Heading\n\nThis is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "p")

    def test_complex_markdown(self):
        markdown = """# Main Heading

This is a **bold** paragraph with _italic_ text.

- First item
- Second item

> This is a quote

```
print('code block')
```"""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 5)
        
        # Check heading
        self.assertEqual(html_node.children[0].tag, "h1")
        
        # Check paragraph
        self.assertEqual(html_node.children[1].tag, "p")
        
        # Check unordered list
        self.assertEqual(html_node.children[2].tag, "ul")
        
        # Check quote
        self.assertEqual(html_node.children[3].tag, "blockquote")
        
        # Check code block
        self.assertEqual(html_node.children[4].tag, "pre")

    def test_empty_markdown(self):
        markdown = ""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 0)


