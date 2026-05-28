import customtkinter as ctk
from pathlib import Path
import os
import threading
from lazerbeam.history import CaptureHistory
from lazerbeam.capture_pipeline import capture_url
from lazerbeam.profiles import BUILT_IN_PROFILES

class HistoryPanel(ctk.CTkFrame):
    def __init__(self, master, get_vault_path_cb, config, log_cb):
        super().__init__(master)
        self.get_vault_path_cb = get_vault_path_cb
        self.config = config
        self.log_cb = log_cb
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        ctk.CTkLabel(header, text="Capture History", font=("Segoe UI", 20, "bold")).pack(side="left")
        ctk.CTkButton(header, text="Refresh", width=80, command=self.load_history).pack(side="right")
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
    def load_history(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        vault_path = self.get_vault_path_cb()
        if not vault_path:
            ctk.CTkLabel(self.scroll_frame, text="No vault selected.").pack(pady=20)
            return
            
        history_path = Path(vault_path) / ".lazerbeam" / "history.json"
        history = CaptureHistory(history_path)
        entries = history.load()
        
        if not entries:
            ctk.CTkLabel(self.scroll_frame, text="No history found.").pack(pady=20)
            return
            
        for entry in reversed(entries):
            row = ctk.CTkFrame(self.scroll_frame)
            row.pack(fill="x", pady=5, padx=5)
            
            info = ctk.CTkLabel(row, text=f"[{entry.source}] {entry.title}\n{entry.url}", justify="left")
            info.pack(side="left", padx=10, pady=10)
            
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="right", padx=10, pady=10)
            
            ctk.CTkButton(btn_frame, text="Re-run", width=60, command=lambda e=entry: self.rerun_capture(e)).pack(side="top", pady=2)
            if entry.note_path and Path(entry.note_path).exists():
                ctk.CTkButton(btn_frame, text="Open", width=60, command=lambda e=entry: os.startfile(e.note_path)).pack(side="top", pady=2)

    def rerun_capture(self, entry):
        self.log_cb(f"Re-running: {entry.url}")
        def worker():
            try:
                result = capture_url(
                    url=entry.url,
                    vault_path=Path(self.get_vault_path_cb()),
                    config=self.config,
                    profile=BUILT_IN_PROFILES["Research"]
                )
                self.log_cb(f"Re-run success: {result.output_plan.note_path}")
            except Exception as exc:
                self.log_cb(f"Re-run failed: {entry.url} - {type(exc).__name__}: {exc}")
        threading.Thread(target=worker, daemon=True).start()
