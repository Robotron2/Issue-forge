# Issue Publishing Pipeline

A robust, production-quality Python pipeline that transforms GitHub issue Markdown files into a repeatable structured issue publishing system using YAML as the ultimate source of truth.

## Folder Structure

```text
issue-generator/
├── issues/          # The single source of truth: YAML configurations.
├── original/        # Folder for legacy markdown files for migration.
├── generated/       # Rendered markdown files for user review.
├── templates/       # Jinja2 templates (e.g. `issue.md.j2`).
├── scripts/         # Pipeline scripts (migrate, generate, validate, publish).
├── config.yml       # Repository configuration.
├── published.json   # State tracking for previously published issues.
└── requirements.txt # Python dependencies.
```

## Requirements

- Python 3.12+
- GitHub CLI (`gh`)

## Features

- **Automated Migration**: Converts legacy markdown to highly structured YAML configurations.
- **Smart Resumption & Idempotency**: Automatically tracks successfully published issues in `published.json`. Re-running the script will detect where you left off and completely skip already published issues.
- **Graceful Error Handling**: Safely aborts if you interrupt the publish prompt (Ctrl+C) without throwing ugly Python tracebacks, saving your exact state.
- **Rich Publishing Summary**: Displays a clean summary of newly published, interactively skipped, and automatically skipped issues after every run.
- **Dry-Run Mode**: Safely simulate publish runs before pushing to GitHub.

## 1. Installation

We recommend using a virtual environment to keep your dependencies isolated. You can use standard `pip` (which is what we used) or `uv` as a faster alternative.

**Option A: Using Standard venv + pip (What we used)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Option B: Using `uv` (Faster alternative)**
If you have [uv](https://github.com/astral-sh/uv) installed, you can set it up instantly:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 2. GitHub CLI Setup & Authentication

This pipeline uses the [GitHub CLI](https://cli.github.com/) to publish issues.

If you don't have it installed:
- **macOS:** `brew install gh`
- **Linux:** Follow the [official instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md).
- **Windows:** `winget install --id GitHub.cli`

Authenticate the CLI:

```bash
gh auth login
```
Follow the interactive prompts to authorize with your GitHub account.

## 3. Migration

Place all your existing markdown issues inside the `original/` directory.

Run the migration script to convert these legacy markdown documents into structured YAML files. **Note: It will fail loudly if the original markdown doesn't match the strict expectations.**

```bash
python scripts/migrate.py
```
This generates `issues/*.yml` which now serves as the **Single Source of Truth**. The original markdown is never edited again.

## 4. Validation (Optional but Recommended)

Check your YAML files to ensure all required fields are present, IDs/branches are unique, and references are sound:

```bash
python scripts/validate.py
```

## 5. Generation

Generate markdown from the structured YAML files for human review:

```bash
python scripts/generate.py
```

## 6. Review

Check the output files generated inside `generated/`. They should closely resemble the original markdown files. *Do not edit these files directly; any corrections should be made in `issues/*.yml`.*

## 7. Publishing

Set up your `config.yml` at the root of the project:

```yaml
owner: my-org
repo: my-repo
```
*(Alternatively, you can provide an `.env` file with `OWNER` and `REPO` variables).*

Publish all un-published issues (it checks `published.json` to avoid duplicates):

```bash
python scripts/publish.py
```
It will prompt you for confirmation before each issue, displaying the ID, Title, and Repository.

### Useful Publishing Flags

**Dry Run:**
To see what commands would run without actually creating issues:
```bash
python scripts/publish.py --dry-run
```

**Specific Issue:**
To publish only a specific issue (e.g. issue 7):
```bash
python scripts/publish.py --issue 7
```

**Range Publishing:**
To publish issues within a range (e.g. 7 through 12):
```bash
python scripts/publish.py --range 7-12
```

**Skip Confirmation:**
Run completely unattended by skipping the interactive `y/n` prompts. Combines perfectly with Smart Resumption to pick up right where you left off:
```bash
python scripts/publish.py --yes
# or
python scripts/publish.py -y
```

## 8. Troubleshooting

- **"No such file or directory: original/":** Make sure you've placed the original markdown files in the `original/` folder before running migration.
- **Migration Fails Loudly:** Ensure your legacy Markdown exactly matches the `# Issue #<ID> — <type>: <title>` header structure, and contains all required sections (`Description`, `Requirements & Context`, `Acceptance Criteria`).
- **"GitHub CLI not found":** Ensure `gh` is installed and accessible in your system's PATH.
- **"Failed to publish":** Ensure your `gh auth status` shows you are logged in and have access rights to the target repository configured in `config.yml`.
