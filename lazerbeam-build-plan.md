# Lazerbeam Build Plan

## What Lazerbeam Is

Lazerbeam is a Windows desktop app that saves online content into an Obsidian vault.

The basic flow:

```text
Paste link
-> Lazerbeam understands the source
-> Lazerbeam fetches the content
-> Lazerbeam organizes it
-> Lazerbeam saves clean Markdown notes into Obsidian
```

The first supported sources should be:

- GitHub
- Reddit

Later sources:

- Hacker News
- normal websites/articles
- Twitter/X
- Threads
- Instagram

## Core Principle

The user should not need to manually decide where everything goes.

Lazerbeam should automatically understand:

- what kind of link was pasted
- what content type it is
- where the note should be saved
- what the note should be called
- where media should go
- what tags/frontmatter should be added
- whether it belongs in an index note or daily note

The ideal user experience:

```text
Paste link.
Click capture.
Done.
```

## Important Note About The Browser URL

The URL below is for a future browser extension/local server feature:

```text
http://127.0.0.1:28777/capture
```

It will show "site can't be reached" until the desktop app has a local capture server.

That should be built later, not at the start.

## Recommended Project Structure

```text
Lazerbeam/
  README.md
  CHANGELOG.md
  LICENSE
  requirements.txt
  .gitignore
  app.py

  lazerbeam/
    __init__.py
    config.py
    models.py
    url_utils.py
    capture_pipeline.py
    organizer.py
    obsidian_writer.py
    media_downloader.py
    markdown_cleaner.py
    history.py
    templates.py
    profiles.py
    daily_notes.py
    logging_setup.py

    sources/
      __init__.py
      base.py
      github.py
      reddit.py

    ui/
      __init__.py
      main_window.py
      settings_panel.py
      history_panel.py
      queue_panel.py

  templates/
    reddit-post.md
    github-repo.md
    github-section.md
    generic-capture.md

  tests/
    fixtures/
    golden/
    test_url_utils.py
    test_markdown_cleaner.py
    test_obsidian_writer.py
    test_history.py
    test_templates.py
    test_organizer.py
    test_github_heading_splitter.py

  docs/
    release-checklist.md
    regression-urls.md
    adr/

  scripts/
    build_exe.ps1
```

## Main App Flow

```text
URL or URL list
-> queue parser
-> clean URLs
-> duplicate check
-> detect source provider
-> fetch content
-> normalize into CapturedItem
-> automatic organizer decides where things go
-> apply capture profile
-> download media
-> render Markdown template
-> write note to Obsidian
-> update history
-> optionally backlink daily note
```

## Main Data Models

### CapturedItem

Represents captured content before it is written to Obsidian.

```text
source
title
author
url
body
created_at
captured_at
comments
media
metadata
tags
```

### OutputPlan

Created by the automatic organizer.

```text
note_path
media_folder
index_note_path
daily_note_path
tags
naming_strategy
duplicate_strategy
```

### CaptureProfile

Controls how much content to save.

```text
name
include_media
include_comments
max_images
max_comments
save_mode
append_daily_note
```

### CaptureHistoryEntry

Used for history and duplicate detection.

```text
url
cleaned_url
source
title
note_path
captured_at
status
```

## Automatic Organization

Add a module:

```text
lazerbeam/organizer.py
```

Its job is to decide where captured content belongs.

### Reddit Organization

Use subreddit first.

```text
Vault/
  reddit-notes/
    Obsidian/
      Post Title.md
```

Megathreads:

```text
Vault/
  reddit-notes/
    Obsidian/
      megathreads/
        Post Title.md
```

Media:

```text
Vault/
  reddit-media/
    Obsidian/
      image.jpg
```

Tags:

```yaml
tags:
  - lazerbeam
  - reddit
  - reddit/Obsidian
```

### GitHub Organization

Use owner and repo.

```text
Vault/
  github-notes/
    owner/
      repo-name/
        repo-name - Index.md
        README.md
        Installation.md
        Usage.md
        _images/
```

