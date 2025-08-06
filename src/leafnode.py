from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self,tag=None,value=None,props=None):
        super().__init__(tag=tag,children=None,props=props)
        self.value=value
        

    def to_html(self):
        if self.value is None:
            raise ValueError("Must contain a value")
        
        if not self.tag:
            return self.value
        
        if self.props:
            props = "".join([f' {k}="{v}"' for k,v in self.props.items()])
        else:
            props = ""

        return f'<{self.tag}{props}>{self.value}</{self.tag}>'
    