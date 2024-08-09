import os
from io import open
from uix import T, app, html, Element
from uix.elements import row, button, div

base_path = os.path.dirname(__file__)
public_path = os.path.join(base_path, "_public")
with open(os.path.join(public_path, "_credit_card.html"), mode="r", encoding="utf-8") as f:
    html_content = f.read()

app.serve_module_static_files(__file__)

def register_resources(cls):
    cls.register_style("_credit_card_css", "/_credit_card/_credit_card.css", is_url=True)

    cls.register_script("imask.min.js", "/_credit_card/imask.min.js", is_url=True)
    cls.register_script("credit_card_ui", "/_credit_card/_credit_card.js", is_url=True)
    cls.register_script("add_card_js", "/_credit_card/_add_card.js", is_url=True)
    return cls

@register_resources
class credit_card(Element):
    def __init__(self, value, id=None, callback=None):
        super().__init__(value, id=id)
        self.callback = callback
        self.size("100%", "100%")

        with self:
            with row("", id="credit-cards").cls("credit-card-row") as self.creditcard:
                with div(id="add_card_div").cls("field-container") as self.add_card_div:
                    button(T("Add Card"), id="payment-button", type="submit")\
                        .cls("payment-button")\
                        .on("add_card", self.callback)

    def init(self):
        self.session.queue_for_send(self.id, {
            'creditcard': self.creditcard.id,
            'html_content': html_content,
            'add_card_div': self.add_card_div.id
        }, "init-credit-card")
