import customtkinter as ctk
import threading
from tkinter import messagebox
from utils.logger import get_logger

logger = get_logger(__name__)

class BrowserTab(ctk.CTkFrame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main = main_window
        self._build()

    def _build(self):
        # Address bar
        addr_frame = ctk.CTkFrame(self)
        addr_frame.pack(fill="x", padx=10, pady=10)

        self.url_entry = ctk.CTkEntry(addr_frame, placeholder_text="Enter URL...", width=600)
        self.url_entry.pack(side="left", padx=(0,10))

        self.go_button = ctk.CTkButton(addr_frame, text="Crawl", command=self.start_crawl, width=100)
        self.go_button.pack(side="left")

        # Mode selection
        self.mode_var = ctk.StringVar(value="normal")
        modes = [("Normal", "normal"), ("Anonymous", "anonymous"), ("Tor", "tor")]
        for text, value in modes:
            ctk.CTkRadioButton(addr_frame, text=text, variable=self.mode_var,
                               value=value).pack(side="left", padx=10)

        # Dynamic rendering checkbox
        self.dynamic_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(addr_frame, text="Dynamic Rendering", variable=self.dynamic_var).pack(side="left", padx=10)

        # Progress bar (indeterminate)
        self.progress = ctk.CTkProgressBar(self, mode='indeterminate')
        self.progress.pack(fill="x", padx=10, pady=5)
        self.progress.set(0)

        # Text display
        self.result_text = ctk.CTkTextbox(self, wrap="word")
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Status bar
        self.status_var = ctk.StringVar(value="Ready")
        status = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w")
        status.pack(fill="x", padx=10, pady=(0,5))

    def start_crawl(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return
        threading.Thread(target=self._crawl_task, args=(url,), daemon=True).start()

    def _crawl_task(self, url):
        self.go_button.configure(state="disabled")
        self.progress.start()
        self.status_var.set("Crawling...")

        try:
            # Determine mode
            mode = self.mode_var.get()
            crawler = self.main.get_crawler()
            # If tor mode selected but tor not running, fallback
            if mode == "tor" and not self.main.tor_manager:
                messagebox.showwarning("Tor", "Tor not running. Using anonymous mode.")
                mode = "anonymous"

            # For anonymous mode we rely on proxy pool (already in crawler)
            # For normal, no proxy (crawler will use direct)

            result = crawler.crawl(url, force=False, dynamic=self.dynamic_var.get())

            # Handle compliance blocks
            if isinstance(result, str) and (result.startswith('robots_blocked') or result.startswith('http_')):
                answer = messagebox.askyesno(
                    "Compliance Warning",
                    f"{result} for {url}.\nDo you want to force crawl?"
                )
                if answer:
                    self.status_var.set("Force crawling...")
                    result = crawler.crawl(url, force=True, dynamic=self.dynamic_var.get())
                else:
                    self.result_text.delete("1.0", "end")
                    self.result_text.insert("1.0", f"Cancelled due to {result}.")
                    return

            if result is None:
                self.status_var.set("Crawl failed")
                messagebox.showerror("Error", "Failed to retrieve content.")
                return

            # Display text
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result.get("text", ""))

            # Download media
            if result.get("images"):
                self.status_var.set(f"Downloading {len(result['images'])} images...")
                downloader = self.main.downloader if hasattr(self.main, 'downloader') else None
                # Not implemented fully; placeholder
                logger.info(f"Images: {result['images']}")

            if result.get("videos"):
                self.status_var.set(f"Downloading {len(result['videos'])} videos...")
                logger.info(f"Videos: {result['videos']}")

            self.status_var.set("Crawl completed.")
        except Exception as e:
            logger.exception("Crawl error")
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()
            self.go_button.configure(state="normal")
