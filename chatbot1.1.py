import datetime
import re
import os
import pyowm
import tkinter as tk
from tkinter import messagebox

# Define the patterns to recognize user input
patterns = {
    'date': r'\b(date|day)\b',
    'time': r'\b(time|clock)\b',
    'note': r'\b(note|remember)\b',
    'help': r'\b(help|list)\b',
    'exit': r'\b(exit|bye|goodbye)\b',
    'functions': r'\b(what can you do\?|what are your functions\?)\b',
    'weather': r'\b(weather)\b'
}

responses = {
    'date': datetime.datetime.now().strftime('%A, %B %d, %Y'),
    'time': datetime.datetime.now().strftime('%I:%M %p'),
    'weather': 'Please enter the name of the location for which you want to check the weather.'
}

owm = pyowm.OWM('e75425d9196536d8d9021257adbdecc3')
def get_weather():
    try:
        # Get location from user input
        location = input('What is your location? ')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(location)
        w = observation.weather
        # Get weather information
        temperature = w.temperature('celsius')['temp']
        status = w.detailed_status
        humidity = w.humidity
        # Return the weather information
        return f'The temperature in {location} is {temperature:.1f}°C and {status.lower()}. Humidity is {humidity}%.'
    except Exception as e:
        print(f"Sorry, I couldn't get the weather information. {e}")


# Define a function to recognize and respond to user input
def respond(message):
    for pattern, regex in patterns.items():
        if re.search(regex, message, re.IGNORECASE):
            if pattern == 'weather':
                location = re.findall(r'[\w\s]+', message)[0]
                return get_weather()
            else:
                return responses.get(pattern)
    return None


# Define a function to create a note and save it as a text file on the desktop
def create_note():
    filename = input('What would you like to name your note? ') + '.txt'
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = os.path.join(desktop_path, filename)
    content = input('What would you like to write in your note? ')
    with open(filepath, 'w') as file:
        file.write(content)
    print(f'Your note has been saved as {filename} on your desktop!')

# Define a function to list all the functions that the chat bot provides
def list_functions():
    messagebox.showinfo("Functions", "I can help you with the following functions:\n"
                        "- Get the current date\n"
                        "- Get the current time\n"
                        "- Create a note\n"
                        "- List all the functions that I provide\n"
                        "- Exit the program")

# Define the main function to run the chat bot
def run_chat_bot():
    # Create the main window
    root = tk.Tk()
    root.title("Chat Bot")

    # Define the response box
    response_box = tk.Text(root, width=50, height=10)
    response_box.pack(pady=10)

    # Define the input box
    input_box = tk.Entry(root, width=50)
    input_box.pack(pady=10)

    # Define the submit button
    def submit_message(event=None):
        message = input_box.get()
        response = respond(message)
        if response:
            response_box.insert(tk.END, f'{response}\n\n')
        elif re.search(patterns['note'], message, re.IGNORECASE):
            create_note()
        elif re.search(patterns['help'], message, re.IGNORECASE):
            list_functions()
        elif re.search(patterns['exit'], message, re.IGNORECASE):
            response_box.insert(tk.END, 'Goodbye!\n\n')
            root.destroy()
        elif re.search(patterns['functions'], message, re.IGNORECASE):
            list_functions()
        else:
            response_box.insert(tk.END, "I'm sorry, I didn't understand your request.\n\n")
        input_box.delete(0, tk.END)

    input_box.bind("<Return>", submit_message)

    # Start the main event loop
    root.mainloop()

# Run the chat bot
run_chat_bot()
