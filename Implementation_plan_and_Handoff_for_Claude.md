# Lazerbeam: App DNA & Handoff Plan

This document serves as the master blueprint and handoff document for the **Lazerbeam** project. It outlines the core identity, technical architecture (App DNA), and the step-by-step phased execution plan required to build the prototype and beyond.

## 🧬 App DNA

### Core Vision
**Lazerbeam** is a desktop "save anything into Obsidian" tool. Users paste a link from Reddit, GitHub, Hacker News, or other platforms, and Lazerbeam automatically turns it into clean, local-first Obsidian notes with media, metadata, backlinks, and sensible folder structures.

### Key Architectural Decisions
- **Provider Interface Architecture**: To support unlimited future platforms, parsing logic is never hardcoded into the GUI. The app uses a pluggable `SourceProvider` system.
- **Obsidian-Native Output**: Notes are built specifically for Obsidian, including YAML frontmatter, Dataview compatibility, custom templates, and Daily Note backlinks.
- **Reliability First**: Image/comment limits are enforced to prevent massive downloads. The app will overwrite existing notes with new captures to ensure the information is always up to date.

### Tech Stack
- **Language**: Python
- **GUI Framework**: Explore more UI preferences (e.g., PyQt, Flet, Textual, Electron, or Tauri) instead of defaulting to CustomTkinter, to determine the best fit for the aesthetic and functionality.
- **Packaging**: PyInstaller (Standalone `.exe`)

### Core Flow Pipeline
`URL Input (or Queue) -> Clean URLs -> Duplicate Check -> Source Provider Detection -> Fetch Content -> Normalize to CapturedItem -> Apply Capture Profile -> Download Media -> Render Markdown Template -> Write to Obsidian Vault -> Update History -> (Optional) Backlink to Daily Note`

### Core Data Models
1. **CapturedItem**: A standardized format that every provider returns.
   `source | title | author | url | body | created_at | captured_at | comments | media | metadata | tags`
2. **CaptureProfile**: Controls what gets saved during a capture.
   `name | include_media | include_comments | max_images | max_comments | save_mode | append_daily_note`
3. **CaptureHistoryEntry**: Tracks previous captures to avoid/manage duplicates.
   `url | cleaned_url | source | title | note_path | captured_at | status`

### Project Structure Foundation
```text
Lazerbeam/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── app.py
├── lazerbeam/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── url_utils.py
│   ├── capture_pipeline.py
│   ├── obsidian_writer.py
│   ├── media_downloader.py
│   ├── markdown_cleaner.py
│   ├── history.py
│   ├── templates.py
│   ├── profiles.py
│   └── daily_notes.py
├── sources/
│   ├── __init__.py
│   ├── base.py
│   ├── reddit.py
│   └── github.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── settings_panel.py
│   ├── history_panel.py
│   └── queue_panel.py
├── templates/
│   ├── reddit-post.md
│   ├── github-repo.md
│   ├── github-section.md
│   └── generic-capture.md
├── tests/
│   └── (test files...)
└── scripts/
    └── build_exe.ps1
```

---

## 🚀 Build Phases Roadmap

> [!NOTE]
> **Progress Update**
> Progress currently strictly follows the `Lazerbeam Build session with Codex.md` document. Some initial groundwork (project structure, foundation) has been explored and documented in Codex.

### Phase 0: GitHub-Ready Foundation
*Set up the app like a real open-source project immediately.*
- Create project structure and subdirectories.
- Create `README.md`, `requirements.txt`, `.gitignore`.
- Set up basic test files and main `app.py` entry point.
- Create separate GitHub workflows/Actions for: debug, reporting, update proposal, and documentation.

### Phase 1: Core App Shell
*Build the desktop GUI.*
- Base window configuration (framework to be decided after exploring UI preferences).
- Vault folder selector.
- URL/queue input text box.
- Capture profile dropdown.
- Download/Capture button.
- Status/progress log text area.
- Configuration persistence (remembering the vault path).

### Phase 2: Shared Capture Engine
*Build the "spine" of the app.*
- URL cleaning logic (removing trackers, anchors).
- Source detection routing.
- Define `CapturedItem` model.
- Base provider interface (`SourceProvider`).
- Queue processing logic.
- Duplicate detection and history storage (Behavior: overwrite existing notes).

### Phase 3: Obsidian Writer
*Handle local file creation.*
- Safe filename sanitization.
- Folder structure creation.
- Overwrite mode for existing files.
- Frontmatter generator.
- Template renderer (Jinja2 or custom string templating).
- Optional daily note backlink appending.

### Phase 4: GitHub Provider
*Extract Markdown from repositories.*
- Detect repo URLs.
- Fetch `README.md` and docs Markdown.
- Split content by headings.
- Create nested folders from heading hierarchy.
- Resolve relative image URLs to raw GitHub URLs.
- Download images to `_images` folder.
- Create "Repo Index" note linking all captured files.

### Phase 5: Reddit Provider
*Extract posts, comments, and media.*
- Post capture (title, body, author, score).
- Handle subreddit-aware folder routing.
- Apply comment limits and fetch top-level comments.
- Apply media limits and download images/videos.
- (Wiki and megathread support added later).

### Phase 6: Reliability + UX
*Make the prototype pleasant to use.*
- Multithreaded/background capture to keep UI responsive.
- Stop/cancel button.
- Capture history panel with re-run capability.
- Settings panel for limits and preferences.
- Better error handling and failed capture recovery.

### Phase 7: Packaging
*Create the distributable artifact.*
- Add app icon.
- Configure PyInstaller.
- Add system tray support (minimize to tray).
- Build standalone Windows `.exe`.

### Phase 8: Visual Redesign
*Upgrade the UI aesthetics.*
- Implement dark mode and glassmorphism (depending on chosen UI framework).
- Create a bento-style dashboard layout.
- Add neon accents and micro-interactions.

### Phase 9: More Sources
*Expand platform support.*
- Hacker News provider.
- Generic webpage/article capture.
- Twitter/X, Threads, and Instagram providers.

### Phase 10: Browser Extensions
*Seamless capture from the browser.*
- Create a local capture server in the desktop app (`http://127.0.0.1:28777/capture`).
- Build Chrome and Firefox extensions.
- Enable sending current URL, selected text, or page title directly to Lazerbeam.
