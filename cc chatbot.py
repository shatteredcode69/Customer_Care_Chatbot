import json
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load FAQ data from JSON file
def load_faq_data():
    try:
        with open("faq_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict) and "faqs" in data:
                return data["faqs"]
            else:
                print("Error: JSON format is incorrect.")
                return []
    except FileNotFoundError:
        print("Error: faq_data.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: JSON file is corrupted.")
        return []

# Find the exact response for the user's query
def get_response(user_input):
    user_input = user_input.strip()
    for faq in faq_data:
        if faq["question"].strip() == user_input:
            return faq["answer"]
    return "Sorry, I don't understand. Please contact support."

# Function to display bot response with typing effect
def type_response(response, index=0):
    if index < len(response):
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, response[index], "bot")
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)  # Auto-scroll
        root.after(30, type_response, response, index + 1)  # Adjust speed
    elif index == len(response):
        # Done typing, now speak
        speak_threaded(response)
        # Add a newline after the response is complete
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "\n\n", "bot")
        chat_area.config(state=tk.DISABLED)

# Function to handle user input and display response
def send_message(event=None):
    user_text = user_input_entry.get()
    if user_text.strip():
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "You: " + user_text + "\n", "user")
        chat_area.config(state=tk.DISABLED)
        chat_area.see(tk.END)
        user_input_entry.delete(0, tk.END)

        response = get_response(user_text)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Bot: ", "bot")
        chat_area.config(state=tk.DISABLED)

        # Start typing effect - speech will occur after typing is complete
        root.after(1000, type_response, response)

# Function to make the bot speak without blocking
def speak_threaded(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    
    # Create and start speech thread
    speech_thread = threading.Thread(target=run_speech)
    speech_thread.daemon = True  # Allow program to exit even if thread is running
    speech_thread.start()

# Load FAQ data
faq_data = load_faq_data()
print(f"Total FAQs Loaded: {len(faq_data)}")

# Create GUI using Tkinter
root = tk.Tk()
root.title("Customer Care Chatbot")
root.geometry("500x500")
root.configure(bg="black")

# Chat display area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20, bg="black", fg="white")
chat_area.pack(pady=10, padx=10)
chat_area.tag_config("user", foreground="white")
chat_area.tag_config("bot", foreground="yellow")

# Display the default message at the start
chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, "Bot: Hi! How can we help you today?\n\n", "bot")
chat_area.config(state=tk.DISABLED)

# User input field
user_input_entry = tk.Entry(root, width=50)
user_input_entry.pack(pady=5)
user_input_entry.bind("<Return>", send_message)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

# Speak the welcome message after the GUI is fully loaded
root.after(1000, lambda: speak_threaded("Hi! How can we help you today?"))

# Start GUI loop
root.mainloop()