from uix import app, Element
from uix.elements import details, text, div

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("_basic_details_css", "/_basic_details/_basic_details.css", is_url=True)
    return cls

@register_resources
class basic_details(Element):
    def __init__(self, value, id = None,label_=None, acc_elements = list()):
        super().__init__(value,id = id)

        self.cls("border")
        self.style("width","100%")
        with self:
            with details(id=id+"-details").cls("default square"):
                text(label_).tag="summary"
                if acc_elements:
                    for element in acc_elements:
                        with div().cls("details_acc"):
                            element()
