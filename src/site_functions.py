import os
import shutil
from pathlib import Path
from converters import markdown_to_html_node
from parentnode import ParentNode
from htmlnode import HTMLNode




def copy_files(source,destination):
    if not os.path.exists(source):
        raise OSError(f"Source path not found: {source}")
    if not os.path.exists(destination):
        raise OSError(f"Destination path not found: {destination}")
    
    #delete contents of destination
    clear_directory(os.path.abspath(destination))

    dir_content = os.listdir(source)

    for content in dir_content:
        src = os.path.join(source,content)
        target = os.path.join(destination,content)

        if os.path.isfile(src):
            shutil.copy(src,target)

        if os.path.isdir(src):
           os.mkdir(target)
           copy_files(src,target) 


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip('# ').strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as m:
        markdown = m.read()
        with open(template_path) as t:
            template = t.read()
            html = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            final_html=template.replace('{{ Title }}',title)
            final_html = final_html.replace('{{ Content }}',html )
            final_html = final_html.replace('href="/', 'href="' + basepath)
            final_html = final_html.replace('src="/', 'src="' + basepath)
            dest_dir = os.path.dirname(dest_path)
            if dest_dir:
                os.makedirs(dest_dir,exist_ok=True)
            with open (dest_path,"w") as d:
                d.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    content_paths = []
    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content,content)
        target_path = os.path.join(dest_dir_path,content)
        
        if os.path.isfile(content_path):
            if content.endswith(".md"):
                target_path = os.path.splitext(target_path)[0] + ".html"
                generate_page(content_path,template_path,target_path,basepath)
        elif os.path.isdir(content_path):
            generate_pages_recursive(content_path,template_path,target_path,basepath)          



def clear_directory(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path,filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)