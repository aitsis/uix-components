from uix.elements import canvas
from uix_components import chart
from uix_components._chart.chart_utils import ChartUtils

class chart_bar(chart):
    def __init__(self, id, value=None, labels=None, options=None):
        super().__init__(id=id, value=value)
        self.labels = labels
        self._value = value
        self.value_name = None
        self.options = options

        self.chartData ={
            "type": "bar",
            "data": {
                "labels": [],

                "datasets": [
                ],
            },
            "options": {
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
                        "anchor": "center",
                        "align": "center",
                        "display": True,
                        "color": "white",
                        "font": {
                            "family": "Exo 2",
                            "size": 14,
                            "weight": "bold",
                        },
                    }
                }
            },
        }

        ChartUtils.dataset_importer(self.chartData, self.value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)

        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        ChartUtils.dataset_importer(self.chartData, value, self.labels)
        ChartUtils.set_options(self.chartData, self.options)
        with self:
            self.canvas = canvas(id=self.canvas_id, value=self.chartData)
        #self.init()
        self.update()
