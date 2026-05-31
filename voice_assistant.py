import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import datetime
import os
import sys
import webbrowser
import urllib.parse
import urllib.request
import urllib.error
import json
import random
import math
import subprocess
import platform
import calendar
import time


# ── Knowledge Base ────────────────────────────────────────────────────────────

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python programmer get glasses? Because he couldn't C#!",
    "How many programmers does it take to change a light bulb? None – it's a hardware problem!",
    "Why do Java developers wear glasses? Because they don't C++!",
    "What's a computer's favourite snack? Microchips!",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
    "What do you call a fish without eyes? A fsh!",
    "I told my computer I needed a break. Now it won't stop sending me KitKat ads.",
    "Why did the developer go broke? Because he used up all his cache!",
    "What's a programmer's favourite hangout place? The Foo Bar!",
]

GREETINGS = ["Hello!", "Hi there!", "Hey!", "Greetings!", "Howdy!"]

FACTS = [
    "Honey never spoils — archaeologists found 3000-year-old honey in Egyptian tombs.",
    "A day on Venus is longer than a year on Venus.",
    "Octopuses have three hearts and blue blood.",
    "The Eiffel Tower grows about 6 inches taller in summer due to thermal expansion.",
    "Bananas are berries, but strawberries are not.",
    "A group of flamingos is called a flamboyance.",
    "The shortest war in history lasted 38–45 minutes — between Britain and Zanzibar in 1896.",
    "Cleopatra lived closer in time to the Moon landing than to the construction of the Great Pyramid.",
    "There are more stars in the universe than grains of sand on all of Earth's beaches.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
]

TIPS = [
    "Drink at least 8 glasses of water a day to stay hydrated.",
    "Take a 5-minute break every hour when working at a computer.",
    "Sleeping 7-9 hours per night improves memory and focus.",
    "Exercise for at least 30 minutes a day to boost mood and energy.",
    "Practice gratitude daily — write 3 things you're thankful for.",
    "Read for at least 20 minutes a day to expand your knowledge.",
    "Limit screen time before bed for better sleep quality.",
    "Eat more vegetables and fruits — aim for 5 servings a day.",
]

MOTIVATIONS = [
    "Believe you can and you're halfway there. — Theodore Roosevelt",
    "The only way to do great work is to love what you do. — Steve Jobs",
    "It does not matter how slowly you go as long as you do not stop. — Confucius",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. — Churchill",
    "The future belongs to those who believe in the beauty of their dreams. — Eleanor Roosevelt",
    "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
    "You are never too old to set another goal or to dream a new dream. — C.S. Lewis",
    "Act as if what you do makes a difference. It does. — William James",
]


# ── Assistant Brain ───────────────────────────────────────────────────────────

