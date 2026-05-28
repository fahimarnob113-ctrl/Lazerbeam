from __future__ import annotations

import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from lazerbeam import __version__
from lazerbeam.capture_pipeline import capture_url
from lazerbeam.config import AppConfig, load_config, save_config
from lazerbeam.logging_setup import configure_logging
from lazerbeam.profiles import BUILT_IN_PROFILES
from lazerbeam.url_utils import clean_url, parse_urls

from lazerbeam.ui.settings_panel import SettingsPanel
from lazerbeam.ui.history_panel import HistoryPanel
from lazerbeam.ui.queue_panel import QueuePanel


def run_app() -> None:
    try:
        import customtkinter as ctk
    except ImportError as exc:
        raise SystemExit("CustomTkinter is not installed. Run: pip install -r requirements.txt") from exc

    config = load_config()
    configure_logging(config.debug)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title(f"Lazerbeam {__version__}")
    app.geometry("860x640")

    vault_var = ctk.StringVar(value=config.vault_path)
    
    # Header
    header = ctk.CTkFrame(app, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(15, 5))
    ctk.CTkLabel(header, text=f"Lazerbeam", font=("Segoe UI", 24, "bold")).pack(side="left")
    
    vault_frame = ctk.CTkFrame(header, fg_color="transparent")
    vault_frame.pack(side="right")
    ctk.CTkLabel(vault_frame, text="Vault: ").pack(side="left")
    ctk.CTkLabel(vault_frame, textvariable=vault_var, width=150, anchor="w").pack(side="left", padx=5)
    
    status_box = ctk.CTkTextbox(app, height=150) # Just a placeholder since it needs to exist for log early on
    
    def log(message: str) -> None:
        status_box.insert("end", message + "\n")
        status_box.see("end")

    def choose_vault() -> None:
        selected = filedialog.askdirectory(title="Select Obsidian Vault")
        if selected:
            vault_var.set(selected)
            config.vault_path = selected
            save_config(config)
            log(f"Vault selected: {selected}")
            
    ctk.CTkButton(vault_frame, text="Change", width=60, command=choose_vault).pack(side="left")

    # Tabs
    tabview = ctk.CTkTabview(app)
    tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    tab_capture = tabview.add("Capture")
    tab_queue = tabview.add("Queue")
    tab_history = tabview.add("History")
    tab_settings = tabview.add("Settings")
    
    # --- Capture Tab ---
    profile_var = ctk.StringVar(value="Research")
    mode_var = ctk.StringVar(value=config.organization_mode)
    
    ctk.CTkLabel(tab_capture, text="Paste URL(s)").pack(anchor="w", padx=20, pady=(10, 0))
    url_box = ctk.CTkTextbox(tab_capture, height=120)
    url_box.pack(fill="x", padx=20, pady=(5, 10))
    
    profile_row = ctk.CTkFrame(tab_capture, fg_color="transparent")
    profile_row.pack(fill="x", padx=20, pady=5)
    ctk.CTkOptionMenu(profile_row, variable=profile_var, values=list(BUILT_IN_PROFILES)).pack(side="left")
    ctk.CTkOptionMenu(profile_row, variable=mode_var, values=["auto", "inbox", "source", "manual"]).pack(side="left", padx=10)
    
    # Reparent status_box properly
    status_box.destroy()
    status_box = ctk.CTkTextbox(tab_capture, height=150)
        
    def capture() -> None:
        config.vault_path = vault_var.get()
        config.organization_mode = mode_var.get()
        save_config(config)
        if not config.vault_path:
            messagebox.showerror("Lazerbeam", "Choose an Obsidian vault first.")
            return
        urls = parse_urls(url_box.get("1.0", "end"))
        if not urls:
            messagebox.showerror("Lazerbeam", "Paste at least one URL.")
            return
        profile = BUILT_IN_PROFILES[profile_var.get()]
        
        capture_btn.configure(state="disabled")
        
        def worker():
            for url in urls:
                try:
                    log(f"Capturing: {url}")
                    log(f"Cleaned URL: {clean_url(url)}")
                    result = capture_url(url, Path(config.vault_path), config, profile)
                    log(f"Saved: {result.output_plan.note_path}")
                    if result.item.media:
                        log(f"Media saved: {len(result.item.media)} file(s) in {result.output_plan.media_folder}")
                except Exception as exc:
                    log(f"Failed: {url} - {type(exc).__name__}: {exc}")
            capture_btn.configure(state="normal")
            
        threading.Thread(target=worker, daemon=True).start()

    capture_btn = ctk.CTkButton(profile_row, text="Capture Now", command=capture)
    capture_btn.pack(side="right")
    
    ctk.CTkLabel(tab_capture, text="Status").pack(anchor="w", padx=20, pady=(10, 0))
    status_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))
    
    # --- Other Tabs ---
    def get_vault_path():
        return vault_var.get()
        
    SettingsPanel(tab_settings, config).pack(fill="both", expand=True)
    
    history_panel = HistoryPanel(tab_history, get_vault_path, config, log)
    history_panel.pack(fill="both", expand=True)
    
    queue_panel = QueuePanel(tab_queue, get_vault_path, config, log)
    queue_panel.pack(fill="both", expand=True)
    
    def on_tab_changed():
        if tabview.get() == "History":
            history_panel.load_history()
            
    tabview.configure(command=on_tab_changed)
    
    try:
        app.iconbitmap("icon.ico")
    except Exception:
        pass
        
    def withdraw_window():
        import pystray
        from PIL import Image
        app.withdraw()
        
        try:
            image = Image.open("icon.ico")
        except FileNotFoundError:
            image = Image.new('RGB', (64, 64), color='blue')
            
        def show_window(icon, item):
            icon.stop()
            app.after(0, app.deiconify)
            
        def quit_window(icon, item):
            icon.stop()
            app.quit()
            
        menu = pystray.Menu(
            pystray.MenuItem('Show', show_window, default=True),
            pystray.MenuItem('Quit', quit_window)
        )
        icon = pystray.Icon("Lazerbeam", image, "Lazerbeam", menu)
        icon.run()

    def on_closing():
        threading.Thread(target=withdraw_window, daemon=True).start()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    
    app.mainloop()
