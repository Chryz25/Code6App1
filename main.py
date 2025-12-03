from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import math

Window.clearcolor = (0.05, 0.05, 0.08, 1)


class CalculatorButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.15, 0.15, 0.2, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(20)
        self.bold = True
        
        with self.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class OperatorButton(CalculatorButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.4, 0.8, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.color = (1, 1, 1, 1)


class SpecialButton(CalculatorButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.25, 0.25, 0.3, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])


class EqualsButton(CalculatorButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.7, 0.4, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])


class AdvancedCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        self.current_number = ""
        self.previous_number = ""
        self.operation = ""
        self.result = 0
        self.new_calculation = False
        self.history = []
        
        # Display area
        display_box = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=dp(5))
        
        # History label
        self.history_label = Label(
            text="",
            font_size=dp(16),
            halign='right',
            valign='middle',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.3
        )
        self.history_label.bind(size=self.history_label.setter('text_size'))
        
        # Main display
        self.display = Label(
            text="0",
            font_size=dp(48),
            halign='right',
            valign='middle',
            bold=True,
            size_hint_y=0.7
        )
        self.display.bind(size=self.display.setter('text_size'))
        
        display_box.add_widget(self.history_label)
        display_box.add_widget(self.display)
        self.add_widget(display_box)
        
        # Button layout
        button_layout = GridLayout(cols=4, spacing=dp(8), size_hint_y=0.75)
        
        # Scientific functions row
        buttons_sci = [
            ('sin', SpecialButton), ('cos', SpecialButton), 
            ('tan', SpecialButton), ('log', SpecialButton)
        ]
        
        for btn_text, btn_class in buttons_sci:
            btn = btn_class(text=btn_text)
            btn.bind(on_press=self.on_button_press)
            button_layout.add_widget(btn)
        
        # Advanced functions row
        buttons_adv = [
            ('√', SpecialButton), ('x²', SpecialButton),
            ('xʸ', OperatorButton), ('1/x', SpecialButton)
        ]
        
        for btn_text, btn_class in buttons_adv:
            btn = btn_class(text=btn_text)
            btn.bind(on_press=self.on_button_press)
            button_layout.add_widget(btn)
        
        # Number and operation buttons
        buttons = [
            [('C', SpecialButton), ('⌫', SpecialButton), ('%', OperatorButton), ('÷', OperatorButton)],
            [('7', CalculatorButton), ('8', CalculatorButton), ('9', CalculatorButton), ('×', OperatorButton)],
            [('4', CalculatorButton), ('5', CalculatorButton), ('6', CalculatorButton), ('-', OperatorButton)],
            [('1', CalculatorButton), ('2', CalculatorButton), ('3', CalculatorButton), ('+', OperatorButton)],
            [('±', SpecialButton), ('0', CalculatorButton), ('.', CalculatorButton), ('=', EqualsButton)]
        ]
        
        for row in buttons:
            for btn_text, btn_class in row:
                btn = btn_class(text=btn_text)
                btn.bind(on_press=self.on_button_press)
                button_layout.add_widget(btn)
        
        self.add_widget(button_layout)
    
    def on_button_press(self, instance):
        button_text = instance.text
        
        if button_text in '0123456789':
            if self.new_calculation:
                self.current_number = ""
                self.new_calculation = False
            self.current_number += button_text
            self.update_display()
        
        elif button_text == '.':
            if '.' not in self.current_number:
                if self.current_number == "":
                    self.current_number = "0"
                self.current_number += '.'
                self.update_display()
        
        elif button_text == 'C':
            self.clear()
        
        elif button_text == '⌫':
            self.backspace()
        
        elif button_text == '±':
            self.toggle_sign()
        
        elif button_text in ['+', '-', '×', '÷', '%', 'xʸ']:
            self.set_operation(button_text)
        
        elif button_text == '=':
            self.calculate()
        
        elif button_text in ['sin', 'cos', 'tan', 'log', '√', 'x²', '1/x']:
            self.scientific_operation(button_text)
    
    def update_display(self):
        if self.current_number == "":
            self.display.text = "0"
        else:
            self.display.text = self.current_number
    
    def clear(self):
        self.current_number = ""
        self.previous_number = ""
        self.operation = ""
        self.result = 0
        self.history_label.text = ""
        self.update_display()
    
    def backspace(self):
        if self.current_number:
            self.current_number = self.current_number[:-1]
            self.update_display()
    
    def toggle_sign(self):
        if self.current_number and self.current_number != "0":
            if self.current_number[0] == '-':
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.update_display()
    
    def set_operation(self, op):
        if self.current_number:
            if self.previous_number and not self.new_calculation:
                self.calculate()
            else:
                self.previous_number = self.current_number
                self.current_number = ""
            self.operation = op
            self.history_label.text = f"{self.previous_number} {op}"
            self.new_calculation = False
    
    def calculate(self):
        if not self.previous_number or not self.current_number:
            return
        
        try:
            num1 = float(self.previous_number)
            num2 = float(self.current_number)
            
            if self.operation == '+':
                self.result = num1 + num2
            elif self.operation == '-':
                self.result = num1 - num2
            elif self.operation == '×':
                self.result = num1 * num2
            elif self.operation == '÷':
                if num2 != 0:
                    self.result = num1 / num2
                else:
                    self.display.text = "Error"
                    self.clear()
                    return
            elif self.operation == '%':
                self.result = num1 % num2
            elif self.operation == 'xʸ':
                self.result = num1 ** num2
            
            self.history_label.text = f"{self.previous_number} {self.operation} {self.current_number} ="
            self.current_number = str(self.result)
            self.previous_number = ""
            self.operation = ""
            self.new_calculation = True
            self.update_display()
        
        except Exception as e:
            self.display.text = "Error"
            self.clear()
    
    def scientific_operation(self, func):
        if not self.current_number or self.current_number == "0":
            return
        
        try:
            num = float(self.current_number)
            
            if func == 'sin':
                self.result = math.sin(math.radians(num))
            elif func == 'cos':
                self.result = math.cos(math.radians(num))
            elif func == 'tan':
                self.result = math.tan(math.radians(num))
            elif func == 'log':
                if num > 0:
                    self.result = math.log10(num)
                else:
                    self.display.text = "Error"
                    return
            elif func == '√':
                if num >= 0:
                    self.result = math.sqrt(num)
                else:
                    self.display.text = "Error"
                    return
            elif func == 'x²':
                self.result = num ** 2
            elif func == '1/x':
                if num != 0:
                    self.result = 1 / num
                else:
                    self.display.text = "Error"
                    return
            
            self.history_label.text = f"{func}({self.current_number}) ="
            self.current_number = str(self.result)
            self.new_calculation = True
            self.update_display()
        
        except Exception as e:
            self.display.text = "Error"


class CalculatorApp(App):
    def build(self):
        self.title = 'Advanced Calculator'
        return AdvancedCalculator()


if __name__ == '__main__':
    CalculatorApp().run()
