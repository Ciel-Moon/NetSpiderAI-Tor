import customtkinter as ctk
from config import settings

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("500x600")
        self._build()

    def _build(self):
        # Tor settings
        tor_frame = ctk.CTkFrame(self)
        tor_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(tor_frame, text="Tor", font=("Arial", 16)).pack(anchor="w")

        row = ctk.CTkFrame(tor_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text="SOCKS Port:", width=100).pack(side="left")
        self.tor_socks = ctk.CTkEntry(row)
        self.tor_socks.insert(0, str(settings.TOR_SOCKS_PORT))
        self.tor_socks.pack(side="left", padx=5)

        row = ctk.CTkFrame(tor_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text="Control Port:", width=100).pack(side="left")
        self.tor_control = ctk.CTkEntry(row)
        self.tor_control.insert(0, str(settings.TOR_CONTROL_PORT))
        self.tor_control.pack(side="left", padx=5)

        # Crawler settings
        crawl_frame = ctk.CTkFrame(self)
        crawl_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(crawl_frame, text="Crawler", font=("Arial", 16)).pack(anchor="w")

        row = ctk.CTkFrame(crawl_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text="Timeout (s):", width=100).pack(side="left")
        self.timeout = ctk.CTkEntry(row)
        self.timeout.insert(0, str(settings.REQUEST_TIMEOUT))
        self.timeout.pack(side="left", padx=5)

        row = ctk.CTkFrame(crawl_frame)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text="Max Retries:", width=100).pack(side="left")
        self.retries = ctk.CTkEntry(row)
        self.retries.insert(0, str(settings.MAX_RETRIES))
        self.retries.pack(side="left", padx=5)

        # Save button
        ctk.CTkButton(self, text="Save", command=self.save).pack(pady=20)

    def save(self):
        # Update settings module (in real app, update and persist)
        settings.TOR_SOCKS_PORT = int(self.tor_socks.get())
        settings.TOR_CONTROL_PORT = int(self.tor_control.get())
        settings.REQUEST_TIMEOUT = int(self.timeout.get())
        settings.MAX_RETRIES = int(self.retries.get())
        self.destroy()
