import tkinter as tk
from calculator import calculate_total_per_person

class TipCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tip Calculator")
        
        # Set fixed window size
        self.window_width = 450
        self.window_height = 500

        self.centre_window()

        self.bill_amount = tk.StringVar()
        self.custom_amount = tk.StringVar()
        self.custom_people = tk.StringVar()

        self.selected_tip_percentage = None
        self.split_bill_choice = None
        self.selected_people = None
        self.result = tk.StringVar(value="Total per person: £0.00")

        # Used to highlight buttons
        self.tip_buttons = []
        self.split_buttons = []
        self.people_buttons = []

        # Used to un-highlight buttons
        self._suppress_custom_tip_trace = False
        self._suppress_custom_people_trace = False
        self.custom_amount.trace_add("write", self.on_custom_tip_change)
        self.custom_people.trace_add("write", self.on_custom_people_change)

        self.create_widgets()

    def centre_window(self):
        """Centres the window on the user's screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def create_widgets(self):
        tk.Label(self.root, text="Bill Amount (£):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.bill_amount).pack()

        self.create_tip_buttons()
        self.create_split_bill_buttons()
        self.number_of_people_options()

        # Calculate button
        tk.Button(self.root, text="Calculate", command=self.calculate).pack(pady=10)

        # Result label
        tk.Label(self.root, textvariable=self.result, font=("Arial", 14, "bold")).pack(pady=20)

    def create_tip_buttons(self):
        tk.Label(self.root, text="Select Tip:").pack(pady=5)
        tip_frame = tk.Frame(self.root)
        tip_frame.pack()

        self.tip_buttons = []
        for tip in [10, 15, 20]:
            btn = tk.Button(tip_frame, text=f"{tip}%")
            btn.config(command=lambda t=tip, b=btn: self.set_tip(t, b))
            btn.pack(side=tk.LEFT, padx=5)
            self.tip_buttons.append(btn)

        custom_tip_frame = tk.Frame(self.root)
        custom_tip_frame.pack(pady=5)

        tk.Label(custom_tip_frame, text="Custom amount (%):").pack(side=tk.LEFT, padx=5)

        self.custom_tip_entry = tk.Entry(custom_tip_frame, textvariable=self.custom_amount, width=5)
        self.custom_tip_entry.pack(side=tk.LEFT)

        # clear highlights when user focuses the custom tip entry
        self.custom_tip_entry.bind("<FocusIn>", self.on_custom_tip_focus)

    def on_custom_tip_change(self, *args):
        # Un-highlight tip buttons
        for btn in self.tip_buttons:
            btn.config(bg="SystemButtonFace")
        self.selected_tip_percentage = None

        # If split is yes, clear people button highlights too
        if self.split_bill_choice:
            for btn in self.people_buttons:
                btn.config(bg="SystemButtonFace")
            self.selected_people = None
            self.custom_people.set("")

    def create_split_bill_buttons(self):
        tk.Label(self.root, text="Split Bill?").pack(pady=5)
        split_frame = tk.Frame(self.root)
        split_frame.pack()

        split_bill_options = {
            'Yes': True,
            'No': False
        }

        for label, val in split_bill_options.items():
            btn = tk.Button(split_frame, text=label)
            btn.config(command=lambda v=val, b=btn: self.set_split_choice(v, b))
            btn.pack(side=tk.LEFT, padx=5)
            self.split_buttons.append(btn)
    
    def number_of_people_options(self):
        self.people_options_container = tk.Frame(self.root)
        self.people_options_container.pack()

        # label created once; show/hide later (prevents duplicates)
        self.people_label = tk.Label(self.people_options_container, text="Number of People:")
        self.people_label.pack_forget()

        self.people_buttons_frame = tk.Frame(self.people_options_container)
        self.people_buttons_frame.pack_forget()

        self.custom_people_frame = tk.Frame(self.people_options_container)
        self.custom_people_label = tk.Label(self.custom_people_frame, text="Custom Number of People:")
        self.custom_people_entry = tk.Entry(self.custom_people_frame, textvariable=self.custom_people, width=5)

        # pack order inside the frame
        self.custom_people_label.pack(side=tk.LEFT, padx=5)
        self.custom_people_entry.pack(side=tk.LEFT)

        # clear people highlights when focusing the custom people entry
        self.custom_people_entry.bind("<FocusIn>", self.on_custom_people_focus)
    
    def on_custom_people_change(self, *args):
        # Clear people buttons highlight
        for btn in self.people_buttons:
            btn.config(bg="SystemButtonFace")
        self.selected_people = None

    def highlight_button(self, clicked_button, button_list):
        """Highlight clicked button and reset others"""
        for btn in button_list:
            btn.config(bg="SystemButtonFace")
            
        clicked_button.config(bg="lightblue")

    def set_tip(self, tip_percentage, button):
        self.selected_tip_percentage = tip_percentage
        self.highlight_button(button, self.tip_buttons)

        # Prevent on_custom_tip_change from clearing the selection we just made
        self._suppress_custom_tip_trace = True
        try:
            self.custom_amount.set("")   # Clear the custom field safely
        finally:
            self._suppress_custom_tip_trace = False

    def set_split_choice(self, split_yes, button):
        self.split_bill_choice = split_yes
        self.selected_people = None
        self.custom_people.set("")
        self.highlight_button(button, self.split_buttons)

        self.clear_people_options()

        if split_yes:
            self.show_people_options()
        else:
            self.hide_people_options()

    def clear_people_options(self):
        for w in self.people_buttons_frame.winfo_children():
            w.destroy()

        self.people_buttons.clear()

        # fully hide people UI
        self.people_label.pack_forget()
        self.people_buttons_frame.pack_forget()
        self.custom_people_frame.pack_forget()

    def show_people_options(self):
        # pack in the correct vertical order (label above buttons)
        self.people_label.pack(pady=5)
        self.people_buttons_frame.pack()

        self.people_buttons.clear()
        for p in [2, 3, 4]:
            btn = tk.Button(self.people_buttons_frame, text=str(p))
            btn.config(command=lambda n=p, b=btn: self.set_people(n, b))
            btn.pack(side=tk.LEFT, padx=5)
            self.people_buttons.append(btn)

        self.custom_people_frame.pack(pady=5)

    def hide_people_options(self):
        self.people_label.pack_forget()
        self.people_buttons_frame.pack_forget()
        self.custom_people_frame.pack_forget()

    def set_people(self, people, button):
        self.selected_people = people
        self.highlight_button(button, self.people_buttons)

        # Prevent on_custom_people_change from clearing the selection we just made
        self._suppress_custom_people_trace = True
        try:
            self.custom_people.set("")   # Clear the custom field safely
        finally:
            self._suppress_custom_people_trace = False

    def clear_tip_selection(self):
        for btn in self.tip_buttons:
            btn.config(bg="SystemButtonFace")
        self.selected_tip_percentage = None

    def clear_people_selection(self):
        for btn in self.people_buttons:
            btn.config(bg="SystemButtonFace")
        self.selected_people = None

    def on_custom_tip_focus(self, event):
        self.clear_tip_selection()
        if self.split_bill_choice:
            self.clear_people_selection()

    def on_custom_tip_change(self, *args):
        if self._suppress_custom_tip_trace:
            return

        for btn in self.tip_buttons:
            btn.config(bg="SystemButtonFace")
        self.selected_tip_percentage = None

        if self.split_bill_choice:
            for btn in self.people_buttons:
                btn.config(bg="SystemButtonFace")
            self.selected_people = None
            self.custom_people.set("")

    def on_custom_people_focus(self, event):
        self.clear_people_selection()

    def on_custom_people_change(self, *args):
        if self._suppress_custom_people_trace:
            return
        
        # Only loop over still-existing widgets
        alive_buttons = [btn for btn in self.people_buttons if btn.winfo_exists()]

        for btn in alive_buttons:
            btn.config(bg="SystemButtonFace")

        self.selected_people = None

    def calculate(self):
        try:
            bill_amount = float(self.bill_amount.get())
            tip_percentage = self.get_tip_percentage()

            if self.split_bill_choice is None:
                raise ValueError("Please choose whether to split the bill.")
            
            if self.split_bill_choice:
                number_of_people = self.get_number_of_people()
                total_per_person = calculate_total_per_person(bill_amount, tip_percentage, number_of_people)
                self.result.set(f"Total per person: £{total_per_person:.2f}")
            else:
                total_amount = calculate_total_per_person(bill_amount, tip_percentage, 1)
                self.result.set(f"Total: £{total_amount:.2f}")

        except ValueError as e:
            self.result.set(f"Error: {e}")

    def get_tip_percentage(self):
        if self.custom_amount.get():
            return float(self.custom_amount.get())
        elif self.selected_tip_percentage is not None:
            return self.selected_tip_percentage
        else:
            raise ValueError("Please select or enter a tip percentage.")
        
    def get_number_of_people(self):
        if self.custom_people.get():
            return int(self.custom_people.get())
        elif self.selected_people is not None:
            return self.selected_people
        else:
            raise ValueError("Please select or enter number of people.")

        