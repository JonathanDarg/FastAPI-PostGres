import tkinter as tk
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from api_client import get_recent_sessions
except ImportError:
    from ..api_client import get_recent_sessions


class HistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.sessions = []
        self.selected_label = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = tk.Frame(self, bg="white")
        self.left_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        tk.Button(
            self.left_frame,
            text="Cancel",
            command=lambda: controller.show_page("Home"),
            font=("Arial", 12),
            width=12
        ).pack(anchor="w", pady=5)

        self.list_frame = tk.Frame(self.left_frame, bg="white")
        self.list_frame.pack(fill="both", expand=True, pady=10)

        self.right_frame = tk.Frame(self, bg="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        self.preview_title = tk.Label(
            self.right_frame,
            text="Select a session",
            font=("Arial", 28, "bold"),
            bg="white"
        )
        self.preview_title.pack(pady=(20, 10))

        self.preview_box = tk.Text(
            self.right_frame,
            font=("Courier New", 12),
            bg="white",
            wrap="word",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#d9d9d9",
            padx=12,
            pady=12
        )
        self.preview_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.preview_box.config(state="disabled")

    def refresh(self):
        self.load_sessions()

    def load_sessions(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        try:
            self.sessions = get_recent_sessions()
        except Exception as e:
            tk.Label(
                self.list_frame,
                text=f"Error loading history:\n{e}",
                bg="white",
                fg="red"
            ).pack()
            return

        if not self.sessions:
            tk.Label(
                self.list_frame,
                text="No sessions found.",
                bg="white"
            ).pack()
            return

        for session in self.sessions:
            display_name = f"Session {session.get('id', 'N/A')}"

            item = tk.Label(
                self.list_frame,
                text=f"→ {display_name}",
                anchor="w",
                padx=10,
                pady=8,
                bg="white",
                cursor="hand2",
                font=("Arial", 11)
            )
            item.pack(fill="x")

            item.bind("<Button-1>", lambda e, s=session: self.select_session(e, s))

            tk.Frame(self.list_frame, height=1, bg="#ccc").pack(
                fill="x", padx=5, pady=2
            )

    def select_session(self, event, session):
        if self.selected_label and self.selected_label.winfo_exists():
            self.selected_label.config(bg="white")

        self.selected_label = event.widget
        self.selected_label.config(bg="#e0e0e0")

        self.show_session_preview(session)

    def show_session_preview(self, session):
        self.preview_title.config(
            text=f"Session {session.get('id', 'N/A')}"
        )

        text = self.format_session_text(session)

        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert("1.0", text)
        self.preview_box.config(state="disabled")

    def format_session_text(self, session):
        created_at = session.get("created_at", "N/A")

        if created_at != "N/A":
            created_at = (
                datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                .astimezone(ZoneInfo("America/New_York"))
                .strftime("%m-%d-%Y %I:%M %p")
        )

        return "\n".join([
            f"Session ID: {session.get('id', 'N/A')}",
            f"Created At: {created_at}",
            "",
            f"A: {session.get('a', 'N/A')}",
            f"B: {session.get('b', 'N/A')}",
            f"Sum Result: {session.get('result', 'N/A')}",
            "",
            f"First Name: {session.get('first_name', 'N/A')}",
            f"Last Name: {session.get('last_name', 'N/A')}",
            f"Full Name: {session.get('full_name', 'N/A')}",
        ])