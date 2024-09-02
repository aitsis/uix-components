from uix.elements import canvas
from uix_components import chart
from uix_components._chart.chart_utils import ChartUtils

class chart_scatter(chart):
    def __init__(self, id, value=None, labels=None, options=None):
        super().__init__(id=id, value=value)
        self._value = value
        self.value_name = None
        self.options = options

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
                    },
                     "datalabels": {
                         "display": False,
                     },
                },
            }
        }
        

        ChartUtils.dataset_importer(self.chartData, self.value)
        ChartUtils.set_options(self.chartData, self.options)

        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)

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