class AssistantBrain:

    def __init__(self):
        self.name = "ARIA"
        self.history = []

    def process(self, user_input):
        txt = user_input.strip().lower()
        self.history.append(("user", user_input.strip()))
        response = self._route(txt, user_input.strip())
        self.history.append(("aria", response))
        return response

    def _route(self, t, raw):
        # greetings
        if any(w in t for w in ["hello","hi","hey","greetings","howdy","sup","good morning","good evening","good afternoon"]):
            hour = datetime.datetime.now().hour
            if hour < 12:   tod = "Good morning"
            elif hour < 17: tod = "Good afternoon"
            else:           tod = "Good evening"
            return f"{tod}! 👋 I'm {self.name}, your AI assistant. How can I help you today?"

        # farewell
        if any(w in t for w in ["bye","goodbye","exit","quit","see you","later","farewell"]):
            return "Goodbye! 👋 It was great talking to you. Have a wonderful day! 🌟"

        # time
        if "time" in t and not "timezone" in t:
            now = datetime.datetime.now()
            return f"🕐 The current time is **{now.strftime('%I:%M:%S %p')}**."

        # date
        if any(w in t for w in ["date","today","what day"]):
            now = datetime.datetime.now()
            return (f"📅 Today is **{now.strftime('%A, %d %B %Y')}**.\n"
                    f"   Week {now.strftime('%W')} of {now.year}.")

        # day of week
        if "day of week" in t or "what day is" in t:
            now = datetime.datetime.now()
            return f"📅 Today is **{now.strftime('%A')}**."

        # calendar
        if "calendar" in t:
            now = datetime.datetime.now()
            cal = calendar.month(now.year, now.month)
            return f"📆 **{now.strftime('%B %Y')}**\n```\n{cal}```"

        # joke
        if any(w in t for w in ["joke","funny","laugh","humor","make me laugh"]):
            return f"😄 {random.choice(JOKES)}"

        # fact
        if any(w in t for w in ["fact","did you know","interesting","trivia","tell me something"]):
            return f"🧠 **Interesting Fact:**\n{random.choice(FACTS)}"

        # motivation / quote
        if any(w in t for w in ["motivat","inspir","quote","encourage","cheer","uplift"]):
            return f"💪 **Motivation for you:**\n\n_{random.choice(MOTIVATIONS)}_"

        # tip
        if any(w in t for w in ["tip","advice","suggestion","health","productivity"]):
            return f"💡 **Tip:**\n{random.choice(TIPS)}"

        # calculator
        if any(w in t for w in ["calculat","compute","math","what is","solve","evaluate"]):
            result = self._calculate(t, raw)
            if result:
                return result

        # fibonacci
        if "fibonacci" in t:
            return self._fibonacci_cmd(t)

        # search web
        if any(w in t for w in ["search","google","look up","find","browse"]):
            query = self._extract_after(raw, ["search for","search","google","look up","find","browse"])
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(url)
                return f"🔍 Searching Google for **\"{query}\"** ...\n   Opening in your browser!"
            return "🔍 What would you like me to search for?"

        # open website
        if any(w in t for w in ["open","go to","visit","navigate"]):
            site = self._extract_after(raw, ["open","go to","visit","navigate to","navigate"])
            if site:
                if "." not in site:
                    site += ".com"
                if not site.startswith("http"):
                    site = "https://" + site
                webbrowser.open(site)
                return f"🌐 Opening **{site}** in your browser!"

        # YouTube
        if "youtube" in t:
            query = self._extract_after(raw, ["youtube","on youtube","play on youtube"])
            if query:
                url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                webbrowser.open(url)
                return f"▶️ Searching YouTube for **\"{query}\"** ..."
            webbrowser.open("https://www.youtube.com")
            return "▶️ Opening YouTube!"

        # Wikipedia
        if "wikipedia" in t or "wiki" in t:
            query = self._extract_after(raw, ["wikipedia","wiki","search wikipedia for"])
            if query:
                url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query.replace(' ','_'))}"
                webbrowser.open(url)
                return f"📖 Opening Wikipedia for **\"{query}\"** ..."
            return "📖 What topic shall I look up on Wikipedia?"

        # system info
        if any(w in t for w in ["system","os","platform","computer info","my pc","machine"]):
            return self._system_info()

        # battery / cpu  (platform only, no psutil)
        if "battery" in t:
            return "🔋 Battery info requires the 'psutil' library. Try: pip install psutil"

        # open notepad / calculator app
        if "notepad" in t or "text editor" in t:
            self._open_app(["notepad"] if platform.system()=="Windows" else ["gedit","nano"])
            return "📝 Opening text editor!"

        if "calculator app" in t or "open calculator" in t:
            if platform.system() == "Windows":
                os.system("calc")
            elif platform.system() == "Darwin":
                os.system("open -a Calculator")
            return "🧮 Opening system calculator!"

        # screenshot folder / file manager
        if "file manager" in t or "explorer" in t:
            if platform.system() == "Windows":
                os.system("explorer .")
            elif platform.system() == "Darwin":
                os.system("open .")
            else:
                os.system("xdg-open .")
            return "📁 Opening file manager!"

        # name / who are you
        if any(w in t for w in ["your name","who are you","what are you","who am i talking","introduce"]):
            return (f"🤖 I'm **{self.name}** — Artificial Responsive Intelligence Assistant.\n\n"
                    "   I can help you with:\n"
                    "   • Time & Date  • Jokes & Facts\n"
                    "   • Web Search   • Calculator\n"
                    "   • Motivation   • System Info\n"
                    "   • Fibonacci    • Wikipedia\n"
                    "   • And much more — just ask!")

        # help
        if any(w in t for w in ["help","commands","what can you do","capabilities","features"]):
            return self._help()

        # thank you
        if any(w in t for w in ["thank","thanks","appreciate","grateful"]):
            return "😊 You're very welcome! Happy to help anytime."

        # how are you
        if any(w in t for w in ["how are you","how do you do","you okay","you good"]):
            return "😊 I'm doing great, thank you for asking! Ready to assist you with anything."

        # weather (redirect — no API key)
        if "weather" in t:
            city = self._extract_after(raw, ["weather in","weather for","weather"])
            if city:
                url = f"https://www.google.com/search?q=weather+{urllib.parse.quote(city)}"
                webbrowser.open(url)
                return f"🌤️ Opening weather for **{city}** in your browser!"
            webbrowser.open("https://www.google.com/search?q=weather+today")
            return "🌤️ Opening weather in your browser!"

        # news
        if "news" in t:
            webbrowser.open("https://news.google.com")
            return "📰 Opening Google News in your browser!"

        # maps
        if "map" in t or "direction" in t or "navigate to" in t:
            place = self._extract_after(raw, ["map of","directions to","navigate to","maps"])
            if place:
                url = f"https://www.google.com/maps/search/{urllib.parse.quote(place)}"
                webbrowser.open(url)
                return f"🗺️ Opening Google Maps for **{place}**!"
            webbrowser.open("https://maps.google.com")
            return "🗺️ Opening Google Maps!"

        # email
        if "email" in t or "gmail" in t:
            webbrowser.open("https://mail.google.com")
            return "📧 Opening Gmail in your browser!"

        # history
        if "history" in t and "conversation" in t:
            return self._show_history()

        # clear history
        if "clear history" in t or "reset" in t:
            self.history = []
            return "🗑️ Conversation history cleared!"

        # default
        query = urllib.parse.quote(raw)
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return (f"🤔 I'm not sure about that, but I've searched Google for:\n"
                f"   **\"{raw}\"**\n   Check your browser for results!")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _calculate(self, t, raw):
        # extract math expression
        expr = self._extract_after(raw, ["calculate","compute","what is","solve","evaluate","math"])
        if not expr:
            expr = raw
        # allow safe chars only
        safe = "0123456789+-*/.() **%sqrtpielog"
        cleaned = expr.replace("^","**").replace("√","sqrt(").replace("x","*")
        try:
            # replace sqrt, pi, e
            cleaned = cleaned.replace("sqrt","math.sqrt").replace("pi","math.pi").replace("log","math.log")
            result = eval(cleaned, {"__builtins__": {}, "math": math})
            return f"🧮 **{expr.strip()}**  =  **{result:,}**"
        except:
            return None

    def _fibonacci_cmd(self, t):
        nums = [int(w) for w in t.split() if w.isdigit()]
        if nums:
            n = nums[0]
            a, b = 0, 1
            seq = [0]
            for _ in range(n-1):
                a, b = b, a+b
                seq.append(a)
            return f"🔢 First **{n}** Fibonacci numbers:\n   {', '.join(map(str,seq))}"
        return "🔢 Tell me how many Fibonacci numbers you want! E.g. 'fibonacci 10'"

    def _extract_after(self, raw, keywords):
        low = raw.lower()
        for kw in sorted(keywords, key=len, reverse=True):
            idx = low.find(kw)
            if idx != -1:
                after = raw[idx+len(kw):].strip(" ?,.")
                if after:
                    return after
        return ""

    def _system_info(self):
        info = {
            "OS":       platform.system(),
            "Version":  platform.version()[:40],
            "Machine":  platform.machine(),
            "Processor":platform.processor()[:40] or "N/A",
            "Python":   sys.version.split()[0],
            "Node":     platform.node(),
        }
        lines = ["💻 **System Information:**\n"]
        for k, v in info.items():
            lines.append(f"   {k:<12}:  {v}")
        return "\n".join(lines)

    def _open_app(self, names):
        for name in names:
            try:
                subprocess.Popen([name])
                return
            except:
                continue

    def _help(self):
        return (
            "🆘 **What I can do — just type naturally!**\n\n"
            "  🕐 Time & Date   — 'What time is it?' / 'What's today's date?'\n"
            "  😄 Joke          — 'Tell me a joke'\n"
            "  🧠 Fact          — 'Give me a fun fact'\n"
            "  💪 Motivation    — 'Motivate me'\n"
            "  💡 Tip           — 'Give me a productivity tip'\n"
            "  🧮 Calculator    — 'What is 25 * 4 + 10?'\n"
            "  🔍 Web Search    — 'Search for Python tutorials'\n"
            "  🌐 Open Website  — 'Open github.com'\n"
            "  ▶️ YouTube       — 'Search YouTube for lo-fi music'\n"
            "  📖 Wikipedia     — 'Wikipedia Artificial Intelligence'\n"
            "  🌤️ Weather       — 'Weather in London'\n"
            "  🗺️ Maps          — 'Directions to Eiffel Tower'\n"
            "  📰 News          — 'Show me the news'\n"
            "  📧 Email         — 'Open Gmail'\n"
            "  💻 System Info   — 'Show system info'\n"
            "  🔢 Fibonacci     — 'Fibonacci 10'\n"
            "  📅 Calendar      — 'Show calendar'\n"
            "  📜 History       — 'Show conversation history'\n"
        )

    def _show_history(self):
        if not self.history:
            return "📜 No conversation history yet."
        lines = ["📜 **Conversation History:**\n"]
        for role, msg in self.history[-20:]:
            prefix = "You" if role == "user" else "ARIA"
            lines.append(f"  [{prefix}] {msg[:80]}{'...' if len(msg)>80 else ''}")
        return "\n".join(lines)


