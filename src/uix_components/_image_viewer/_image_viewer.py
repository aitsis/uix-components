import uix
import os
uix.html.add_script_source('seadragon-js-lib', 'openseadragon.min.js',localpath=__file__,beforeMain=False)
uix.html.add_script_source('seadragon', 'seadragon.js',localpath=__file__, beforeMain=False)
icons_path = os.path.join(os.path.dirname(__file__), "icons")


class image_viewer(uix.Element):
    def __init__(self, id = None, value=None, buttonGroup={}, zoom=False, size=(500,500)):
        super().__init__(id=id, value=value)
        self.tag = "div"
        self.value_name = None
        self.buttonGroup = buttonGroup
     
        self.config = {
            "buttonGroup": buttonGroup,
            "zoom":  zoom,
            "image": value,
        }
        if size is not None and len(size) == 2:
            self.size(*size)
        

    def init(self):
        self.session.queue_for_send(self.id, self.config, "init-seadragon")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        print("value",value)
        self._value = value
        if self._value is not None:
            self.session.send(self.id, self.value_to_command("open",{"type": "image","url": self._value}), "seadragon")

    def value_to_command(self,command,value):
        return { "action": command, "value": value }


    def zoom_in(self):
        self.session.send(self.id, self.value_to_command("zoomIn", None), "seadragon")

    def zoom_out(self):
        self.session.send(self.id, self.value_to_command("zoomOut", None), "seadragon")

    def home(self):
        self.session.send(self.id, self.value_to_command("home", None), "seadragon")
    
    def fullscreen(self):
        self.session.send(self.id, self.value_to_command("fullscreen", None), "seadragon")
    
    def download(self):
        self.session.send(self.id, self.value_to_command("download", None), "seadragon")

    def save(self):
        #save fonksiyonu yazılacak
        pass


        