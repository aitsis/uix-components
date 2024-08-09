from uix import Element
from uix.elements import text, image, div

style = """
@keyframes loading-bar {
    0% {
        width: 0%;
        background-color: #00573d;
    }

    100% {
        background-color: #333333;
        width: 100%;
    }
}

@keyframes ping-black {
    0% {
        opacity: 0.7;
    }
    75% {
        opacity: 1;
    }
    100% {
        opacity: 0.7;
    }
}

.logo-div {
    position: absolute;
    top: 35%;
    left: 40%;
    height: 30%;
    width: 20%;
}

.loading-logo {
    height: 100%;
    object-fit: contain;
    width: 100%;
}

.hidden {
    display: none;
}"""

def register_resources(cls):
    cls.register_style("loading_component_css", style)
    return cls

@register_resources
class basic_loading(Element):
    def __init__(self, value = None, id = None, timer = 10):
        super().__init__(value, id = id)
        self.cls("wall hall").style("position: relative;")

        with self:
            with div().cls("hall")as loading:
                loading.style(f"animation: loading-bar {timer}s ease-in-out forwards, ping-black 1.5s infinite; border-radius: 3px;")
                pass
            with div().style("position: absolute; top: .2rem; right: 1rem"):
                text(id = "text1" ,value = "Estimated Time: " + str(timer) + " s").cls("loading-title")
            with div().cls("logo-div"):
                image(value="https://aitools.ait.com.tr/AIT_AI_LOGO.png").cls("loading-logo")

    def start(self):
        self.remove_class("hidden")

    def stop(self):
        self.add_class("hidden")
