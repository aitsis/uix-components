from uix import Element, app
from uix.elements import unorderedlist, listitem, label, div, check

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("_basic_tree_view_css", "/_basic_tree_view/_basic_tree_view.css", is_url=True)
    return cls

@register_resources
class basic_tree_view(Element):
    def __init__(self, id, data):
        super().__init__(id=id)
        if data is None:
            data = {}

        def create_tree(key, data, component):
            with listitem(id="li-"+key.lower()).style("list-style","none"):
                label_attributes = {"usefor": "trigger-" + key.lower()}
                check(id="trigger-" + key.lower()).cls("comp_type")
                self.label = label(value=key, **label_attributes)
                if isinstance(data, dict) and data:
                    self.label.cls("super-class")
                    with self.label:
                        div("").cls("plus").tag = "span"
                    with unorderedlist("").cls("pure-tree"):
                        for sub_key in data:
                            create_tree(sub_key, data[sub_key], component)

        with self:
            with unorderedlist("").cls("pure-tree main-tree"):
                for main_title in data:
                    create_tree(main_title, data[main_title], check)
