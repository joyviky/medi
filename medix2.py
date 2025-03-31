import requests
import os
import tkinter as tk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch response from Gemini API
def fetch_gemini_response(prompt):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: API key not found. Set GEMINI_API_KEY in the .env file."

    api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200:
            return data.get("candidates", [{}])[0].get("content", "No response generated.")
        else:
            return f"Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"

# Function to send user message
def send_message():
    user_input = entry.get().strip()
    if user_input:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        entry.delete(0, tk.END)

        # Fetch Gemini API response
        response = fetch_gemini_response(user_input)
        chat_display.insert(tk.END, f"Gemini: {response}\n", "bot")
        chat_display.config(state=tk.DISABLED)

# Create GUI application
root = tk.Tk()
root.title("Gemini Chatbot")
root.geometry("500x600")

# Chat Display Area
chat_display = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Scrollbar for chat display
scrollbar = tk.Scrollbar(chat_display)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_display.yview)

# Entry field for user input
entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10, fill=tk.X, padx=10)

# Send Button
send_button = tk.Button(root, text="Send", font=("Arial", 14), command=send_message)
send_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
