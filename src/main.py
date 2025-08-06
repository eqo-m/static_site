from textnode import TextNode
from site_functions import copy_files,generate_page,clear_directory,generate_pages_recursive

def main():
    
    clear_directory("public")
    copy_files("static/","public/")
    generate_pages_recursive("content/","template.html","public/")

    #generate_page("content/index.md","template.html","public/index.html")
    #generate_page("content/blog/glorfindel/index.md","template.html","public/blog/glorfindel/index.html")
    #generate_page("content/blog/tom/index.md","template.html","public/blog/tom/index.html")
    #generate_page("content/blog/majesty/index.md","template.html","public/blog/majesty/index.html")
    #generate_page("content/contact/index.md","template.html","public/contact/index.html")


main()