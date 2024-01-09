import uix
from uix.elements import select, option

class basic_select(uix.Element):
    def __init__(
            self,
            id=None,
            value=None,
            options : dict[str, str] = None,
            callback=None,
            **kwargs
        ):
        super().__init__( id=id, **kwargs)
        self.selectID = id + "-select"
        self.options = options
        self.callback = callback

        with (
            select(id=self.selectID)
                .on("change", self.on_change)
        ) as _select:
            self.select = _select
            if type(self.options) == list:
                for _option in self.options:
                    if _option["isSelect"] == True:
                        option(id=_option['id'], value=_option['value']).selected()
                    else:
                        option(id=_option['id'], value=_option['value'])
            else:
                for key, value in self.options.items():
                    if value["isSelect"] == True:
                        option(value=key, id=value["id"]).selected()
                    else:
                        option(value=key, id=value["id"])

    def on_change(self, ctx, id, value):
        self.value = value
        print("Select value:", value)
        if self.callback:
            self.callback(self.id, value)