import uix
from uix.elements import canvas

uix.app.serve_module_static_files(__file__)

script = """
    event_handlers["init-chart"] = function (id, value, event_name) {
        Chart.register(ChartDataLabels);
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
"""

def register_resources(cls):
    cls.register_script("chart-js-umd", "/_chart/chart.umd.js", is_url=True)
    cls.register_script("chartjs-plugin-datalabels", "/_chart/chartjs-plugin-datalabels.min.js", is_url=True)
    cls.register_script("chart-js", script)
    return cls

@register_resources
class chart(uix.Element):
    def __init__(self, id, value=None):
        super().__init__(id=id, value=value)
        self.value_name = None
        self.canvas_id = id + "_canvas"
   
        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.value)

    def init(self):
        self.session.queue_for_send(self.canvas_id, self.canvas.value, "init-chart")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.value)
        self.init()
        self.update()
