from uix import app
from uix.elements import canvas

app.serve_module_static_files(__file__)

def register_resources(cls):
    # cls.register_script("fabric-cdn", "https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js", is_url=True)
    # cls.register_script("image-cropper", "/_fabric/image_cropper.js", is_url=True)
    cls.register_script("fabric-js-local", "/_fabric/fabric.min.js", is_url=True)
    cls.register_script("image-cropper", "/_fabric/image_cropper.js", is_url=True)
    return cls

@register_resources
class fabric(canvas):
    def __init__(self, id, value=None, width= 300, height= 150):
        super().__init__(id=id, value=value, width=width, height=height)
        self.tag = "canvas"
        self.value_name = None
        print("fabric init", self.id)
        print("width", width)
        print("height", height)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if self._value is not None:
            self.session.send(self.id, self.value_to_command("loadImage", self._value), "image-cropper")

    def init(self):
        if self.id is not None:
            self.session.queue_for_send(self.id, "", "init-image-cropper")
        if self.value is not None:
            self.session.queue_for_send(self.id, self.value_to_command("loadImage", self._value), "image-cropper")

    # def closeImage(self):
    #     self.session.send(self.id, self.value_to_command("close", None), "image-cropper")

    def crop_and_move(self, axis, scale):
        self.session.send(self.id, self.value_to_command("cropAndMove", {"axis": axis, "scale": scale}), "image-cropper")

    # def repeatImage(self, value):
    #     self.session.send(self.id, self.value_to_command("repeatImage", value), "image-cropper")

    # def resetImage(self):
    #     self.session.send(self.id, self.value_to_command("resetImage", ""), "image-cropper")

    def value_to_command(self, command, value):
        command = {
            "action": command,
            "value": value
    }
        return command
