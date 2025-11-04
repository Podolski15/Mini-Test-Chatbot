# gui_chatbot.py
# Simple beginner-friendly chatbot GUI using tkinter
# Save file and run: python gui_chatbot.py

import tkinter as tk
from tkinter import scrolledtext
import time
import random

# ---------- Chat "brain" ----------
knowledge = [
    (["hi", "hello", "hey"], "Hi there! I am a mini chatbot. How can I help you today?"),
    (["how are you", "how are you?"], "I'm just code, but I'm doing great — thanks! What about you?"),
    (["help", "commands"], "Try: 'time', 'joke', 'my name is <yourname>', or use the buttons below."),
    (["time", "what time"], lambda: f"Current time: {time.strftime('%H:%M:%S')}"),
    (["joke", "tell me a joke"], "Why do programmers prefer dark mode? Because light attracts bugs 😄"),
    (["bye", "goodbye", "see you"], "Goodbye! Have a nice day.")
]

fallback_questions = [
    "That's a great question! I don't know yet, but I'm learning.",
    "Tell me more.",
    "I don't know that yet. Try 'help'.",
    "Interesting — tell me more."
]

# ---------- Helper functions ----------
def find_reply(user_text, state):
    t = user_text.lower().strip().strip("'\"")  # remove extra quotes
    # check for explicit "my name is ..." or "i am / i'm"
    if ("my name is " in t) or t.startswith("i am ") or t.startswith("i'm "):
        # try to extract name
        tokens = t.replace("i'm ", "i am ").split("i am ")
        if len(tokens) > 1 and tokens[1].strip():
            name = tokens[1].strip().title()
            state['name'] = name
            return f"Nice to meet you, {name}!"
        # fallback
        state['name'] = None

    # check knowledge base
    for patterns, reply in knowledge:
        for p in patterns:
            if p in t:
                return reply() if callable(reply) else reply

    # if user asked a question (ends with ?)
    if user_text.strip().endswith('?'):
        return fallback_questions[0]

    # if user says affectionate phrases or "i love you" -> friendly generic
    if "love" in t or "i love you" in t:
        return "I appreciate the kindness! I'm a little program, but that warms my bytes 😊"

    # default fallback
    return random.choice(fallback_questions)

# ---------- GUI ----------
class MiniChatbot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Logan's Mini Chatbot")
        self.geometry("560x520")
        self.resizable(False, False)

        self.state = {'name': None}

        # Top label
        header = tk.Label(self, text="Logan's Mini Chatbot — (Beginner)", font=("Arial", 14, "bold"))
        header.pack(pady=(8, 4))

        # Chat display (scrollable)
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', font=("Segoe UI", 10))
        self.chat_display.pack(padx=12, pady=(0,8), fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(padx=12, pady=(0,8), fill=tk.X)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(input_frame, textvariable=self.input_var, font=("Segoe UI", 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.input_entry.bind("<Return>", lambda e: self.on_send())

        send_btn = tk.Button(input_frame, text="Send", command=self.on_send, width=10)
        send_btn.pack(side=tk.LEFT, padx=(8,0))

        # Quick-reply buttons
        quick_frame = tk.Frame(self)
        quick_frame.pack(padx=12, pady=(0,10), fill=tk.X)

        for txt in ["hi", "help", "time", "joke", "my name is Loganesh", "bye"]:
            b = tk.Button(quick_frame, text=txt, command=lambda t=txt: self.quick_send(t))
            b.pack(side=tk.LEFT, padx=4, pady=4)

        # Bottom controls
        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(padx=12, pady=(0,12), fill=tk.X)
        self.name_label = tk.Label(ctrl_frame, text="Name: —", anchor='w')
        self.name_label.pack(side=tk.LEFT)

        clear_btn = tk.Button(ctrl_frame, text="Clear Chat", command=self.clear_chat)
        clear_btn.pack(side=tk.RIGHT, padx=(4,0))

        exit_btn = tk.Button(ctrl_frame, text="Exit", command=self.quit)
        exit_btn.pack(side=tk.RIGHT)

        # Start message
        self._bot_say("Hello! I'm a tiny test chatbot. Try: hi, help, joke, or tell me your name.")

    def append_text(self, text, who="bot"):
        self.chat_display.configure(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        if who == "user":
            self.chat_display.insert(tk.END, f"You ({timestamp}): {text}\n")
        else:
            self.chat_display.insert(tk.END, f"Bot ({timestamp}): {text}\n")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')

    def _bot_say(self, text):
        self.append_text(text, "bot")
        # update name label if set
        if self.state.get('name'):
            self.name_label.config(text=f"Name: {self.state['name']}")

    def on_send(self):
        user_text = self.input_var.get().strip()
        if not user_text:
            return
        self.append_text(user_text, "user")
        self.input_var.set("")
        # small "thinking" delay simulation
        self.after(250, lambda: self.process_user(user_text))

    def quick_send(self, text):
        self.input_var.set(text)
        self.on_send()

    def process_user(self, text):
        reply = find_reply(text, self.state)
        self._bot_say(reply)

    def clear_chat(self):
        self.chat_display.configure(state='normal')
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.configure(state='disabled')
        self.state['name'] = None
        self.name_label.config(text="Name: —")
        self._bot_say("Chat cleared. Say hi to start again!")

if __name__ == "__main__":
    app = MiniChatbot()
    app.mainloop()