Tags:

```yaml
tags:
  - lazerbeam
  - github
  - repo/owner/repo-name
```

### Future Web Organization

Use domain.

```text
Vault/
  web-notes/
    example.com/
      Article Title.md
```

## Organization Modes

### Auto Mode

Default mode.

Lazerbeam decides folders, filenames, tags, and media locations automatically.

### Inbox Mode

Everything goes into:

```text
Vault/
  lazerbeam-inbox/
```

Good for fast saving.

### Manual Mode

The user chooses the target folder while Lazerbeam still helps with filenames, frontmatter, tags, and media embeds.

This option stays available even though Auto Mode is the default.

### Source Mode

Organize by platform:

```text
reddit-notes/
github-notes/
web-notes/
```

### Topic Mode

Future mode.

Organize by topic, such as:

```text
AI/
Programming/
Obsidian/
Research/
```

This can use metadata, tags, or AI later.

## Capture Profiles

Start with four profiles.

### Research

Save:

- body
- metadata
- comments
- media

### Lightweight

Save:

- title
- source link
- body

### Archive

Save as much as possible within limits.

### Media Only

Save media and create a small index note.

## Core Features To Include Early

- GitHub support from the beginning
- Reddit support from the beginning
- automatic organization
- frontmatter
- templates
- capture history
- duplicate detection
- queue mode for multiple URLs
- capture profiles
- GitHub repo index note
- optional daily note backlink
- debug logs
- dry run / preview mode
- failed capture reports

## Build Phases

### Phase 0: Foundation

Goal: make the project organized from day one.

Build:

- project structure
- Git repository
- README
- requirements file
- gitignore
- config system
- logging system
- basic tests

Done when:

- the app can start
- tests can run
- config can be saved and loaded
- logs are written

### Phase 1: Basic App Window

Goal: create a simple desktop app shell.

Build:

- CustomTkinter window
- vault folder picker
- URL input
- capture button
- status log
- capture profile dropdown

Done when:

- user can select a vault
- user can paste a URL
- user can click capture
- app shows status messages

### Phase 2: Capture Engine

Goal: create the brain of the app.

Build:

- URL cleaner
- source detector
- CapturedItem model
- provider interface
- queue processor
- duplicate checker
- history writer

Done when:

- a URL can move through the pipeline using fake/sample provider data

### Phase 3: Automatic Organizer

Goal: make Lazerbeam decide where content belongs.

Build:

- organizer module
- folder rules
- filename rules
- tag rules
- media folder rules
- duplicate behavior rules

Done when:

- captured items get a clear output plan before being written

### Phase 4: Obsidian Writer

Goal: save clean notes safely.

Build:

- safe filename creation
- folder creation
- append-only writing
- frontmatter generation
- template rendering
- Obsidian image embeds
- optional daily note backlink

Done when:

- sample captures create valid Obsidian notes
- existing notes are appended, not overwritten
- images use `![[filename.jpg]]`

### Phase 5: GitHub Provider

Goal: turn GitHub repos into organized notes.

Build:

- GitHub URL detection
- repo metadata capture
- README capture
- docs Markdown capture
- heading-based splitting
- nested folders from headings
- relative image URL resolution
- image downloads into `_images`
- repo index note

Done when:

- a GitHub repo becomes an organized folder of Obsidian notes
- the index note links generated notes
- images render in Obsidian

### Phase 6: Reddit Provider

Goal: turn Reddit posts into useful notes.

Build:

- Reddit post detection
- query and anchor cleaning
- title/body/author/score capture
- comment capture
- comment limits
- media download
- subreddit folders
- one note per post

Done when:

- a Reddit post creates one complete note
- comments and media obey profile settings
- duplicate captures append safely

### Phase 7: Reliability And Debugging

Goal: make problems easy to understand.

Build:

- debug mode
- log file
- failed capture reports
- dry run mode
- retry failed capture
- cancel button
- graceful network errors

Done when:

- invalid, private, deleted, or broken URLs do not crash the app
- failures leave useful logs or reports

