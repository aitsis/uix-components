import io
from uuid import uuid4
import os
from PIL import Image
from uix import Element, app

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_script("seadragon-lib", "/_image_viewer/openseadragon.min.js", is_url=True)
    cls.register_script("seadragon-js", "/_image_viewer/seadragon.js", is_url=True)
    cls.register_script("interactive_seadragon", "/_image_viewer/openseadragon-fabricjs-overlay.js", is_url=True)
    cls.register_script("fabric-js-local", "/_fabric/fabric.min.js", is_url=True)
    
    return cls

@register_resources
class image_viewer(Element):
    def __init__(self, id = None, value=None, buttonGroup=None, zoom=False, size=(500,500), viewer="seadragon", button_groupId=None):
        super().__init__(id=id, value=value)
        self.tag = "div"
        self.value_name = None
        self.viewer = viewer
        self.config = {
            "zoom":  zoom,
            "image": value,
            "buttonGroupId": button_groupId
        }
        if buttonGroup is not None:
            self.config["buttonGroup"] = buttonGroup

        if size is not None and len(size) == 2:
            self.size(*size)

        self.has_PIL_image = False
        self.set_later = True

    def init(self):
        self.session.queue_for_send(self.id, self.config, "init-" + self.viewer)
        self.value = self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Image.Image):
            self.has_PIL_image = True
            self._value = self._create_image_url(value)
        else:
            self.has_PIL_image = False
            self._value = value

        if self._value is not None:
            if self.set_later:
                self.session.queue_for_send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), self.viewer)
            else:
                self.session.send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), self.viewer)
            self.set_later = False

    def __del__(self):
        if self.has_PIL_image:
            app.files[self.id] = None

    def _create_image_url(self,img):
        if self.id is None:
            self.id = str(uuid4())
        temp_data = io.BytesIO()
        img.save(temp_data, format="png")
        temp_data.seek(0)
        app.files[self.id] = {"data":temp_data.read(),"type":"image/png"}
        return "/download/"+self.id + "?" + str(uuid4())

    def value_to_command(self,command,value):
        return { "action": command, "value": value }


    def zoom_in(self):
        self.session.send(self.id, self.value_to_command("zoomIn", None), self.viewer) 

    def zoom_out(self):
        self.session.send(self.id, self.value_to_command("zoomOut", None), self.viewer)                          

    def home(self):
        self.session.send(self.id, self.value_to_command("home", None), self.viewer)

    def fullscreen(self):
        self.session.send(self.id, self.value_to_command("fullscreen", None), self.viewer)

    def download(self):
        self.session.send(self.id, self.value_to_command("download", None), self.viewer)

    def open_edit_area(self, value):
        self.session.send(self.id, self.value_to_command("open-edit-area", value), self.viewer)

    def edit_brush(self, color,opacity, brushSize):
        brushSize = int(brushSize)
        self.session.send(self.id, self.value_to_command("editBrush", {"color": color, "opacity": opacity, "brushSize": brushSize}), self.viewer)


    def set_pan_mode(self):
        self.session.send(self.id, self.value_to_command("setPanMode", None), self.viewer)

    def eraser_tool(self, brushSize, value=None):
        brushSize = int(brushSize)
        self.session.send(self.id, self.value_to_command("eraserBrush", {"brushSize": brushSize, "isChecked": value}), self.viewer)
