import uix

from uix.elements import grid, col, button

from components import basic_slider, component_list, basic_checkbox, basic_select, basic_dialog

def basic_slider_example():
    return basic_slider(name="Deneme", id = "mySlider", callback = lambda ctx, id, value: print(f"Slider {id} changed to: {value}"))

def comp1():
    def callback(ctx, id, value):
        print(f"Slider {id} changed to: {value}")
    basic_slider(name="Deneme1", id = "mySlider1", callback = callback)

def comp2():
    def callback(ctx, id, value):
        print(f"Slider {id} changed to: {value}")
    basic_slider(name="Deneme2", id = "mySlider2",callback=callback)

def component_list_example():
    return component_list(id = "comp_main", components = [comp1,comp2])

def basic_checkbox_example():
    return basic_checkbox(id = "myCheckbox",label_text="Label")

options_dict = {
    "Option 1": {"id":"1","isSelect":False, "value":"Option 1"},
    "Option 2": {"id":"1","isSelect":True, "value":"Option 2"},
    "Option 3": {"id":"1","isSelect":False, "value":"Option 3"},
}

options = [
    {"id":"1","isSelect":False, "value":"Option 1"},
    {"id":"2","isSelect":False, "value":"Option 2"},
    {"id":"3","isSelect":True, "value":"Option 3"},
]

def basic_select_example():
    return basic_select(id = "mySelect",options = options)

def basic_dialog_example():
    return basic_dialog(id = "myDialog",elements=[basic_checkbox], close_on_outside = True)

examples = {"Slider Example": basic_slider_example,
            "Component List Example": component_list_example,
            "Checkbox Example": basic_checkbox_example,
            "Select Example": basic_select_example,
            "Dialog Example": basic_dialog_example}


def on_change_example(ctx, id, value):
    print("Example =", value)
    content = ctx.elements["content"]
    if value in examples:
        content.update(examples[value])
    


with grid("",columns = "1fr 5fr") as main:
    with col() as menu:
        menu.cls("border")
        button("Slider Example", id = "slider_example").on("click", on_change_example)
        button("Component List Example", id = "comp_list_example").on("click", on_change_example)
        button("Checkbox Example", id = "checkbox_example").on("click", on_change_example)
        button("Select Example", id = "select_example").on("click", on_change_example)
        button("Dialog Example", id = "dialog_example").on("click", on_change_example)
    with col(id = "content") as content:
        content.cls("container border")
        basic_slider_example()



uix.start(ui=main, config={"debug": True})