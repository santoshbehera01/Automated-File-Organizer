# User Manual — Automated File Organizer

## 1. Installation

1. Install Python 3.8 or newer from <https://www.python.org/downloads/>.
2. Download or clone this repository.
3. No additional packages are required.

## 2. Launching the App

Open a terminal in the project folder and run:

```bash
python main.py
```

The main window opens with the **Dashboard** page visible.

## 3. Using the Organizer

1. Click **Organizer** in the top navigation bar.
2. Click **Browse Folder** to choose the folder you want to clean.
3. The selected path appears below the folder icon.
4. Click **Organize Now**.
5. Confirm the action in the dialog.
6. When the run finishes, a summary appears in the "Run summary" card.

Files are moved into subfolders named **Images**, **Documents**, **Videos**,
**Audio**, **Archives**, and **Others** — created automatically when needed.
If a file with the same name already exists at the destination, a numeric
suffix (e.g. `report (1).pdf`) is added to avoid overwriting.

## 4. Viewing Statistics

Click **Statistics** in the top navigation to see:

- Total files scanned (all-time)
- Files organized
- Folders created
- Skipped files
- Errors
- Last run timestamp
- A table of every previous run

## 5. Logs

Click **Logs** to view the contents of `logs/organizer.log`. Each entry
contains a timestamp, filename, destination, and status. You can:

- **Refresh** — reload the file from disk.
- **Clear Logs** — wipe the log file (asks for confirmation).

## 6. Troubleshooting

| Problem                                | Solution                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------ |
| "Please select a valid folder"         | The path no longer exists — pick a new folder.                           |
| "You do not have permission…"          | Run the app as a user that can read/write the target folder.             |
| "The selected folder has no files…"    | Pick a folder that actually contains files (subfolders are ignored).     |
| The window looks too small             | Drag the corner to resize; the layout is fully responsive.               |
| Nothing happens after clicking Browse  | The dialog may be behind another window — check your taskbar.            |

## 7. Conclusion

You now know everything you need to keep your folders tidy with Automated
File Organizer. Happy organizing!
