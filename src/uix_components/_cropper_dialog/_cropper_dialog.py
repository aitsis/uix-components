
from uix import Element, app
from uix.elements import button, canvas, text
from uix_components._basic_dialog._basic_dialog import basic_dialog

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_script("imask.min.js", "/_cropper_dialog/_cropper_dialog.js", is_url=True)
    return cls

@register_resources
class cropper_dialog(Element):
    def __init__(self, id=None, image_url=None, callback=None):
        super().__init__(id=id)
        self.callback = callback
        self.image_url = image_url
        self.dialog = basic_dialog(id=self.id + "-dialog", elements=[self.crop_dialog]).size("42vw","70vh")

    def show(self):
        self.dialog.show()
        self.session.send(self.id, {"imageUrl": self.image_url, "cropCanvas" : self.canvas.id}, "init-cropper")

    def hide(self):
        self.dialog.hide()

    def crop_dialog(self):
        self.canvas = canvas(id=self.id+"-cropper").style("border","2px solid black")
        self.canvas.attrs["width"] = 800
        self.canvas.attrs["height"] = 450
        text("* Crop işlemi yapmak için resme çift tıklayın.")
        text("* İşleminiz bittiğinde imaj dışarısındaki bir alana tıklayarak işlemi gerçekleştirmiş olursunuz.")
        text("* Done butonuna basarak işlemi tamamlayabilirsiniz.")
        button("Done", id="doneButton").on("cropper-done", self.callback)
