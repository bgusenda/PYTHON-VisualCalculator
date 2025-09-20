# base: https://www.youtube.com/watch?v=28tj-IBfGH4

import tkinter

# Button layout
button_values = [
    ["AC", "+/-", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "√", "="]
]

# Operators and function buttons
right_symbols = ["÷", "×", "-", "+", "="]
top_symbols = ["AC", "+/-", "%", "√"]

# Get layout dimensions from button_values
row_count = len(button_values)  # 5 rows
column_count = len(button_values[0])  # 4 columns

start_new_number = False

# Color variables 
color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"

# Window setup
window = tkinter.Tk()  # Create the window
window.title("Simple Visual Calculator")  # Set window title
window.resizable(False, False)  # Disable window resizing

# Create frame for layout
frame = tkinter.Frame(window)
# Display label
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black, 
                     foreground=color_white, anchor="e", width=column_count)

# Place label using grid
label.grid(row=0, column=0, columnspan=column_count, sticky="we")

# Create and place buttons
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
                                width=column_count-1, height=1)
        
        # Set button colors based on type
        if value in top_symbols:
            button.config(foreground=color_black, background=color_light_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)
            
        button.grid(row=row+1, column=column)

frame.pack()

# Calculator state variables
current_value = "0"  # Current value on display
stored_value = None  # Value stored for operation
current_operator = None  # Current operator (+, -, ×, ÷)
should_reset_display = False  # Flag to reset display on next input

# Remove trailing .0 from whole numbers
def remove_zero_decimal(num):
    if isinstance(num, str):
        try:
            num = float(num)
        except ValueError:
            return num
    
    if isinstance(num, float) and num.is_integer():
        return str(int(num))
    return str(num)

# Clear calculator state
def clear_all():
    global current_value, stored_value, current_operator, should_reset_display
    current_value = "0"
    stored_value = None
    current_operator = None
    should_reset_display = False
    label.config(text=current_value)

# Handle button clicks
def button_clicked(value):
    global current_value, stored_value, current_operator, should_reset_display
    
    # Handle digit input
    if value in "0123456789":
        if current_value == "0" or should_reset_display:
            current_value = value
            should_reset_display = False
        else:
            current_value += value
        label.config(text=current_value)
    
    # Handle decimal point
    elif value == ".":
        if should_reset_display:
            current_value = "0."
            should_reset_display = False
        elif "." not in current_value:
            current_value += "."
        label.config(text=current_value)
    
    # Handle operators (+, -, ×, ÷)
    elif value in "+-×÷":
        if stored_value is None:
            stored_value = current_value
        elif current_operator and not should_reset_display:
            # Calculate previous operation if needed
            calculate_result()
        
        current_operator = value
        should_reset_display = True
    
    # Handle equals button
    elif value == "=":
        if stored_value is not None and current_operator is not None:
            calculate_result()
            stored_value = None
            current_operator = None
    
    # Handle special functions
    elif value == "AC":  # All Clear
        clear_all()
    
    elif value == "+/-":  # Toggle positive/negative
        if current_value != "0":
            if current_value[0] == '-':
                current_value = current_value[1:]
            else:
                current_value = '-' + current_value
        label.config(text=current_value)
    
    elif value == "%":  # Percentage
        try:
            current_value = str(float(current_value) / 100)
            label.config(text=remove_zero_decimal(current_value))
        except ValueError:
            current_value = "0"
            label.config(text="Error")
    
    elif value == "√":  # Square root
        try:
            num = float(current_value)
            if num >= 0:
                current_value = str(num ** 0.5)
                label.config(text=remove_zero_decimal(current_value))
            else:
                label.config(text="Error")
                current_value = "0"
        except ValueError:
            label.config(text="Error")
            current_value = "0"
        should_reset_display = True

# Calculate result of current operation
def calculate_result():
    global current_value, stored_value, should_reset_display
    
    if stored_value is None or current_operator is None:
        return
    
    try:
        num1 = float(stored_value)
        num2 = float(current_value)
        
        if current_operator == "+":
            result = num1 + num2
        elif current_operator == "-":
            result = num1 - num2
        elif current_operator == "×":
            result = num1 * num2
        elif current_operator == "÷":
            if num2 == 0:
                label.config(text="Error")
                clear_all()
                return
            result = num1 / num2
        
        current_value = remove_zero_decimal(result)
        label.config(text=current_value)
        stored_value = current_value
        should_reset_display = True
        
    except ValueError:
        label.config(text="Error")
        clear_all()

# Set up button commands
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        # Get the button at this position
        children = frame.grid_slaves(row=row+1, column=column)
        if children:
            button = children[0]
            # Set the command with the correct value
            button.config(command=lambda v=value: button_clicked(v))

# Center the window on screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Start the application
window.mainloop()