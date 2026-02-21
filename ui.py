import tkinter as tk
import threading
from assistant import start_assistant, stop_assistant


def update_chat(message):
    chat_box.insert(tk.END, message)
    chat_box.see(tk.END)


def start_thread():
    threading.Thread(
        target=start_assistant,
        args=(update_chat,),
        daemon=True
    ).start()

    status_label.config(text="Status: Listening...", fg="#00ff88")


def stop_thread():
    stop_assistant()
    status_label.config(text="Status: Stopped", fg="#ff4d4d")
    update_chat("Assistant stopped.\n\n")


# ---------------- UI DESIGN ----------------
root = tk.Tk()
root.title("FARINA - Voice Assistant")
root.geometry("520x600")
root.configure(bg="#1e1e2f")

title = tk.Label(
    root,
    text="FARINA",
    font=("Helvetica", 32, "bold"),
    bg="#1e1e2f",
    fg="#00e5ff"
)
title.pack(pady=20)

subtitle = tk.Label(
    root,
    text="Voice Activated Virtual Assistant",
    font=("Helvetica", 12),
    bg="#1e1e2f",
    fg="white"
)
subtitle.pack(pady=5)

status_label = tk.Label(
    root,
    text="Status: Idle",
    font=("Helvetica", 12),
    bg="#1e1e2f",
    fg="white"
)
status_label.pack(pady=10)

chat_box = tk.Text(
    root,
    height=18,
    width=60,
    bg="#2b2b3c",
    fg="white",
    font=("Consolas", 10),
    bd=0
)
chat_box.pack(pady=15)
chat_box.insert(tk.END, "Welcome to FARINA Assistant\n\n")

button_frame = tk.Frame(root, bg="#1e1e2f")
button_frame.pack(pady=20)

start_button = tk.Button(
    button_frame,
    text="Start Listening",
    command=start_thread,
    bg="#00c853",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=15,
    relief="flat"
)
start_button.grid(row=0, column=0, padx=15)

stop_button = tk.Button(
    button_frame,
    text="Stop",
    command=stop_thread,
    bg="#d50000",
    fg="white",
    font=("Helvetica", 12, "bold"),
    width=15,
    relief="flat"
)
stop_button.grid(row=0, column=1, padx=15)

footer = tk.Label(
    root,
    text="Powered by Groq LLM",
    font=("Helvetica", 10),
    bg="#1e1e2f",
    fg="#888888"
)
footer.pack(side="bottom", pady=10)

root.mainloop()