"""
Automated File Organizer - Smart Desktop File Management System
Python 3 + Tkinter (standard library only)

Run: python main.py
"""
import os
import json
import shutil
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"
HISTORY_FILE = DATA_DIR / "history.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
LOG_FILE = LOGS_DIR / "organizer.log"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}
OTHER_CATEGORY = "Others"

# Modern color palette (deep indigo / teal accent)
COLORS = {
    "bg": "#0F172A",          # background
    "surface": "#1E293B",      # card surface
    "surface_alt": "#273449",
    "border": "#334155",
    "text": "#F1F5F9",
    "muted": "#94A3B8",
    "primary": "#14B8A6",      # teal
    "primary_hover": "#0EA5A0",
    "accent": "#6366F1",       # indigo
    "accent_hover": "#4F46E5",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "nav": "#111827",
}

FONT_FAMILY = "Segoe UI"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_event(filename: str, destination: str, status: str) -> None:
    logging.info("%s -> %s | %s", filename, destination, status)


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------
def load_json(path: Path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError):
        pass
    return default


def save_json(path: Path, data) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError as exc:
        logging.error("Failed to save %s: %s", path, exc)


def category_for(ext: str) -> str:
    ext = ext.lower()
    for category, exts in FILE_CATEGORIES.items():
        if ext in exts:
            return category
    return OTHER_CATEGORY


def unique_destination(dest_dir: Path, filename: str) -> Path:
    target = dest_dir / filename
    if not target.exists():
        return target
    stem, suffix = os.path.splitext(filename)
    counter = 1
    while True:
        candidate = dest_dir / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


# ---------------------------------------------------------------------------
# Core organizer
# ---------------------------------------------------------------------------
def organize_folder(folder: Path):
    """Returns a stats dict for the run."""
    stats = {
        "scanned": 0,
        "organized": 0,
        "folders_created": 0,
        "skipped": 0,
        "errors": 0,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "folder": str(folder),
        "items": [],
    }
    if not folder.exists() or not folder.is_dir():
        raise ValueError("Selected path is not a valid folder.")

    category_dirs = set(FILE_CATEGORIES.keys()) | {OTHER_CATEGORY}

    for entry in folder.iterdir():
        if entry.is_dir():
            continue
        stats["scanned"] += 1
        try:
            category = category_for(entry.suffix)
            dest_dir = folder / category
            if not dest_dir.exists():
                dest_dir.mkdir(parents=True, exist_ok=True)
                stats["folders_created"] += 1
            # Skip files that already live in a category folder root
            if entry.parent.name in category_dirs:
                stats["skipped"] += 1
                continue
            target = unique_destination(dest_dir, entry.name)
            shutil.move(str(entry), str(target))
            stats["organized"] += 1
            stats["items"].append({
                "file": entry.name,
                "destination": category,
                "status": "moved",
            })
            log_event(entry.name, category, "moved")
        except PermissionError as exc:
            stats["errors"] += 1
            stats["items"].append({"file": entry.name, "destination": "-", "status": f"permission error"})
            log_event(entry.name, "-", f"permission error: {exc}")
        except Exception as exc:  # noqa: BLE001
            stats["errors"] += 1
            stats["items"].append({"file": entry.name, "destination": "-", "status": f"error: {exc}"})
            log_event(entry.name, "-", f"error: {exc}")

    # persist history
    history = load_json(HISTORY_FILE, [])
    history.insert(0, stats)
    save_json(HISTORY_FILE, history[:100])
    return stats


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------
class HoverButton(tk.Canvas):
    """Flat rounded-ish button rendered on canvas for a modern look."""

    def __init__(self, parent, text, command=None, *, bg=COLORS["primary"],
                 hover=COLORS["primary_hover"], fg="#FFFFFF", width=160, height=42,
                 font=(FONT_FAMILY, 10, "bold")):
        super().__init__(parent, width=width, height=height, bg=parent["bg"],
                         highlightthickness=0, bd=0)
        self.command = command
        self.bg = bg
        self.hover = hover
        self._rect = self.create_rectangle(0, 0, width, height, fill=bg, outline=bg)
        self._text = self.create_text(width / 2, height / 2, text=text, fill=fg, font=font)
        self.bind("<Enter>", lambda e: self.itemconfig(self._rect, fill=hover, outline=hover))
        self.bind("<Leave>", lambda e: self.itemconfig(self._rect, fill=bg, outline=bg))
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)

    def set_text(self, text):
        self.itemconfig(self._text, text=text)


