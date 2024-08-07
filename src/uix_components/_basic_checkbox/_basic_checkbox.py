from uix import Element
from uix.elements import check, label

checkbox_css = """
.checkbox-container{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
}"""

def register_resources(cls):
    cls.register_style("checkbox_css", checkbox_css)
    return cls

@register_resources
class basic_checkbox(Element):
    def __init__(
            self,
            id=None,
            label_text=None,
            value=None,
            callback=None,
            **kwargs
        ):
        super().__init__(id=id, **kwargs) # value won't be sent to super class, only used to set checkbox value
        self.label = label_text
        self.callback = callback
        self.checkboxID = id + "-checkbox"
        self.labelID = id + "-label"
        self.cls("checkbox-container")

        with self:
            self.checkbox = check(id=self.checkboxID, value=value).on("click", self.set_value)
            label(usefor=self.checkbox.id, value=self.label)

    def set_value(self, ctx, id, value):
        self.checkbox.value = value
        if self.callback:
            self.callback(ctx,id, value)
