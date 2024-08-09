from uix import Element, app, T
from uix.core.session import context
from uix.elements import table, tr, th, td, div, button, input, span,thead, tbody,icon

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("datatables_css", "/_data_table/datatables.css", is_url=True)
    cls.register_script("data-table-js", "/_data_table/datatables.min.js", is_url=True)
    cls.register_script("data-table-init-js", "/_data_table/datatable_comp.js", is_url=True)
    return cls

@register_resources
class data_table(Element):
    def __init__(self, id=None, data=[],cols=None,dialog_id=None,callback=None,config=None):
        super().__init__(id=id)
        columns = []
        self.id = id
        self.config = {
            "data":  data,
            "columns": columns,
            "dataTable_config": config,
            "dialog_id": dialog_id,
            "isEditable": False
        }

        if callback and dialog_id:
            self.config["isEditable"] = True
            context.session.context.elements[dialog_id].on("info_dialog_open", callback)

        with self:
            with table(id=self.id + "-table",value="").cls("stripe hover"):
                with thead():
                    with tr():
                        if cols:
                            for key, value in cols.items():
                                columns.append({"data": key})
                                th(T(value))
                        else:
                            for key in data[0].keys():
                                columns.append({"data": key})
                                th(T(key))



    def init(self):
        self.session.send(self.id+"-table", self.config ,"init-data-table")

    def update_table(self,value):
         self.config["data"] = value
         self.session.send(self.id+"-table", self.config,"reload")