# ── GUI ───────────────────────────────────────────────────────────────────────

class VoiceAssistantApp(tk.Tk):

    BG     = "#0a0a14"
    PANEL  = "#12121f"
    CARD   = "#1a1a2e"
    ACCENT = "#7c3aed"
    ACC2   = "#1e1b4b"
    TEXT   = "#e2e8f0"
    MUTED  = "#64748b"
    GREEN  = "#10b981"
    YELLOW = "#f59e0b"
    RED    = "#ef4444"
    CYAN   = "#06b6d4"
    BORDER = "#2d2d4e"
    FONT   = "Segoe UI"

    def __init__(self):
        super().__init__()
        self.brain = AssistantBrain()
        self.title("ARIA — AI Voice Assistant · Hex Softwares")
        self.geometry("1050x720")
        self.minsize(900, 640)
        self.configure(bg=self.BG)
        self._typing = False
        self._build_ui()
        self._welcome()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── top bar ──
        topbar = tk.Frame(self, bg=self.PANEL, height=64)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        # logo area
        logo_f = tk.Frame(topbar, bg=self.PANEL)
        logo_f.pack(side="left", padx=20)
        tk.Label(logo_f, text="🤖", font=(self.FONT, 22),
                 bg=self.PANEL).pack(side="left", pady=10)
        name_f = tk.Frame(logo_f, bg=self.PANEL)
        name_f.pack(side="left", padx=8)
        tk.Label(name_f, text="ARIA", font=(self.FONT, 16, "bold"),
                 bg=self.PANEL, fg=self.TEXT).pack(anchor="w")
        tk.Label(name_f, text="Artificial Responsive Intelligence Assistant",
                 font=(self.FONT, 8), bg=self.PANEL, fg=self.MUTED).pack(anchor="w")

        # status
        self.status_dot = tk.Label(topbar, text="●", font=(self.FONT, 12),
                                   bg=self.PANEL, fg=self.GREEN)
        self.status_dot.pack(side="right", padx=(0, 6), pady=20)
        self.status_lbl = tk.Label(topbar, text="Online",
                                   font=(self.FONT, 9), bg=self.PANEL, fg=self.GREEN)
        self.status_lbl.pack(side="right", pady=20)

        tk.Label(topbar, text="Hex Softwares  ·  Python Internship  ·  Task 2",
                 font=(self.FONT, 8), bg=self.PANEL,
                 fg=self.MUTED).pack(side="right", padx=20)

        # ── body ──
        body = tk.Frame(self, bg=self.BG)
        body.pack(fill="both", expand=True)

        # ── sidebar ──
        sidebar = tk.Frame(body, bg=self.PANEL, width=210)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Quick Commands",
                 font=(self.FONT, 10, "bold"),
                 bg=self.PANEL, fg=self.TEXT).pack(pady=(18, 6), padx=14, anchor="w")

        quick = [
            ("🕐 Time",         "What time is it?"),
            ("📅 Date",         "What is today's date?"),
            ("😄 Joke",         "Tell me a joke"),
            ("🧠 Fun Fact",     "Tell me a fun fact"),
            ("💪 Motivation",   "Motivate me"),
            ("💡 Tip",          "Give me a tip"),
            ("📅 Calendar",     "Show me the calendar"),
            ("💻 System Info",  "Show system info"),
            ("🔢 Fibonacci",    "Fibonacci 10"),
            ("📰 News",         "Show me the news"),
            ("📧 Gmail",        "Open Gmail"),
            ("🆘 Help",         "Help"),
            ("🗑️ Clear Chat",   "__clear__"),
        ]
        for label, cmd in quick:
            tk.Button(sidebar, text=label,
                      font=(self.FONT, 9), anchor="w",
                      bg=self.PANEL, fg=self.MUTED,
                      activebackground=self.ACC2, activeforeground=self.TEXT,
                      bd=0, padx=14, pady=6, cursor="hand2",
                      command=lambda c=cmd: self._quick(c)
                      ).pack(fill="x", padx=4, pady=1)

        tk.Label(sidebar, text="© 2025 Hex Softwares",
                 font=(self.FONT, 8), bg=self.PANEL,
                 fg=self.MUTED).pack(side="bottom", pady=12)

        # ── chat area ──
        chat_frame = tk.Frame(body, bg=self.BG)
        chat_frame.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        # chat display
        display_frame = tk.Frame(chat_frame, bg=self.CARD,
                                 highlightbackground=self.BORDER, highlightthickness=1)
        display_frame.pack(fill="both", expand=True)

        self.chat = tk.Text(display_frame,
                            font=(self.FONT, 11),
                            bg=self.CARD, fg=self.TEXT,
                            relief="flat", bd=0,
                            wrap="word", state="disabled",
                            padx=18, pady=14,
                            cursor="arrow",
                            spacing1=4, spacing3=4)
        sb = ttk.Scrollbar(display_frame, orient="vertical", command=self.chat.yview)
        self.chat.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.chat.pack(fill="both", expand=True)

        # tags
        self.chat.tag_config("user_name",  foreground=self.CYAN,  font=(self.FONT, 10, "bold"))
        self.chat.tag_config("user_msg",   foreground=self.TEXT,  font=(self.FONT, 11))
        self.chat.tag_config("aria_name",  foreground=self.ACCENT, font=(self.FONT, 10, "bold"))
        self.chat.tag_config("aria_msg",   foreground="#c4b5fd",  font=(self.FONT, 11))
        self.chat.tag_config("system",     foreground=self.MUTED, font=(self.FONT, 9, "italic"))
        self.chat.tag_config("time_stamp", foreground=self.MUTED, font=(self.FONT, 8))
        self.chat.tag_config("bold",       font=(self.FONT, 11, "bold"), foreground=self.YELLOW)

        # ── input bar ──
        input_frame = tk.Frame(chat_frame, bg=self.CARD,
                               highlightbackground=self.BORDER, highlightthickness=1)
        input_frame.pack(fill="x", pady=(10, 0))

        self.input_var = tk.StringVar()
        self.input_box = tk.Entry(input_frame,
                                  textvariable=self.input_var,
                                  font=(self.FONT, 12),
                                  bg=self.CARD, fg=self.TEXT,
                                  insertbackground=self.TEXT,
                                  relief="flat", bd=0)
        self.input_box.pack(side="left", fill="both", expand=True,
                            padx=16, pady=14, ipady=4)
        self.input_box.bind("<Return>", lambda e: self._send())
        self.input_box.bind("<Up>",     self._history_up)
        self.input_box.bind("<Down>",   self._history_down)
        self._cmd_history = []
        self._cmd_idx = -1

        send_btn = tk.Button(input_frame, text="Send  ➤",
                             font=(self.FONT, 10, "bold"),
                             bg=self.ACCENT, fg="white",
                             relief="flat", bd=0,
                             padx=18, pady=10, cursor="hand2",
                             command=self._send,
                             activebackground=self.ACC2,
                             activeforeground="white")
        send_btn.pack(side="right", padx=10, pady=8)

        clear_btn = tk.Button(input_frame, text="🗑️",
                              font=(self.FONT, 12),
                              bg=self.CARD, fg=self.MUTED,
                              relief="flat", bd=0,
                              padx=8, pady=10, cursor="hand2",
                              command=self._clear_chat,
                              activebackground=self.PANEL)
        clear_btn.pack(side="right", pady=8)

        self.char_count = tk.Label(input_frame, text="0 / 500",
                                   font=(self.FONT, 8),
                                   bg=self.CARD, fg=self.MUTED)
        self.char_count.pack(side="right", padx=4)
        self.input_var.trace("w", self._update_char_count)

        self.input_box.focus()

    # ── chat helpers ──────────────────────────────────────────────────────────

    def _append(self, text, tag="aria_msg"):
        self.chat.config(state="normal")
        self.chat.insert("end", text, tag)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _append_msg(self, sender, msg, is_user=False):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self._append(f"\n  {now}\n", "time_stamp")
        name_tag = "user_name" if is_user else "aria_name"
        self._append(f"  {'You' if is_user else '🤖 ARIA'}  ", name_tag)
        self._append("\n", "system")
        msg_tag = "user_msg" if is_user else "aria_msg"
        # simple bold: **text**
        parts = msg.split("**")
        for i, part in enumerate(parts):
            self._append(f"  {part}\n" if i == 0 else part,
                         "bold" if i % 2 == 1 else msg_tag)
        self._append("\n", "system")

    def _welcome(self):
        self._append("  ╔══════════════════════════════════════════════╗\n", "system")
        self._append("  ║   ARIA  —  AI Assistant  ·  Hex Softwares   ║\n", "aria_name")
        self._append("  ╚══════════════════════════════════════════════╝\n\n", "system")
        self._append_msg("ARIA",
            "Hello! 👋 I'm ARIA, your AI assistant.\n\n"
            "  I can help with time, dates, jokes, facts, calculations,\n"
            "  web searches, Wikipedia, YouTube, weather, and much more!\n\n"
            "  Type 'help' to see all my commands, or just chat naturally! 😊")

    def _send(self):
        text = self.input_var.get().strip()
        if not text or self._typing:
            return
        self.input_var.set("")
        self._cmd_history.append(text)
        self._cmd_idx = -1
        self._append_msg("You", text, is_user=True)
        self._show_typing()
        threading.Thread(target=self._process, args=(text,), daemon=True).start()

    def _process(self, text):
        time.sleep(0.4)  # simulate thinking
        response = self.brain.process(text)
        self.after(0, self._hide_typing)
        self.after(0, lambda: self._append_msg("ARIA", response))

    def _show_typing(self):
        self._typing = True
        self.status_lbl.config(text="Thinking...", fg=self.YELLOW)
        self.status_dot.config(fg=self.YELLOW)

    def _hide_typing(self):
        self._typing = False
        self.status_lbl.config(text="Online", fg=self.GREEN)
        self.status_dot.config(fg=self.GREEN)

    def _quick(self, cmd):
        if cmd == "__clear__":
            self._clear_chat()
            return
        self.input_var.set(cmd)
        self._send()

    def _clear_chat(self):
        self.chat.config(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.config(state="disabled")
        self.brain.history = []
        self._welcome()

    def _update_char_count(self, *_):
        n = len(self.input_var.get())
        self.char_count.config(
            text=f"{n} / 500",
            fg=self.RED if n > 450 else self.MUTED)

    def _history_up(self, event):
        if self._cmd_history:
            self._cmd_idx = max(0, len(self._cmd_history)-1 if self._cmd_idx < 0
                                else self._cmd_idx - 1)
            self.input_var.set(self._cmd_history[self._cmd_idx])

    def _history_down(self, event):
        if self._cmd_history and self._cmd_idx >= 0:
            self._cmd_idx += 1
            if self._cmd_idx >= len(self._cmd_history):
                self._cmd_idx = -1
                self.input_var.set("")
            else:
                self.input_var.set(self._cmd_history[self._cmd_idx])


if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()
