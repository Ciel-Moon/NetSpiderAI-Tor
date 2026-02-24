import customtkinter as ctk
from tkinter import ttk

class TaskPanel(ctk.CTkFrame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main = main_window
        self._build()

    def _build(self):
        # Treeview for tasks
        columns = ('ID', 'URL', 'Status', 'Progress', 'Start Time')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(btn_frame, text="Pause", command=self.pause_task).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Resume", command=self.resume_task).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.cancel_task).pack(side="left", padx=5)

    def pause_task(self):
        pass

    def resume_task(self):
        pass

    def cancel_task(self):
        pass

    def add_task(self, task_id, url):
        self.tree.insert('', 'end', values=(task_id, url, 'pending', '0%', ''))
