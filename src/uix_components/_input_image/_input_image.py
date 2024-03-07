import uix
from uix.elements import file,col,text,label
from uix import T
from uix_components import image_viewer, fabric, button_group
uix.html.add_css_file("_input_image.css",__file__)

buttonGroupConfig = {
            "seadragon": {
                "Delete": {
                    "icon": "fa-solid fa-trash-can",
                    "icon_styles": {"font-size": "20px", "color": "var(--danger-color)"},
                },
            },
            "fabric": {
                "Delete": {
                    "icon": "fa-solid fa-trash-can",
                    "icon_styles": {"font-size": "20px", "color": "var(--danger-color)"},
                    "onClick": "",
                },
            }
        }
class input_image(uix.Element):
    def __init__(
            self,
            value=None,
            id=None,
            viewer="seadragon",
            callback=None
            ):
        super().__init__(value=value,id=id)
        self.imageID = None
        self.viewer_id = id + "-viewer"
        self.file_id = id + "-file"
        self.dropzone_id= id + "-dropzone"
        self.label_id = id + "-label"
        self.loading_file_id = id + "-loading-file"
        self.filename=""
        self.file_url=""
        self.on_upload_done = callback
        self.cls("wall hall input")
        self.style("position","relative")

        with self:
            self.file=file(id=self.file_id,accept="image/png, image/jpeg",multiple=False,callback=self.file_callback).cls("file-input")
            self.loading_file = col(id=self.loading_file_id).cls("loading-file hidden")

            with self.loading_file:
                col().cls("spinner")
                text(T("Uploading")+"...")

            with label(id=self.label_id,usefor=self.file_id).cls("dropzone-label") as dropzone_parent :
                self.dropzone_parent = dropzone_parent
                with col(id=self.dropzone_id).cls("dropzone") as dropzone_inside:
                    self.dropzone_inside = dropzone_inside
                    text(T("Click to upload")).style("font-size","1.5rem")
                    text(T("It supports only png , jpeg files . Upload size is limited to 10MB")).style("font-size","1rem")
                    
                if viewer == "seadragon":   
                    self.create_image_viewer("my_images/AIT_AI_LOGO.png")
                else:
                   self.create_fabric_viewer()

    def file_callback(self,ctx, id, event, data, status):
        if event == "select":
            self.upload_file(ctx, data, status)    
        elif event == "upload":
            self.upload_callback(ctx, id, data, status)
       
    def upload_file(self,ctx, data, value):
        self.dropzone_parent.set_style("display", "none")
        
        if data[0].size < 10000000 and (data[0].type == "image/png" or data[0].type == "image/jpeg"):
            self.file.upload(data[0].url)
            self.dropzone_image.value =data[0].url
            self.file_url = data[0].url
            self.filename = data[0].name
        else:
            ctx.elements["comp_alert"].open("alert-danger", T("File size should be less than 10MB and file type should be png or jpeg."))
            self.dropzone_parent.set_style("display", "flex")
            self.loading_file.set_style("display", "none")

    def upload_callback(self,ctx, id, data, status):
        if status == "done":
            self.loading_file.set_style("display", "none")
            self.dropzone_inside.set_style("display", "none")
            self.dropzone_image.set_style("display", "flex")
            self.dropzone_parent.set_style("display", "flex")
            if self.on_upload_done:
                self.imageID=self.on_upload_done(ctx, data, self.filename)
            
        elif status == "progress":
            self.loading_file.set_style("display", "flex")
        else:
            print("error")
                    
    def create_image_viewer(self, image_url):
        self.dropzone_image = image_viewer(id=self.viewer_id, value=image_url, buttonGroup=buttonGroupConfig["seadragon"]).size("100%", "100%")
        self.dropzone_image.on("button_click", self.resetImage)
        self.dropzone_image.style("display: none ; z-index: 3")

    def create_fabric_viewer(self):
        self.dropzone_image = fabric(id=self.viewer_id)
        self.dropzone_image.style("display: none ; z-index: 8")
        buttonGroupConfig["fabric"]["Delete"]["onClick"] = self.resetImage
        button_group(items=buttonGroupConfig["fabric"], id=self.viewer_id + "-button-group").cls("button-group")

    def resetImage(self,ctx, id, value):
            if self.dropzone_image.value:                
                self.dropzone_inside.set_style("display", "flex")
                self.dropzone_image.set_style("display", "none")
                self.dropzone_image.value = None
                self.file.value = None
            else:
                print("No image to reset")

    def setImage(self, options):
        url = options.get("url", None)
        imageID = options.get("_id", None) or options.get("id", None)
        if url and imageID is not None:
            self.dropzone_inside.set_style("display", "none")
            self.dropzone_image.set_style("display", "flex")
            self.dropzone_image.value = url
            self.imageID = imageID
    
    
        

title = "Input Image"
description = """
## input_image(value=None, id=None, viewer="seadragon",callback=None)

1- Kullanıcıların resim yüklemesini ve görüntülemesini sağlar.

| attr                  | desc                                              |
| :-------------------- | :------------------------------------------------ |
| viewer                | Resim görüntüleyici tipi. Seadragon veya fabric olabilir. |
| callback              | Resim yüklendikten sonra çalıştırılacak fonksiyon. |

"""

sample="""
   def input_image_example():
        with col(id="imagine-input-col").cls("border").style("width","50%") as input_image_test:
            input_image(id="input_image").style("height","500px")
        return input_image_test
    """


        