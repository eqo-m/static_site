from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props)
    

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node mist have tag")
        if not self.children:
            raise ValueError("Parent Node must have children")
        props = self.props_to_html()

        inner_html = "".join([child.to_html() for child in self.children])   
        return f'<{self.tag}{props}>{inner_html}</{self.tag}>'