### Phase 8: UX And History

Goal: make repeated use comfortable.

Build:

- history panel
- re-run button
- queue panel
- settings panel
- duplicate action selector
- capture profile editor
- open output folder/note button

Done when:

- user can manage previous captures from the app

### Phase 9: Packaging

Goal: ship a real Windows app.

Build:

- app icon
- PyInstaller build script
- packaged `.exe`
- tray support
- portable config behavior
- release folder cleanup

Done when:

- the `.exe` works on Windows without Python

### Phase 10: Visual Redesign

Goal: make the app feel polished.

Build:

- dark mode polish
- bento layout
- glassy panels
- neon accents
- smooth interactions
- empty states
- loading states

Done when:

- the app feels finished without slowing down the workflow

### Phase 11: More Sources

Goal: expand capture support.

Add sources in this order:

1. Hacker News
2. generic webpages/articles
3. Twitter/X
4. Threads
5. Instagram

Rule:

Every new source must use the provider interface.

### Phase 12: Browser Extensions

Goal: capture directly from the browser.

Build:

- desktop local server
- `POST /capture`
- Chrome extension
- Firefox extension
- selected text capture
- current page capture
- capture status response

Only in this phase should this URL work:

```text
http://127.0.0.1:28777/capture
```

## Testing Plan

### Unit Tests

Test small parts:

- URL cleaning
- source detection
- filename cleaning
- Markdown cleaning
- template rendering
- history
- organizer rules
- Obsidian writer

### Fixture Tests

Use local sample files instead of live internet.

```text
tests/
  fixtures/
    reddit_post.json
    reddit_comments.json
    github_readme.md
    github_docs_page.md
    github_repo_tree.json
```

### Golden Markdown Tests

Compare generated Markdown to expected Markdown.

```text
tests/
  golden/
    reddit_post_expected.md
    github_repo_index_expected.md
    github_section_expected.md
```

Use this to catch accidental output changes.

### Test Vault

Use a fake Obsidian vault while developing.

```text
test-vault/
  reddit-notes/
  reddit-media/
  github-notes/
  lazerbeam-inbox/
```

Do not test new code on a real vault first.

## Debug Workflow

When something breaks, check the pipeline in order:

```text
URL cleaning
-> source detection
-> fetching content
-> media download
-> organization
-> template rendering
-> file writing
```

Logs should go here:

```text
logs/lazerbeam.log
```

Failed captures should create reports here:

```text
Vault/
  lazerbeam-failures/
```

Failure reports should include:

- original URL
- cleaned URL
- source
- capture profile
- error message
- time
- possible note path

## Daily Build Routine

Use this loop:

```text
Pick one small feature
-> write or update tests
-> build the feature
-> run tests
-> test with fake vault
-> inspect generated Markdown
-> check logs
-> commit
```

## Commit Rules

Use small clear commits.

Good examples:

```text
Add provider interface and captured item model
Implement automatic organizer rules
Add append-only Obsidian writer
Add GitHub README fixture tests
Support Reddit post URL cleaning
Add capture history duplicate detection
```

Avoid vague commits:

```text
updates
fix stuff
big changes
```

## Release Checklist

Before release:

- tests pass
- manual QA is complete
- packaged `.exe` is tested
- README is updated
- CHANGELOG is updated
- known issues are listed
- screenshots are updated
- release notes are written

## Decision Rules

When unsure where something belongs:

- Reddit-specific logic goes in the Reddit provider
- GitHub-specific logic goes in the GitHub provider
- saving notes goes in the Obsidian writer
- folder and naming decisions go in the organizer
- URL cleanup goes in URL utilities
- buttons and panels go in the UI
- shared app workflow goes in the capture pipeline
- unfinished features should use feature flags

## Most Important Technical Rule

Do not put everything inside the GUI file.

The app should be shaped like this:

```text
UI
-> Capture Engine
-> Source Provider
-> Organizer
-> Template Renderer
-> Obsidian Writer
```

This keeps the app easy to grow.
