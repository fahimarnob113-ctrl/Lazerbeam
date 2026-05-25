# Lazerbeam

Lazerbeam is a Windows desktop app for saving Reddit and GitHub links into an Obsidian vault as organized Markdown notes.

## Prototype Status

This repository is in early prototype setup. The current focus is the core capture pipeline:

```text
URL -> provider -> organizer -> template -> Obsidian writer
```

## Run

```powershell
.\scripts\run_app.cmd
```

## Test

```powershell
.\scripts\run_tests.cmd
```

## First-Time Local Setup

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Test Vault

Use a disposable test vault while developing:

```text
test-vault/
  reddit-notes/
  reddit-media/
  github-notes/
  lazerbeam-inbox/
```

## Package Later

```powershell
pyinstaller --onefile --windowed --name Lazerbeam app.py
```
