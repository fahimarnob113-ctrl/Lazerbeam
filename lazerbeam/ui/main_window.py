from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

from lazerbeam import __version__
from lazerbeam.capture_pipeline import capture_url
from lazerbeam.config import AppConfig, load_config, save_config
from lazerbeam.logging_setup import configure_logging
from lazerbeam.profiles import BUILT_IN_PROFILES
from lazerbeam.url_utils import clean_url, parse_urls


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
    app.geometry("760x520")

    vault_var = ctk.StringVar(value=config.vault_path)
    profile_var = ctk.StringVar(value="Research")
    mode_var = ctk.StringVar(value=config.organization_mode)
    url_box = ctk.CTkTextbox(app, height=120)
    status_box = ctk.CTkTextbox(app, height=180)

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

    ctk.CTkLabel(app, text=f"Lazerbeam {__version__}", font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=20, pady=(18, 6))
    ctk.CTkButton(app, text="Choose Vault", command=choose_vault).pack(anchor="w", padx=20)
    ctk.CTkLabel(app, textvariable=vault_var).pack(anchor="w", padx=20, pady=(4, 12))
    ctk.CTkLabel(app, text="URLs").pack(anchor="w", padx=20)
    url_box.pack(fill="x", padx=20, pady=(4, 12))
    profile_row = ctk.CTkFrame(app)
    profile_row.pack(fill="x", padx=20, pady=(0, 12))
    ctk.CTkOptionMenu(profile_row, variable=profile_var, values=list(BUILT_IN_PROFILES)).pack(side="left")
    ctk.CTkOptionMenu(profile_row, variable=mode_var, values=["auto", "inbox", "source", "manual"]).pack(side="left", padx=10)
    ctk.CTkButton(profile_row, text="Capture", command=capture).pack(side="right")
    ctk.CTkLabel(app, text="Status").pack(anchor="w", padx=20)
    status_box.pack(fill="both", expand=True, padx=20, pady=(4, 20))

    app.mainloop()
