import os
from io import open
from uix import T, app, html, Element
from uix.elements import row, button, div

base_path = os.path.dirname(__file__)
public_path = os.path.join(base_path, "public")

def add_resources(resource_type, resources):
    for resource_id, filename in resources.items():
        full_path = os.path.join(public_path, filename)
        if resource_type == 'css':
            html.add_css_file(filename, full_path)
        elif resource_type == 'js':
            html.add_script_source(id=resource_id, script=filename, beforeMain=False, localpath=full_path)

add_resources('css', {'_credit_card': '_credit_card.css'})
add_resources('js', {
    'credit_card': 'imask.min.js',
    'credit_card_ui': '_credit_card.js',
    'add_card_js': '_add_card.js'
})

app.add_static_route("credit_card", public_path)

with open(os.path.join(public_path, "_credit_card.html"), mode="r", encoding="utf-8") as f:
    html_content = f.read()

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