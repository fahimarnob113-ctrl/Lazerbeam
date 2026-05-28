import customtkinter as ctk
import threading
from pathlib import Path
from lazerbeam.capture_pipeline import capture_url
from lazerbeam.url_utils import parse_urls
from lazerbeam.profiles import BUILT_IN_PROFILES

class QueuePanel(ctk.CTkFrame):
    def __init__(self, master, get_vault_path_cb, config, log_cb):
        super().__init__(master)
        self.get_vault_path_cb = get_vault_path_cb
        self.config = config
        self.log_cb = log_cb
        
        ctk.CTkLabel(self, text="Batch Queue", font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(self, text="Paste multiple URLs (one per line):").pack(anchor="w", padx=20)
        
        self.url_box = ctk.CTkTextbox(self, height=150)
        self.url_box.pack(fill="x", padx=20, pady=(5, 10))
        
        self.process_btn = ctk.CTkButton(self, text="Process Queue", command=self.process_queue)
        self.process_btn.pack(anchor="e", padx=20)
        
        self.progress_label = ctk.CTkLabel(self, text="")
        self.progress_label.pack(anchor="w", padx=20, pady=5)
        
    def process_queue(self):
        vault_path = self.get_vault_path_cb()
        if not vault_path:
            self.progress_label.configure(text="Error: No vault selected.")
            return
            
        urls = parse_urls(self.url_box.get("1.0", "end"))
        if not urls:
            self.progress_label.configure(text="No URLs found.")
            return
            
        self.process_btn.configure(state="disabled")
        
        def worker():
            total = len(urls)
            for i, url in enumerate(urls, 1):
                self.progress_label.configure(text=f"Processing {i}/{total}...")
                self.log_cb(f"[Queue] Capturing: {url}")
                try:
                    result = capture_url(
                        url=url,
                        vault_path=Path(vault_path),
                        config=self.config,
                        profile=BUILT_IN_PROFILES["Research"]
                    )
                    self.log_cb(f"[Queue] Saved: {result.output_plan.note_path}")
                except Exception as exc:
                    self.log_cb(f"[Queue] Failed: {url} - {type(exc).__name__}: {exc}")
            
            self.progress_label.configure(text=f"Queue finished. ({total} items)")
            self.process_btn.configure(state="normal")
            
        threading.Thread(target=worker, daemon=True).start()
