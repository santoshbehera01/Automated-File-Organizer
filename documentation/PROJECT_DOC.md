# Project Documentation — Automated File Organizer

## 1. Introduction

Automated File Organizer is a desktop application that helps users keep their
folders tidy by automatically sorting files into categorized subfolders. It is
written in Python 3 using only the standard library (Tkinter for the UI), so
it runs out of the box on Windows, macOS, and Linux.

## 2. Objectives

- Eliminate the manual work of sorting files by extension.
- Provide a modern, distraction-free desktop interface.
- Keep a transparent audit trail of every operation.
- Run without third-party dependencies.

## 3. Architecture

The application follows a simple three-layer architecture:

```
┌───────────────────────────────────────────────┐
│            Presentation Layer                 │
│  Tkinter pages: Dashboard / Organizer /       │
│  Statistics / Logs / About                    │
└───────────────────────────────────────────────┘
                  │
┌───────────────────────────────────────────────┐
│            Application Layer                  │
│  organize_folder(), category_for(),           │
│  unique_destination(), aggregate_stats()      │
└───────────────────────────────────────────────┘
                  │
┌───────────────────────────────────────────────┐
│             Persistence Layer                 │
│  data/history.json, data/settings.json,       │
│  logs/organizer.log                           │
└───────────────────────────────────────────────┘
```

All logic lives in a single `main.py` for portability.

## 4. Features

- File classification by extension into six categories.
- Automatic creation of missing destination folders.
- Duplicate-safe moves (`name (1).ext`, `name (2).ext`, …).
- Persistent history (last 100 runs).
- Persistent settings (remembers the last folder).
- Full activity log written through the `logging` module.
- Modern dark UI with top navigation and dashboard cards.

## 5. Workflow

1. User opens the app and navigates to **Organizer**.
2. User selects a folder via the system dialog.
3. User clicks **Organize Now**.
4. `organize_folder()` iterates over every file in the folder:
   - Determines its category using the extension.
   - Ensures the destination subfolder exists.
   - Moves the file with a duplicate-safe filename.
   - Logs the operation.
5. A run summary is stored in `data/history.json` and shown in the UI.

## 6. Technologies

| Concern        | Library / Tool      |
| -------------- | ------------------- |
| UI             | tkinter, ttk        |
| File I/O       | pathlib, shutil, os |
| Persistence    | json                |
| Logging        | logging             |
| Date / Time    | datetime            |

## 7. Error Handling

The app gracefully handles:

- **Invalid folder** — shown via a `messagebox.showerror`.
- **Empty folder** — informational dialog, no operation performed.
- **Permission errors** — caught per file; logged and reported.
- **Duplicate filenames** — destination is auto-renamed to avoid overwriting.
- **Generic file move failures** — caught, logged, and counted as errors.

## 8. Future Enhancements

- Drag-and-drop folder selection.
- Custom user-defined categories.
- Scheduled background runs.
- Undo last run.
- Export reports.
- Light theme.

## 9. Conclusion

Automated File Organizer demonstrates that a polished, useful desktop
application can be built with nothing more than Python's standard library.
It is small, dependency-free, easy to extend, and immediately useful for
anyone who deals with messy folders.