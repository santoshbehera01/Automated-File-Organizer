# 📂 Automated File Organizer

**Smart Desktop File Management System** — a modern Python + Tkinter desktop app
that organizes any folder into clean, categorized subfolders with one click.

---

## Overview

Tired of cluttered Downloads folders? Automated File Organizer scans a folder
you choose and sorts every file into the right category (Images, Documents,
Videos, Audio, Archives, or Others) — automatically creating the destination
folders, handling duplicate filenames, and keeping a full activity log.

It ships with a unique, modern UI built entirely with the Python standard
library — no third-party packages, no setup headaches.

## ✨ Features

- One-click automatic organization by file type
- Modern multi-page UI: Dashboard, Organizer, Statistics, Logs, About
- Dashboard cards with live counters
- Run history persisted to `data/history.json`
- Detailed activity log at `logs/organizer.log`
- Duplicate-safe moves (auto-renames conflicting files)
- User-friendly error dialogs for permission / empty-folder / invalid-folder cases
- Remembers the last folder you organized

## 🛠 Technologies Used

- Python 3 (3.8+)
- Tkinter / ttk (standard library)
- `json` for history & settings
- `logging` for the activity log
- `pathlib` and `shutil` for safe file operations

## 📁 Folder Structure

```
Automated-File-Organizer/
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
├── assets/
│   └── icons/
├── data/
│   ├── history.json
│   └── settings.json
├── logs/
│   └── organizer.log
├── documentation/
│   ├── PROJECT_DOC.md
│   └── USER_MANUAL.md
└── screenshots/
    ├── dashboard.png
    ├── organizer.png
    ├── statistics.png
    ├── logs.png
    └── report.png
```

## 🚀 Installation

1. Make sure Python 3.8+ is installed.
2. Clone or download this repository.
3. (Optional) Create a virtual environment.
4. No `pip install` step required — the app uses the standard library only.

## ▶️ Usage

From the project root:

```bash
python main.py
```

Then:

1. Click **Organizer** in the top navigation.
2. Click **Browse Folder** and pick the folder to clean.
3. Click **Organize Now**.
4. Review the run summary, then check **Statistics** or **Logs** for details.

## 🖼 Screenshots

| Page | Preview |
| ---- | ------- |
| Dashboard  | `screenshots/dashboard.png`  |
| Organizer  | `screenshots/organizer.png`  |
| Statistics | `screenshots/statistics.png` |
| Logs       | `screenshots/logs.png`       |
| Report     | `screenshots/report.png`     |

## 🔮 Future Enhancements

- Drag-and-drop folder selection
- Custom user-defined categories and rules
- Scheduled automatic runs (background daemon)
- Undo last run
- Export reports to CSV / PDF
- Light theme toggle

## 👤 Author

Built with care using only Python's standard library.

- Developer: *Your Name*
- Email: developer@example.com
- License: MIT