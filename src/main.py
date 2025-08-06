from textnode import TextNode
from site_functions import copy_files,generate_page,clear_directory,generate_pages_recursive
import sys
import os 

def main():
    if len(sys.argv)>1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    clear_directory("./docs")
    copy_files("static/","./docs")
    basepath = os.path.join("/",basepath)
    generate_pages_recursive("./content/","./template.html","./docs",basepath)

    #generate_page("content/index.md","template.html","public/index.html")
    #generate_page("content/blog/glorfindel/index.md","template.html","public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md","template.html","public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md","template.html","public/blog/majesty/index.html")
    #generate_page("content/contact/index.md","template.html","public/contact/index.html")


main()