def make_card(parent, *, padding=18):
    frame = tk.Frame(parent, bg=COLORS["surface"], highlightthickness=1,
                     highlightbackground=COLORS["border"])
    inner = tk.Frame(frame, bg=COLORS["surface"])
    inner.pack(fill="both", expand=True, padx=padding, pady=padding)
    frame.inner = inner
    return frame


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automated File Organizer")
        self.geometry("1180x720")
        self.minsize(1024, 640)
        self.configure(bg=COLORS["bg"])

        self.settings = load_json(SETTINGS_FILE, {"last_folder": ""})
        self.selected_folder = tk.StringVar(value=self.settings.get("last_folder", ""))
        self.current_page = "Dashboard"
        self.last_stats = None

        self._build_topnav()
        self._build_body()
        self.show_page("Dashboard")

    # -------------------- Top navigation --------------------
    def _build_topnav(self):
        nav = tk.Frame(self, bg=COLORS["nav"], height=64)
        nav.pack(side="top", fill="x")
        nav.pack_propagate(False)

        brand = tk.Frame(nav, bg=COLORS["nav"])
        brand.pack(side="left", padx=24)
        tk.Label(brand, text="📂", bg=COLORS["nav"], fg=COLORS["primary"],
                 font=(FONT_FAMILY, 22)).pack(side="left")
        tk.Label(brand, text="  File Organizer", bg=COLORS["nav"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 15, "bold")).pack(side="left")
        tk.Label(brand, text="  Pro", bg=COLORS["nav"], fg=COLORS["primary"],
                 font=(FONT_FAMILY, 10, "bold")).pack(side="left")

        self.nav_buttons = {}
        nav_frame = tk.Frame(nav, bg=COLORS["nav"])
        nav_frame.pack(side="left", padx=40)
        for name in ("Dashboard", "Organizer", "Statistics", "Logs", "About"):
            btn = tk.Label(nav_frame, text=name, bg=COLORS["nav"], fg=COLORS["muted"],
                           font=(FONT_FAMILY, 10, "bold"), padx=18, pady=22, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Button-1>", lambda e, n=name: self.show_page(n))
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=COLORS["text"]) if self.current_page != b.cget("text") else None)
            btn.bind("<Leave>", lambda e, b=btn: self._refresh_nav())
            self.nav_buttons[name] = btn

        right = tk.Frame(nav, bg=COLORS["nav"])
        right.pack(side="right", padx=24)
        tk.Label(right, text=datetime.now().strftime("%a, %d %b %Y"),
                 bg=COLORS["nav"], fg=COLORS["muted"], font=(FONT_FAMILY, 9)).pack()

    def _refresh_nav(self):
        for name, btn in self.nav_buttons.items():
            if name == self.current_page:
                btn.config(fg=COLORS["primary"])
            else:
                btn.config(fg=COLORS["muted"])

    # -------------------- Body --------------------
    def _build_body(self):
        self.body = tk.Frame(self, bg=COLORS["bg"])
        self.body.pack(fill="both", expand=True)

    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def show_page(self, name):
        self.current_page = name
        self._refresh_nav()
        self._clear_body()
        builder = {
            "Dashboard": self.page_dashboard,
            "Organizer": self.page_organizer,
            "Statistics": self.page_statistics,
            "Logs": self.page_logs,
            "About": self.page_about,
        }[name]
        builder()

    # -------------------- Pages --------------------
    def page_dashboard(self):
        wrap = tk.Frame(self.body, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=24)

        tk.Label(wrap, text="Dashboard", bg=COLORS["bg"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w")
        tk.Label(wrap, text="Overview of your file organization activity",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(2, 18))

        # Cards row
        cards = tk.Frame(wrap, bg=COLORS["bg"])
        cards.pack(fill="x")
        stats = self._aggregate_stats()
        card_data = [
            ("Total Scanned", stats["scanned"], COLORS["accent"], "🔍"),
            ("Files Organized", stats["organized"], COLORS["primary"], "✅"),
            ("Folders Created", stats["folders_created"], COLORS["warning"], "📁"),
            ("Skipped", stats["skipped"], COLORS["danger"], "⏭"),
        ]
        for i, (label, value, color, icon) in enumerate(card_data):
            self._stat_card(cards, label, value, color, icon).grid(
                row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 12, 0))
            cards.grid_columnconfigure(i, weight=1)

        # Quick action + activity
        bottom = tk.Frame(wrap, bg=COLORS["bg"])
        bottom.pack(fill="both", expand=True, pady=(20, 0))

        # Quick action card
        action = make_card(bottom)
        action.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(action.inner, text="Quick Start", bg=COLORS["surface"],
                 fg=COLORS["text"], font=(FONT_FAMILY, 14, "bold")).pack(anchor="w")
        tk.Label(action.inner, text="Jump straight to the Organizer to clean up a folder.",
                 bg=COLORS["surface"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(4, 16))
        HoverButton(action.inner, "Open Organizer →", command=lambda: self.show_page("Organizer"),
                    width=200).pack(anchor="w")
        tk.Label(action.inner, text=f"\nLast run: {stats.get('last_run', 'Never')}",
                 bg=COLORS["surface"], fg=COLORS["muted"], font=(FONT_FAMILY, 9)).pack(anchor="w")

        # Activity card
        activity = make_card(bottom)
        activity.pack(side="left", fill="both", expand=True)
        tk.Label(activity.inner, text="Recent Activity", bg=COLORS["surface"],
                 fg=COLORS["text"], font=(FONT_FAMILY, 14, "bold")).pack(anchor="w", pady=(0, 10))
        history = load_json(HISTORY_FILE, [])
        if not history:
            tk.Label(activity.inner, text="No activity yet. Run the organizer to see history here.",
                     bg=COLORS["surface"], fg=COLORS["muted"],
                     font=(FONT_FAMILY, 10)).pack(anchor="w")
        else:
            for run in history[:5]:
                row = tk.Frame(activity.inner, bg=COLORS["surface"])
                row.pack(fill="x", pady=4)
                tk.Label(row, text="•", bg=COLORS["surface"], fg=COLORS["primary"],
                         font=(FONT_FAMILY, 12, "bold")).pack(side="left", padx=(0, 8))
                folder_name = os.path.basename(run.get("folder", "")) or run.get("folder", "?")
                tk.Label(row, text=f"{folder_name}", bg=COLORS["surface"], fg=COLORS["text"],
                         font=(FONT_FAMILY, 10, "bold")).pack(side="left")
                tk.Label(row, text=f"  · {run['organized']} files organized",
                         bg=COLORS["surface"], fg=COLORS["muted"],
                         font=(FONT_FAMILY, 9)).pack(side="left")
                tk.Label(row, text=run.get("timestamp", ""),
                         bg=COLORS["surface"], fg=COLORS["muted"],
                         font=(FONT_FAMILY, 9)).pack(side="right")

    def _stat_card(self, parent, label, value, color, icon):
        card = make_card(parent)
        top = tk.Frame(card.inner, bg=COLORS["surface"])
        top.pack(fill="x")
        tk.Label(top, text=icon, bg=COLORS["surface"], fg=color,
                 font=(FONT_FAMILY, 18)).pack(side="left")
        tk.Label(top, text=label, bg=COLORS["surface"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(side="right")
        tk.Label(card.inner, text=str(value), bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 26, "bold")).pack(anchor="w", pady=(8, 0))
        bar = tk.Frame(card.inner, bg=color, height=3)
        bar.pack(fill="x", pady=(10, 0))
        return card

    # -------------------- Organizer --------------------
    def page_organizer(self):
        wrap = tk.Frame(self.body, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=24)

        tk.Label(wrap, text="Organizer", bg=COLORS["bg"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w")
        tk.Label(wrap, text="Select a folder and organize files by type in one click.",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(2, 18))

        # Drop / select area
        drop = make_card(wrap, padding=36)
        drop.pack(fill="x")
        tk.Label(drop.inner, text="📁", bg=COLORS["surface"], fg=COLORS["primary"],
                 font=(FONT_FAMILY, 48)).pack()
        tk.Label(drop.inner, text="Select a folder to organize",
                 bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 14, "bold")).pack(pady=(8, 4))
        path_label = tk.Label(drop.inner,
                              textvariable=self.selected_folder,
                              bg=COLORS["surface"], fg=COLORS["muted"],
                              font=(FONT_FAMILY, 10), wraplength=900)
        path_label.pack(pady=(0, 14))
        if not self.selected_folder.get():
            self.selected_folder.set("No folder selected yet")

        btns = tk.Frame(drop.inner, bg=COLORS["surface"])
        btns.pack()
        HoverButton(btns, "Browse Folder", command=self.browse_folder,
                    bg=COLORS["accent"], hover=COLORS["accent_hover"], width=160).pack(side="left", padx=6)
        HoverButton(btns, "Organize Now", command=self.run_organize, width=160).pack(side="left", padx=6)
        HoverButton(btns, "Clear", command=lambda: self.selected_folder.set("No folder selected yet"),
                    bg=COLORS["surface_alt"], hover=COLORS["border"], width=100).pack(side="left", padx=6)

        # Category chips
        chips = tk.Frame(wrap, bg=COLORS["bg"])
        chips.pack(fill="x", pady=(18, 0))
        tk.Label(chips, text="Supported categories", bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(0, 6))
        chip_row = tk.Frame(chips, bg=COLORS["bg"])
        chip_row.pack(anchor="w")
        chip_palette = [COLORS["primary"], COLORS["accent"], COLORS["warning"],
                        COLORS["success"], COLORS["danger"], COLORS["muted"]]
        for i, cat in enumerate(list(FILE_CATEGORIES.keys()) + [OTHER_CATEGORY]):
            color = chip_palette[i % len(chip_palette)]
            chip = tk.Label(chip_row, text=f"  {cat}  ",
                            bg=COLORS["surface"], fg=color,
                            font=(FONT_FAMILY, 9, "bold"),
                            padx=8, pady=6, bd=1, relief="flat",
                            highlightbackground=color, highlightthickness=1)
            chip.pack(side="left", padx=4)

        # Result preview
        self.result_card = make_card(wrap)
        self.result_card.pack(fill="both", expand=True, pady=(18, 0))
        tk.Label(self.result_card.inner, text="Run summary",
                 bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 13, "bold")).pack(anchor="w")
        self.result_text = tk.Label(self.result_card.inner,
                                    text="Results will appear here after you run the organizer.",
                                    bg=COLORS["surface"], fg=COLORS["muted"],
                                    font=(FONT_FAMILY, 10), justify="left", anchor="w")
        self.result_text.pack(anchor="w", pady=(6, 0), fill="x")

    def browse_folder(self):
        initial = self.selected_folder.get()
        if not initial or not os.path.isdir(initial):
            initial = str(Path.home())
        path = filedialog.askdirectory(title="Select folder to organize", initialdir=initial)
        if path:
            self.selected_folder.set(path)
            self.settings["last_folder"] = path
            save_json(SETTINGS_FILE, self.settings)

    def run_organize(self):
        path = self.selected_folder.get()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Invalid folder", "Please select a valid folder first.")
            return
        folder = Path(path)
        try:
            file_count = sum(1 for p in folder.iterdir() if p.is_file())
        except PermissionError:
            messagebox.showerror("Permission denied",
                                 "You do not have permission to read this folder.")
            return
        if file_count == 0:
            messagebox.showinfo("Empty folder", "The selected folder has no files to organize.")
            return
        if not messagebox.askyesno("Confirm",
                                   f"Organize {file_count} file(s) inside:\n{path}?"):
            return
        try:
            stats = organize_folder(folder)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Organize failed", str(exc))
            return
        self.last_stats = stats
        summary = (
            f"✔ Completed at {stats['timestamp']}\n\n"
            f"Scanned:          {stats['scanned']}\n"
            f"Organized:        {stats['organized']}\n"
            f"Folders created:  {stats['folders_created']}\n"
            f"Skipped:          {stats['skipped']}\n"
            f"Errors:           {stats['errors']}\n"
            f"Folder:           {stats['folder']}"
        )
        self.result_text.config(text=summary, fg=COLORS["text"])
        messagebox.showinfo("Done",
                            f"Organized {stats['organized']} of {stats['scanned']} file(s).")

    # -------------------- Statistics --------------------
    def page_statistics(self):
        wrap = tk.Frame(self.body, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=24)

        tk.Label(wrap, text="Statistics", bg=COLORS["bg"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w")
        tk.Label(wrap, text="All-time totals across every organizer run.",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(2, 18))

        stats = self._aggregate_stats()
        rows = [
            ("Total Files Scanned", stats["scanned"], COLORS["accent"]),
            ("Files Organized", stats["organized"], COLORS["primary"]),
            ("Folders Created", stats["folders_created"], COLORS["warning"]),
            ("Skipped Files", stats["skipped"], COLORS["danger"]),
            ("Errors", stats["errors"], COLORS["danger"]),
            ("Last Run Time", stats.get("last_run", "Never"), COLORS["muted"]),
        ]
        grid = tk.Frame(wrap, bg=COLORS["bg"])
        grid.pack(fill="x")
        for i, (label, value, color) in enumerate(rows):
            card = make_card(grid)
            card.grid(row=i // 3, column=i % 3, padx=(0 if i % 3 == 0 else 12, 0),
                      pady=(0 if i // 3 == 0 else 12, 0), sticky="nsew")
            grid.grid_columnconfigure(i % 3, weight=1)
            tk.Label(card.inner, text=label, bg=COLORS["surface"], fg=COLORS["muted"],
                     font=(FONT_FAMILY, 10)).pack(anchor="w")
            tk.Label(card.inner, text=str(value), bg=COLORS["surface"], fg=COLORS["text"],
                     font=(FONT_FAMILY, 20, "bold")).pack(anchor="w", pady=(6, 0))
            tk.Frame(card.inner, bg=color, height=3).pack(fill="x", pady=(10, 0))

        # History table
        history_card = make_card(wrap)
        history_card.pack(fill="both", expand=True, pady=(20, 0))
        tk.Label(history_card.inner, text="Run History",
                 bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 13, "bold")).pack(anchor="w", pady=(0, 8))

        cols = ("timestamp", "folder", "scanned", "organized", "skipped", "errors")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Org.Treeview",
                        background=COLORS["surface"],
                        fieldbackground=COLORS["surface"],
                        foreground=COLORS["text"],
                        rowheight=26, borderwidth=0)
        style.configure("Org.Treeview.Heading",
                        background=COLORS["surface_alt"],
                        foreground=COLORS["text"],
                        font=(FONT_FAMILY, 9, "bold"))
        style.map("Org.Treeview", background=[("selected", COLORS["accent"])])

        tree = ttk.Treeview(history_card.inner, columns=cols, show="headings",
                            style="Org.Treeview", height=10)
        for c, w in zip(cols, (160, 360, 90, 100, 90, 80)):
            tree.heading(c, text=c.title())
            tree.column(c, width=w, anchor="w")
        tree.pack(fill="both", expand=True)

        for run in load_json(HISTORY_FILE, []):
            tree.insert("", "end", values=(
                run.get("timestamp", ""),
                run.get("folder", ""),
                run.get("scanned", 0),
                run.get("organized", 0),
                run.get("skipped", 0),
                run.get("errors", 0),
            ))

    def _aggregate_stats(self):
        history = load_json(HISTORY_FILE, [])
        agg = {"scanned": 0, "organized": 0, "folders_created": 0,
               "skipped": 0, "errors": 0, "last_run": "Never"}
        for run in history:
            for k in ("scanned", "organized", "folders_created", "skipped", "errors"):
                agg[k] += int(run.get(k, 0) or 0)
        if history:
            agg["last_run"] = history[0].get("timestamp", "Never")
        return agg

    # -------------------- Logs --------------------
    def page_logs(self):
        wrap = tk.Frame(self.body, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=24)

        header = tk.Frame(wrap, bg=COLORS["bg"])
        header.pack(fill="x")
        tk.Label(header, text="Activity Logs", bg=COLORS["bg"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 22, "bold")).pack(side="left")
        HoverButton(header, "Refresh", command=lambda: self.show_page("Logs"),
                    bg=COLORS["accent"], hover=COLORS["accent_hover"], width=110).pack(side="right")
        HoverButton(header, "Clear Logs", command=self.clear_logs,
                    bg=COLORS["danger"], hover="#DC2626", width=110).pack(side="right", padx=8)

        tk.Label(wrap, text=f"Log file: {LOG_FILE}",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(2, 18))

        card = make_card(wrap)
        card.pack(fill="both", expand=True)

        text = tk.Text(card.inner, bg=COLORS["surface"], fg=COLORS["text"],
                       insertbackground=COLORS["text"], bd=0, relief="flat",
                       font=("Consolas", 10), wrap="none")
        text.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(card.inner, orient="vertical", command=text.yview)
        sb.pack(side="right", fill="y")
        text.configure(yscrollcommand=sb.set)

        try:
            content = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
        except OSError as exc:
            content = f"Failed to read logs: {exc}"
        text.insert("1.0", content or "No log entries yet.")
        text.config(state="disabled")

    def clear_logs(self):
        if messagebox.askyesno("Clear logs", "Erase all log entries?"):
            try:
                LOG_FILE.write_text("", encoding="utf-8")
            except OSError as exc:
                messagebox.showerror("Error", str(exc))
            self.show_page("Logs")

    # -------------------- About --------------------
    def page_about(self):
        wrap = tk.Frame(self.body, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=32, pady=24)

        tk.Label(wrap, text="About", bg=COLORS["bg"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 22, "bold")).pack(anchor="w")
        tk.Label(wrap, text="Project and developer information.",
                 bg=COLORS["bg"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10)).pack(anchor="w", pady=(2, 18))

        row = tk.Frame(wrap, bg=COLORS["bg"])
        row.pack(fill="both", expand=True)

        info = make_card(row)
        info.pack(side="left", fill="both", expand=True, padx=(0, 12))
        items = [
            ("Project", "Automated File Organizer"),
            ("Version", "1.0.0"),
            ("Tagline", "Smart Desktop File Management System"),
            ("Technologies", "Python 3 · Tkinter · ttk · JSON · logging"),
            ("License", "MIT"),
        ]
        for k, v in items:
            r = tk.Frame(info.inner, bg=COLORS["surface"])
            r.pack(fill="x", pady=4)
            tk.Label(r, text=k, bg=COLORS["surface"], fg=COLORS["muted"],
                     font=(FONT_FAMILY, 10), width=14, anchor="w").pack(side="left")
            tk.Label(r, text=v, bg=COLORS["surface"], fg=COLORS["text"],
                     font=(FONT_FAMILY, 10, "bold")).pack(side="left")

        dev = make_card(row)
        dev.pack(side="left", fill="both", expand=True)
        tk.Label(dev.inner, text="Developer", bg=COLORS["surface"], fg=COLORS["text"],
                 font=(FONT_FAMILY, 14, "bold")).pack(anchor="w")
        tk.Label(dev.inner,
                 text="Built with care using only Python's standard library.\n"
                      "No third-party dependencies are required.\n\n"
                      "Contact: developer@example.com\n"
                      "Website: https://example.com",
                 bg=COLORS["surface"], fg=COLORS["muted"],
                 font=(FONT_FAMILY, 10), justify="left").pack(anchor="w", pady=(8, 0))


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()