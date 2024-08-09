from uix import app
from uix.elements import span, div

print("Imported: tooltip")
app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("_tooltip_css", "/_tooltip/_tooltip.css", is_url=True)
    return cls

@register_resources
class tooltip(span):
    def __init__(self,value:str = None,id:str = None, position="top"):
        super().__init__(value, id = id)
        self.cls(f"tooltiptext tooltip-{position}")
        self.parent.cls("tooltip")

title = "Tooltip"

description = '''
## tooltip("AÇIKLAMA BURAYA", position="top")

1. tooltip position parametresi alabileceği seçenekler: top, bottom, right, left. (String olarak yazılmalı)
2. postion parametresi eklenmezse varsayılan olarak top gelir.
3. Her elemana alt eleman olarak eklenebilir.(button, text, icon vs.) Parent ına tooltip stil sınıfını otomatik ekler.
4. with ile yazılırsa içine istenilen eleman eklenebilir.


| attr                  | desc                                                      |
| :-------------------- | :-------------------------------------------------------- |
| tooltip               | Tooltip içeriğinde yazacak metin.                         |
| position              | Tooltip balonu görüntüleneceği yön.                       |
'''

sample = """
with text('Bu nedir?'):
    tooltip("Tooltip içeriğidir.")
"""
