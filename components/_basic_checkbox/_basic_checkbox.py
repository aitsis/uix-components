import uix
from uix.elements import check, label

class basic_checkbox(uix.Element):
    def __init__(
            self,
            id=None,
            label_text=None,
            value=None,
            callback=None,
            **kwargs
        ):
        super().__init__(value=value,id=id,**kwargs)
        self.label = label_text
        self.callback = callback
        self.checkboxID = id + "-checkbox"
        self.labelID = id + "-label"

        (
            self
                .style("display", "flex")
                .style("justify-content", "center")
                .style("align-items", "center")
                .style("gap","5px")
        )
        with self:
            if self.value:
                self.checkbox = (
                    check(id=self.checkboxID)
                        .on("click", self.set_value)
                        .checked()
                )
            else:
                self.checkbox = check(id=self.checkboxID).on("click", self.set_value)
            
            label(
                usefor=self.checkbox.id,
                value=self.label
            )

    def set_value(self, ctx, id, value):
        self.checkbox.value = value
        print("Checkbox value:", value)
        if self.callback:
            self.callback(id, value)