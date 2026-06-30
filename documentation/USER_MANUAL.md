# User Manual — Automated File Organizer

## 1. Introduction

Welcome to **Automated File Organizer**.

This application helps users automatically organize files into categorized folders, making file management faster, cleaner, and more efficient. The software provides an easy-to-use graphical interface for organizing files, viewing statistics, and monitoring activity logs.

---

## 2. System Requirements

- Python 3.8 or higher
- Windows, Linux, or macOS
- Minimum 4 GB RAM recommended
- Standard Python installation with Tkinter support

No external libraries are required.

---

## 3. Launching the Application

1. Open the project folder.
2. Open a terminal or command prompt.
3. Run the following command:

```bash
python main.py
```

The application will open on the **Dashboard** page.

---

## 4. Application Modules

### 4.1 Dashboard

The Dashboard provides an overview of the application, including:

- Total organization activities
- Recently organized files
- Quick statistics
- System status information

---

### 4.2 Organizer

The Organizer is the main feature of the application.

#### Steps to Organize Files

1. Navigate to the **Organizer** page.
2. Click **Browse Folder**.
3. Select the folder you want to organize.
4. Verify the selected folder path.
5. Click **Organize Now**.
6. Wait for the process to complete.
7. Review the organization summary.

The application automatically creates category folders when required.

#### Supported Categories

| Category | Example File Types |
|-----------|-------------------|
| Images | .jpg, .png, .gif |
| Documents | .pdf, .docx, .txt |
| Videos | .mp4, .mkv, .avi |
| Audio | .mp3, .wav |
| Archives | .zip, .rar |
| Others | Unrecognized file types |

---

### 4.3 Statistics

The Statistics page displays:

- Total files processed
- Total files organized
- Number of folders created
- Error count
- Previous organization records
- Overall activity summary

This section helps users monitor organization performance over time.

---

### 4.4 Logs

The Logs page displays detailed activity records stored in:

```text
logs/organizer.log
```

Available actions:

- Refresh Logs
- View recent activities
- Clear log records (with confirmation)

Each log entry contains information about file operations and system events.

---

### 4.5 About

The About page provides:

- Project information
- Technology details
- Application version
- Developer information

---

## 5. Data Storage

The application automatically stores data in the following files:

### History Data

```text
data/history.json
```

Stores records of previous organization sessions.

### Settings Data

```text
data/settings.json
```

Stores user preferences and the last selected folder.

### Activity Logs

```text
logs/organizer.log
```

Stores operation logs and error information.

---

## 6. File Organization Process

When the organization process starts:

1. The selected folder is scanned.
2. Each file is analyzed based on its extension.
3. The appropriate category folder is identified.
4. Missing folders are created automatically.
5. Files are moved into their respective folders.
6. History and logs are updated.
7. Statistics are refreshed.

Duplicate filenames are automatically renamed to prevent overwriting existing files.

Example:

```text
report.pdf
report (1).pdf
report (2).pdf
```

---

## 7. Troubleshooting

| Problem | Solution |
|----------|----------|
| Invalid folder selected | Choose an existing folder. |
| Folder contains no files | Select a folder with files to organize. |
| Permission denied | Run the application with appropriate access permissions. |
| Files are not moving | Verify that files are not being used by another application. |
| Application does not start | Ensure Python 3.8+ and Tkinter are installed correctly. |
| Log file is empty | Perform an organization task and refresh the Logs page. |

---

## 8. Best Practices

- Organize folders regularly.
- Review logs after large operations.
- Keep backup copies of important files.
- Verify selected folders before starting organization.
- Avoid organizing system directories.

---

## 9. Support

For technical details and project architecture, refer to:

```text
documentation/PROJECT_DOC.md
```

---

## 10. Conclusion

Automated File Organizer provides a simple and efficient way to manage files through automated categorization, activity tracking, and statistical reporting. The application is designed to improve productivity while maintaining a clean and organized file system.
....