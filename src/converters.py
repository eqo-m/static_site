from textnode import TextNode,TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from block import BlockType
import re


def text_node_to_html_node(text_node):
    if text_node.text_type==TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type==TextType.BOLD:
        return LeafNode(tag="b",value=text_node.text)
    elif text_node.text_type==TextType.ITALIC:
        return LeafNode(tag="i",value=text_node.text)
    elif text_node.text_type==TextType.CODE:
        return LeafNode(tag="code",value=text_node.text)
    elif text_node.text_type==TextType.LINK:
        return LeafNode(tag="a",value=text_node.text,props={"href":f"{text_node.url}"})
    elif text_node.text_type==TextType.IMAGE:
        return LeafNode(tag="img",value="",props={"src":f"{text_node.url}","alt":f"{text_node.text}"})
    else:
        raise ValueError("Not a valid TextNode")

    
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes=[]

    for node in old_nodes:
        if node.text_type==TextType.TEXT:

            new_parts= node.text.split(delimiter)
            if len(new_parts)==1:
                    new_nodes.append(node)
                    continue
            if len(new_parts)%2==0:
                raise ValueError("invalid markdown")
            else: 
                for i in range(len(new_parts)):
                
                    if i%2==0 and new_parts[i]:
                        new_nodes.append(TextNode(new_parts[i],node.text_type))
                    if i%2!=0 and new_parts[i]:
                        new_nodes.append(TextNode(new_parts[i],text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes =[]

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            text = node.text
            for image in images:
                new_parts = text.split(f"![{image[0]}]({image[1]})", 1)
                if new_parts[0]:
                    new_nodes.append(TextNode(new_parts[0],node.text_type))
                new_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
                text = new_parts[1]
            if text:
                new_nodes.append(TextNode(text,node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes =[]

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            text = node.text
            for link in links:
                new_parts = text.split(f"[{link[0]}]({link[1]})", 1)
                if new_parts[0]:
                    new_nodes.append(TextNode(new_parts[0],node.text_type))
                new_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
                text = new_parts[1]
            if text:
                new_nodes.append(TextNode(text,node.text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    text = [TextNode(text,TextType.TEXT)]
    text = split_nodes_image(text)
    text = split_nodes_link(text)
    delimiters = {
        "**":TextType.BOLD,
        "_":TextType.ITALIC,
        "`":TextType.CODE
    }
    for del_type in delimiters.items():
        text = split_nodes_delimiter(text,del_type[0],del_type[1])
    return text


def markdown_to_blocks(doc):
    blocks = doc.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks



def block_to_block_type(block):
  lines = block.split("\n")
  if block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  
  if re.match(r'^#{1,6} .+',block):
    return BlockType.HEADING
  
  if all(line.startswith('>') for line in lines):
    return BlockType.QUOTE
  
  if all(re.match(r'^\- ',line)for line in lines):
    return BlockType.UNORDERED_LIST
  
  if all(re.match(r'^\d+\. ',line) for line in lines):
    numbers = [int(re.match(r'^(\d+)\.',line).group(1)) for line in lines]
    if numbers == list(range(1,len(lines)+1)):
        return BlockType.ORDERED_LIST
    
  return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    div_children = []

    for block in blocks:
        block_html_node = block_to_html(block)
        div_children.append(block_html_node)
    return ParentNode("div",div_children,None)
        

def block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

        

def text_to_children(text):
    """ returns a list of HTMLNodes"""
    nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]
    return html_nodes

    
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    size = len(re.match(r"^(#+)",block).group(1))
    if size + 1 >= len(block):
        raise ValueError(f"Invalid size : {size}")
    text = block[size + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{size}",children) 

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)