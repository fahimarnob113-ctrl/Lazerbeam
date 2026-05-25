# Lazerbeam

Lazerbeam is a Windows desktop app for saving Reddit and GitHub links into an Obsidian vault as organized Markdown notes.

## Prototype Status

This repository is in early prototype setup. The current focus is the core capture pipeline:

```text
URL -> provider -> organizer -> template -> Obsidian writer
```

## Run

```powershell
python app.py
```

## Test

```powershell
python -m unittest discover -s tests
```

## Package Later

```powershell
pyinstaller --onefile --windowed --name Lazerbeam app.py
```
