import uix
from uix.elements import text, col, button, image,row,dialog


uix.html.add_script(
    'dialog-js', f"""<script src="comp_static/scripts/comp_modal.js?v={0.15}"></script>"""
)

uix.html.add_css("dialog.css","""
    .dialog-container{
        width: fit-content;
        height: fit-content;
        align-items: flex-end;
        background-color: var(--background);
        gap: 10px;
        justify-content: flex-start;
        padding: 10px;
        border-radius: 6px;
        min-height:50%;
    }
                  """)

class basic_dialog(uix.Element):
    def __init__(self,
                id=None,
                elements=None,
                close_on_outside = True, 
                **kwargs
                ):
        super().__init__(id=id, **kwargs)
        self.dialogID = id + "-dialog"
        self.buttonID = id + "-button"
        self.close_on_outside = close_on_outside
        self.elements = elements
        #self.modal_content=None
        #with self.cls('modal container hidden').style("z-index","14 !important"):
        with dialog(id=self.dialogID,close_on_outside=close_on_outside) as _dialog:
            self._dialog=_dialog
            with col(id="dialog-column"): #.cls("wrapper modal-container")
                    with (
                        button(id=self.buttonID)
                            .style("background-color","red")
                            .style("min-width","0 !important")
                            .style("width","30px")
                            .style("height","30px")
                            .on("click", _dialog.hide)
                            ):
                        
                        image(
                            value="close_icon.svg"
                        ).style("width", "20px").style("height", "20px").style("color", "white")
                
                    with row(""):
                        if elements is not None:
                            for element in elements:
                                element.bind()
    def render(self):
        self.queue_for_send(
            self.id,
            {
                "id": self.id,

            },
            "init-modal"
        )

        return super().render()

    """   def close(self,id,value):
        self.add_class("hidden")

    def open(self):
        self.remove_class("hidden")
      """