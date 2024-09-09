import uix
from uix.elements import div
from uix import T
from uix_components import image_viewer, button_group,fabric
from ._output_loading import output_loading
from uix.core.session import context


buttonGroupConfig = {
            "seadragon": {
                "Zoom in": {"id": "zoom-in",
                            "icon": "fa-solid fa-search-plus", 
                            "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Zoom out": {
                            "id": "zoom-out",
                            "icon": "fa-solid fa-search-minus", 
                            "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Home ": {
                            "id": "home",
                            "icon": "fa-solid fa-home", 
                            "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Full screen": {
                                "id": "full-screen",
                                "icon": "fa-solid fa-expand", 
                                "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Download": {   
                                "id": "download",
                                "icon": "fa-solid fa-download", 
                                "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Save": {
                            "id": "save",
                            "icon": "fa-solid fa-floppy-disk", 
                            "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
                "Send to input": {  
                                    "btn_id": "send-to-input",  
                                    "icon": "fa-solid fa-arrow-left", 
                                    "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
            },
            "fabric": {
                "Download": {"icon": "fa-solid fa-download", "icon_styles": {"font-size": "20px", "color": "var(--ait)"},"link":"my_images/AIT_AI_LOGO.png", "download":True},
                "Save": {"icon": "fa-solid fa-floppy-disk", 
                         "icon_styles": {"font-size": "20px", "color": "var(--ait)"}},
            }
        }
class output_image(uix.Element):
    def __init__(
            self,
            value=None,
            id=None,
            viewer="seadragon",
            setinputImage=None,
            add_to_favorite=None
    ):
        super().__init__(value=value, id=id)
        self.id = id
        self.viewer_id = id + "-viewer"
        self.file_id = id + "-file"
        self.label_id = id + "-label"
        self.loading_file_id = id + "-loading-file"
        self.loading_id = id + "-loading"
        self.setinputImage= setinputImage
        self.add_to_favorite = add_to_favorite
        self.viewer=viewer
        self.cls("wall hall")
        self.style("position", "relative")


        with self:
            if self.viewer == "seadragon":
                self.create_image_viewer("my_images/AIT_AI_LOGO.png")
            else:
                with div().cls("wall hall").style("position", "absolute").style("top", "0").style("left", "0"):
                    self.create_fabric_viewer("my_images/AIT_AI_LOGO.png")
            self.output_loading = output_loading(id=self.loading_id).cls("wall hall hidden")

    def create_image_viewer(self, image_url):
        
        buttonGroupConfig["seadragon"]["Zoom in"]["onClick"] = lambda ctx, id, value, key="Zoom in": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Zoom out"]["onClick"] = lambda ctx, id, value, key="Zoom out": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Home "]["onClick"] = lambda ctx, id, value, key="Home": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Full screen"]["onClick"] = lambda ctx, id, value, key="Full screen": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Download"]["onClick"] = lambda ctx, id, value, key="Download": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Send to input"]["onClick"] = lambda ctx, id, value, key="Send to input": self.on_click(ctx, id, key)
        buttonGroupConfig["seadragon"]["Save"]["onClick"] = lambda ctx, id, value, key="Save": self.on_click(ctx, id, key)

        button_group(items=buttonGroupConfig["seadragon"], id=self.viewer_id + "-button-group")
        self.image_viewer = image_viewer(id=self.viewer_id, value=image_url,button_groupId = self.viewer_id+"-button-group").size("100%", "100%").cls("opacity-30")

    def create_fabric_viewer(self, image_url):
        self.image_viewer = fabric(id=self.viewer_id, value=image_url).size("100%", "100%").cls("opacity-30")
        buttonGroupConfig["fabric"]["Save"]["onClick"] = self.addToFavorite
        self.buttonGroup=button_group(items=buttonGroupConfig["fabric"], id=self.viewer_id + "-button-group").cls("button-group")

    def set_image(self,ctx, id=None, value=None):
        url = value
        if isinstance(value, dict):
            url = value.get("url")

        imageID = id
        if url or imageID is not None:
            self.output_loading.add_class("hidden")
            self.image_viewer.remove_class("hidden")
            self.value = imageID
            self.image_viewer.value = url
            self.image_viewer.remove_class("opacity-30")
            if self.viewer == "fabric":
                self.output_loading.add_class("hidden")
                self.image_viewer.remove_class("hidden")
                self.buttonGroup.link.attrs["href"]=self.image_viewer.value
                name=self.image_viewer.value.split("/")[-1]
                self.buttonGroup.link.attrs["download"]=name
                self.buttonGroup.update()

        elif imageID is None:
            self.image_viewer.add_class("opacity-30")
            self.image_viewer.value = "my_images/AIT_AI_LOGO.png"

        else:
            self.image_viewer.value = url


    def loading(self, is_loading=True):
        if is_loading:
            self.image_viewer.add_class("hidden")
            self.output_loading.remove_class("hidden")
        else:
            self.output_loading.add_class("hidden")
            self.image_viewer.remove_class("hidden")

    def sendToInput(self,ctx,id,value):
        if value == None and "comp_alert" in ctx.elements:
            ctx.elements["comp_alert"].open("alert-danger",(T("Something went wrong")))
        dataToSend = {
            "id": self.value,
            "url": self.image_viewer.value
        }

        if self.setinputImage is not None:
            self.setinputImage(dataToSend)
        else:
            pass

    def addToFavorite(self,ctx,id,value):
        if self.add_to_favorite is not None:
            self.add_to_favorite(ctx, id, self.value)

    def on_click(self, ctx, id, value):
        if value == "Zoom in":
            self.image_viewer.zoom_in()
        elif value == "Zoom out":
            self.image_viewer.zoom_out()
        elif value == "Home":
            self.image_viewer.home()
        elif value == "Full screen":
            print("Full screen")
            self.image_viewer.fullscreen()
        elif value == "Download":
            self.addToFavorite(ctx, "download", value)
            self.image_viewer.download()
        elif value == "Send to input":
            self.sendToInput(ctx, id, self.value)
        elif value == "Save":
            self.addToFavorite(ctx, id, value)
