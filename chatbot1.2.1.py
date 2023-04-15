import datetime
import re
import os
import pyowm
import tkinter as tk
import spacy
from tkinter import messagebox

nlp = spacy.load("en_core_web_sm")

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

def classify_intent(doc):
    for token in doc:
        if token.lower_ in patterns:
            return token.lower_
    return None

responses = {
    'date': datetime.datetime.now().strftime('%A, %B %d, %Y'),
    'time': datetime.datetime.now().strftime('%I:%M %p'),
    'weather': 'Please enter the name of the location for which you want to check the weather.'
}

owm = pyowm.OWM('e75425d9196536d8d9021257adbdecc3')
def get_weather(location):
    try:
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

def respond(message):
    doc = nlp(message)
    intent = classify_intent(doc)

    if intent:
        if intent == 'note':
            return 'note'
        elif intent == 'weather':
            return responses.get(intent)
        else:
            return responses.get(intent)
    return None

def create_note(note_name, content, response_box):
    filename = note_name + '.txt'
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = os.path.join(desktop_path, filename)
    
    with open(filepath, 'w') as file:
        file.write(content)
    
    response_box.insert(tk.END, f'Your note has been saved as {filename} on your desktop!\n\n')


def list_functions():
    messagebox.showinfo("Functions", "I can help you with the following functions:\n"
                        "- Get the current date\n"
                        "- Get the current time\n"
                        "- Create a note\n"
                        "- List all the functions that I provide\n"
                        "- Exit the program")

# Define the main function to run the chat bot
def run_chat_bot():
    root = tk.Tk()
    root.title("Chat Bot")

    response_box = tk.Text(root, width=50, height=10)
    response_box.pack(pady=10)

    input_box = tk.Entry(root, width=50)
    input_box.pack(pady=10)

    waiting_for_location = False
    waiting_for_note_name = False
    waiting_for_note_content = False
    note_name = None

    def submit_message(event=None):
        nonlocal waiting_for_location, waiting_for_note_name, waiting_for_note_content, note_name

        message = input_box.get()

        if waiting_for_location:
            location = message
            response = get_weather(location)
            response_box.insert(tk.END, f'{response}\n\n')
            waiting_for_location = False
        elif waiting_for_note_name:
            note_name = message
            response_box.insert(tk.END, 'Please enter the content of your note:\n\n')
            waiting_for_note_name = False
            waiting_for_note_content = True
        elif waiting_for_note_content:
             content = message
             create_note(note_name, content, response_box)
             waiting_for_note_content = False
        else:
            response = respond(message)
            if response == responses['weather']:
                response_box.insert(tk.END, f'{response}\n\n')
                waiting_for_location = True
            elif response == 'note':
                response_box.insert(tk.END, 'Please enter the name of your note:\n\n')
                waiting_for_note_name = True
            else:
                response_box.insert(tk.END, f'{response}\n\n')
        input_box.delete(0, tk.END)
        response_box.see(tk.END)

    input_box.bind("<Return>", submit_message)
    root.mainloop()


# Run the chat bot
run_chat_bot()
