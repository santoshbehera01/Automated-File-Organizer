# Project Documentation — Automated File Organizer

## 1. Project Overview

**Automated File Organizer** is a desktop application developed using Python and Tkinter that automatically organizes files into categorized folders based on their file extensions. The application helps users maintain a clean and structured directory by reducing manual file management tasks.

The project demonstrates practical concepts of file handling, GUI development, logging, data persistence, and software design using only Python's standard library.

---

## 2. Objectives

- Automate file organization and folder management.
- Improve productivity by reducing manual sorting efforts.
- Provide a simple and user-friendly desktop interface.
- Maintain organization history and activity logs.
- Demonstrate clean, modular, and maintainable Python development.

---

## 3. System Architecture

The application follows a layered architecture consisting of presentation, processing, and storage components.

```text
┌──────────────────────────────────────────────┐
│                User Interface                │
│      Dashboard • Organizer • Statistics      │
│             Logs • About Pages               │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│             Processing Layer                 │
│  File Classification • Validation • Sorting │
│  Statistics Generation • Logging Management │
└──────────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────┐
│               Data Storage                   │
│ history.json • settings.json • organizer.log│
└──────────────────────────────────────────────┘
```

---

## 4. Core Features

| Feature | Description |
|----------|-------------|
| Dashboard | Displays organization statistics and activity summary |
| File Organizer | Automatically sorts files into categorized folders |
| Statistics | Shows organization insights and file distribution |
| Activity Logs | Maintains detailed operation logs |
| History Tracking | Stores previous organization records |
| Duplicate Handling | Prevents file overwriting through auto-renaming |
| Settings Storage | Remembers user preferences and last used folder |
| Error Handling | Gracefully handles invalid folders and file errors |

---

## 5. Working Procedure

1. Launch the application using `python main.py`.
2. Navigate to the **Organizer** page.
3. Select the target folder using the file browser.
4. Click **Organize Now**.
5. The application scans all files in the selected directory.
6. Files are categorized according to their extensions.
7. Category folders are created automatically if they do not exist.
8. Files are moved safely to their respective folders.
9. Activity logs and organization history are updated.
10. Dashboard and Statistics pages reflect the latest results.

---

## 6. Data Management

### History Storage

```text
data/history.json
```

Stores records of previous organization operations.

### Settings Storage

```text
data/settings.json
```

Stores application preferences and recently used folder information.

### Activity Logs

```text
logs/organizer.log
```

Maintains detailed logs of file movement and system events.

---

## 7. Technologies Used

| Component | Technology |
|-----------|------------|
| Programming Language | Python 3 |
| GUI Framework | Tkinter |
| Data Storage | JSON |
| Logging | Python logging module |
| File Management | pathlib, shutil, os |
| Date & Time | datetime |
| IDE | Visual Studio Code |
| Version Control | Git & GitHub |

---

## 8. Error Handling

The application includes robust exception handling mechanisms:

- Invalid folder selection detection
- Empty folder validation
- File permission error handling
- Duplicate filename resolution
- File movement failure recovery
- JSON read/write exception handling
- User-friendly error messages through dialog boxes

---

## 9. Future Enhancements

- Drag-and-drop folder selection
- Custom file organization rules
- Scheduled automatic organization
- Undo last organization operation
- CSV and PDF report generation
- Dark and Light theme switching
- Advanced file filtering options

---

## 10. Conclusion

The Automated File Organizer successfully demonstrates the use of Python for building a practical desktop productivity application. Through automated file classification, persistent storage, logging, and an intuitive graphical interface, the project provides an efficient solution for managing unorganized directories while showcasing key software engineering concepts and best practices.