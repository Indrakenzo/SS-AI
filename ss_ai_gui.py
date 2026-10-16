import os
import requests
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

system_prompt = {
    "role": "system",
    "content": "Anda adalah SS-AI, Asisten Penetration Testing yang dikembangkan oleh Indrayaza Z. "
               "Patuhi Rules of Engagement (RoE): Edukasi defensif, ingatkan otorisasi, tolak ilegalitas."
}

messages = [system_prompt]

def send_message(event=None):
    user_text = entry_field.get().strip()
    if not user_text:
        return
    
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"User: {user_text}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    
    entry_field.delete(0, tk.END)
    messages.append({"role": "user", "content": user_text})
    
    # Menjalankan request di thread terpisah agar GUI tidak freeze (lag)
    threading.Thread(target=fetch_ai_response).start()

def fetch_ai_response():
    if not API_KEY:
        display_message("Error: OPENROUTER_API_KEY tidak ditemukan di file .env")
        return

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/indrayaza/SS-AI",
        "X-Title": "SS-AI Pentest Assistant"
    }
    
    payload = {
        "model": "google/gemini-2.5-flash-free",
        "messages": messages
    }
    
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        
        if response.status_code == 200:
            ai_reply = response_data['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": ai_reply})
            display_message(f"SS-AI: {ai_reply}")
        else:
            display_message(f"API Error: Gagal mendapatkan respons dari server.")
    except Exception as e:
        display_message(f"Error: {str(e)}")

def display_message(msg):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, msg + "\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

# Setup GUI
root = tk.Tk()
root.title("SS-AI Ethical Pentest Assistant - Coded by Indrayaza Z")
root.geometry("700x500")
root.configure(bg="#1e1e1e")

# Chat Area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2d2d2d", fg="#00ff00", font=("Consolas", 10))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.insert(tk.END, "=== SS-AI: Ethical Pentest Assistant (RoE Enforced) ===\n")
chat_area.insert(tk.END, "=== Coded by: Indrayaza Z ===\n\n")
chat_area.config(state=tk.DISABLED)

# Input Area
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

entry_field = tk.Entry(input_frame, bg="#3d3d3d", fg="#ffffff", font=("Consolas", 11), insertbackground="white")
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
entry_field.bind("<Return>", send_message)

send_button = tk.Button(input_frame, text="Execute", bg="#00ff00", fg="#000000", font=("Consolas", 10, "bold"), command=send_message)
send_button.pack(side=tk.RIGHT, ipadx=10, ipady=2)

root.mainloop()
