import types
from uix import Element, app
from uix.elements import textarea
from uix_components._basic_alert._basic_alert import basic_alert

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("_codemirror_css", "/_codemirror/_codemirror.css", is_url=True)
    cls.register_script("_codemirror_init.js", "/_codemirror/_codemirror_init.js", is_url=True)
    cls.register_script("_codemirror_python.js", "/_codemirror/_codemirror_python.js", is_url=True)
    cls.register_script("_codemirror.js", "/_codemirror/_codemirror.js", is_url=True)
    return cls

@register_resources
class codemirror(Element):
    def __init__(self, id=None, cm_parent_id=None, code=None, func_name=None):
        super().__init__(id=id)
        self.cm_parent_id = cm_parent_id
        self.func_name = func_name
        self.code = code

        with self:
            self.alert= basic_alert(id="comp_alert")
            textarea(id="codemirror").cls("wall hall").on("save", self.on_save)

    def on_save(self, ctx, id, value):
        try:
            modified_code = value.replace("\t", "    ")
            dynamic_module = types.ModuleType("dynamic_module")
            globals().update(vars(dynamic_module))
            exec(modified_code, dynamic_module.__dict__)
            file_example_func = getattr(dynamic_module, self.func_name, None)

            if file_example_func:
                with ctx.elements[self.cm_parent_id] as parent_container:
                    file_example_func()
                    parent_container.update()
                self.show_alert("alert-success", "Code executed successfully")
            else:
                self.show_alert("alert-danger", f"Function {self.func_name} not found in code")

        except SyntaxError as syntax_err:
            self.show_alert("alert-danger", f"Syntax Error: {syntax_err}")

        except NameError as name_err:
            self.show_alert("alert-danger", f"Name Error: {name_err}")

        except Exception as e:
            self.show_alert("alert-danger", "Error compiling/executing code: " + str(e))

    def init(self):
        self.session.queue_for_send(self.id, {"string": self.code}, "codemirror-init")

    def show_alert(self, alert_type, message):
        self.alert.open(alert_type, message)
