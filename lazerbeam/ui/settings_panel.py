import customtkinter as ctk
from lazerbeam.config import AppConfig, save_config

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, master, config: AppConfig):
        super().__init__(master)
        self.config = config

        ctk.CTkLabel(self, text="Settings", font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=20, pady=(20, 10))

        ctk.CTkLabel(self, text="Duplicate Strategy:").pack(anchor="w", padx=20, pady=(10, 0))
        self.dup_var = ctk.StringVar(value=self.config.duplicate_strategy)
        ctk.CTkOptionMenu(self, variable=self.dup_var, values=["append", "overwrite", "skip"], command=self.save).pack(anchor="w", padx=20, pady=(5, 10))

        ctk.CTkLabel(self, text="Manual Inbox Folder:").pack(anchor="w", padx=20, pady=(10, 0))
        self.folder_var = ctk.StringVar(value=self.config.manual_folder)
        entry = ctk.CTkEntry(self, textvariable=self.folder_var, width=300)
        entry.pack(anchor="w", padx=20, pady=(5, 10))
        entry.bind("<KeyRelease>", lambda e: self.save())

        self.debug_var = ctk.BooleanVar(value=self.config.debug)
        ctk.CTkSwitch(self, text="Debug Logging", variable=self.debug_var, command=self.save).pack(anchor="w", padx=20, pady=(20, 10))

    def save(self, *args):
        self.config.duplicate_strategy = self.dup_var.get()
        self.config.manual_folder = self.folder_var.get()
        self.config.debug = self.debug_var.get()
        save_config(self.config)
