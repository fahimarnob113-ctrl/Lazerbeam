# Manual QA

Use a test vault before capturing into a real Obsidian vault.

## Test Vault

Create this folder layout locally:

```text
test-vault/
  reddit-notes/
  reddit-media/
  github-notes/
  lazerbeam-inbox/
```

## App Launch

```powershell
.\scripts\run_app.cmd
```

Check:

- the Lazerbeam window opens
- the vault picker works
- the profile dropdown is visible
- the organization mode dropdown includes `auto`, `inbox`, `source`, and `manual`
- status messages appear after a capture attempt

## First Capture Checks

Use the test vault.

GitHub:

- paste a public GitHub repo URL
- capture it
- confirm a note appears under `github-notes`
- confirm the note has YAML frontmatter
- confirm repeated capture appends instead of overwriting

Reddit:

- paste a public Reddit post URL
- capture it
- confirm one note appears under `reddit-notes`
- confirm comments are included for the Research profile
- confirm repeated capture appends instead of overwriting

## Failure Checks

Try:

- an empty URL
- an unsupported URL
- an invalid GitHub URL
- an invalid Reddit URL

The app should show an error in the status panel instead of crashing.
