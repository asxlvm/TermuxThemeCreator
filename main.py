from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.colorpicker import ColorPicker
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from PIL import ImageColor
from dataclasses import dataclass

COLOR_DEFAULTS = {
    "Foreground": "#c0caf5",
    "Background": "#1a1b26",
    "Cursor": "#eaeeff",
    "FILL_IN": None,
    "0":  "#15161e",
    "8":  "#414868",
    "1":  "#b85164",
    "9":  "#f7768e",
    "2":  "#8eb75e",
    "10": "#9ece6a",
    "3":  "#bd9458",
    "11": "#e0af68",
    "4":  "#5875b3",
    "12": "#7aa2f7",
    "5":  "#7e68a7",
    "13": "#bb9af7",
    "6":  "#5288a7",
    "14": "#7dcfff",
    "7":  "#737891",
    "15": "#c0caf5",
}

@dataclass
class ColorButton:
    id: str
    button_obj: Label
    colorpicker_obj: ColorPicker
    current_color: str

def convert_colors(hex_string):
    rgb = ImageColor.getcolor(hex_string, "RGB")
    final = []
    for c in rgb:
        final.append(c/255)
    return final

class MainApp(MDApp):
    def colorchange(self, instance, *args):
        color = self.buttons[instance.id].colorpicker_obj.hex_color
        self.buttons[instance.id].current_color = color
        self.buttons[instance.id].button_obj.background_color = convert_colors(color)

    def export(self, *args):
        clr_list = [self.buttons[btn].current_color for btn in self.buttons]
        export_str = f"""foreground={clr_list[0]}
background={clr_list[1]}
cursor={clr_list[2]}

color0={clr_list[3]}
color8={clr_list[4]}
color1={clr_list[5]}
color9={clr_list[6]}
color2={clr_list[7]}
color10={clr_list[8]}
color3={clr_list[9]}
color11={clr_list[10]}
color4={clr_list[11]}
color12={clr_list[12]}
color5={clr_list[13]}
color13={clr_list[14]}
color6={clr_list[15]}
color14={clr_list[16]}
color7={clr_list[17]}
color15={clr_list[18]}"""

        popup_content = TextInput(text=export_str)
        self.export_popup = Popup(title="Export Output", content = popup_content, size_hint = (.9, .9))
        self.export_popup.open()

    def close_btn(self, *args):
        if self.opened:
            self.opened = False
            self.btn_window.remove_widget(self.buttons[self.active_colpicker].colorpicker_obj)
            self.toolbar.right_action_items = [["download", self.export, "Export your theme"]]


    def remove_button(self, instance, *args):
        _id = instance.text if instance.text != "Close" else 0

        if self.opened:
            self.opened = False
            self.btn_window.remove_widget(self.buttons[self.active_colpicker].colorpicker_obj)
            self.toolbar.right_action_items = [["download", self.export, "Export your theme"]]
        else:
            self.opened = True
            self.active_colpicker = _id
            self.toolbar.right_action_items = [["download", self.export, "Export your theme"], ["close-box", self.close_btn, "Close the selected colorpicker"]]
            self.btn_window.add_widget(self.buttons[_id].colorpicker_obj)
            self.buttons[_id].colorpicker_obj.set_color(
                convert_colors(
                    self.buttons[_id].current_color
            ))
            self.buttons[_id].colorpicker_obj.bind(color=self.colorchange)

    def build(self):
        self.opened = False
        self.active_colpicker = 0
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "900"

        self.main_window = MDBoxLayout(spacing=5, orientation="vertical")
        self.col_window = MDGridLayout(cols=2, rows=10, spacing=5)
        self.btn_window = MDGridLayout(cols=1, rows=2, size_hint = (1,0.7))
        self.export_popup = None
        self.buttons = {}

        for i, v in COLOR_DEFAULTS.items():
            if v != None:
                self.buttons[i] = ColorButton(
                    i, 
                    Button(
                        #text=str(i), background_color = convert_colors(v)
                    ), 
                    ColorPicker(),
                    v
                )
                self.buttons[i].button_obj.text = str(i)
                self.buttons[i].button_obj.background_color = convert_colors(v)
                self.buttons[i].button_obj.background_down = ""
                self.buttons[i].button_obj.background_normal = ""
                self.buttons[i].button_obj.bind(on_press=self.remove_button)
                self.col_window.add_widget(self.buttons[i].button_obj)

                self.btn_window.add_widget(self.buttons[i].colorpicker_obj)
                self.buttons[i].colorpicker_obj.set_color(
                    convert_colors(
                        self.buttons[i].current_color
                ))
                self.btn_window.remove_widget(self.buttons[i].colorpicker_obj)
                self.buttons[i].colorpicker_obj.id = str(i)
            else:
                self.col_window.add_widget(MDLabel())


        self.main_window.add_widget(self.col_window)
        self.main_window.add_widget(self.btn_window)
        self.toolbar = MDToolbar()
        self.toolbar.title = "Termux Theme Creator"
        self.toolbar.right_action_items = [["download", self.export, "Export your theme"]]
        self.main_window.add_widget(self.toolbar)
        

        return self.main_window
    
MainApp().run()