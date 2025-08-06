import re
from converters import markdown_to_html_node
from htmlnode import HTMLNode

def extract_title(markdown):
    header = re.search(r"^#(.*)$",markdown, re.M)
    if not header:
        raise ValueError("No header found")
    return header.group(1).strip()

def generate_page(from_path,template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read markdown path

    try:
        with open(from_path,"r") as file:
            markdown = file.read()
    except Exception as e:
        print(f"Error : {e}")

    try:
        with open(template_path,"r") as file:
            template = file.read()
    except Exception as e:
        print(f"Error : {e}")

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html=template.replace("{{ Title }}",title).replace("{{ Content }}",content)

    

    

    

        




