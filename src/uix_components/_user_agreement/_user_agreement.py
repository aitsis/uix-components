from uix import Element, app
from uix.elements import row, col, button

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_script("_user_agreement.css", "/_user_agreement/_user_agreement.css", is_url=True)
    cls.register_script("useragreement-js", "/_user_agreement/_user_agreement.js", is_url=True)
    return cls

@register_resources
class user_agreement(Element):
    def __init__(self,
                id=None,
                user_agreement=None,
                func_name=None,
                **kwargs
                ):
        super().__init__(id=id)
        self.id=id
        self.accept=False
        self.func_name=func_name
        self.user_agreement=user_agreement
        with self as content:
            self.content=content
            with col("").cls("userAgreement"):
                self.contract=row("",id="contract")
                with row("").cls("term-buttons-container"):
                    self.accept_btn=button(value="Kabul Et",id=id+"-accept-btn").cls("accept-button hidden")

    def init(self):
        self.session.queue_for_send(
            self.id,
            {
                "id": self.id,
                "contract": self.contract.id,
                "contract_content": self.user_agreement,
                "accept_btn": self.accept_btn.id,
                "accept": self.accept,
                "func_name": self.func_name
            },
        "init-contract"),
        return super().render()
