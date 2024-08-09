from uix import Element
from uix.elements import canvas
from uix_components._chart_scatter.chart_scatter_utils import ChartUtils

script = """
    event_handlers["init-chart"] = function (id, value, event_name) {
        let chart = new Chart(id, value);
        elm = document.getElementById(id);
        elm.chart = chart;
    };
"""

def register_resources(cls):
    cls.register_script("chart-js", script)
    return cls

@register_resources
class chart_scatter(Element):
    def __init__(self, id, value=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.options = options
        self.canvas_id = id+"_canvas"

        self.chartData ={
            "type": "scatter",
            "data": {
                "datasets": [
                ],
            },
            "options": {
                "scales": {
					"x": {
						"type": "linear",
						"position": "bottom"
					},
				},
                "responsive": None,
                "plugins": {
                    "legend": {
                    "position": None,
                    },
                "title": {
                "display": None,
                "text": None
                    }
                }
            }
        }

        ChartUtils.dataset_importer(self.chartData, self.value)
        ChartUtils.set_options(self.chartData, self.options)

        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)

    def init(self):
        self.session.queue_for_send(self.canvas_id, self.canvas.value, "init-chart")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        ChartUtils.dataset_importer(self.chartData, value)
        ChartUtils.set_options(self.chartData, self.options)
        with self:
            self.canvas = canvas(id=self.canvas_id,value = self.chartData)
        self.init()
        self.update()
