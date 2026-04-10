import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import re

from matchers import ExactMatcher, RegexMatcher
from processor import FileProcessor


class FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Filter Tool")
        self.root.geometry("450x250")

        self.in_path = tk.StringVar()
        self.out_path = tk.StringVar()
        self.keyword = tk.StringVar()
        self.ignore_case = tk.BooleanVar()
        self.use_regex = tk.BooleanVar()

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Input File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.in_path, width=35).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self._browse_in).grid(row=0, column=2, padx=5)

        tk.Label(self.root, text="Output File:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.out_path, width=35).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self._browse_out).grid(row=1, column=2, padx=5)

        tk.Label(self.root, text="Keyword/Regex:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(self.root, textvariable=self.keyword, width=35).grid(row=2, column=1)

        options_frame = tk.Frame(self.root)
        options_frame.grid(row=3, column=1, sticky="w", pady=5)
        tk.Checkbutton(options_frame, text="Ignore Case", variable=self.ignore_case).pack(side="left")
        tk.Checkbutton(options_frame, text="Use Regex", variable=self.use_regex).pack(side="left")

        tk.Button(self.root, text="Start Filtering", command=self._run, bg="lightblue").grid(row=4, column=1, pady=15)

    def _run(self):
        if not self.in_path.get() or not self.out_path.get() or not self.keyword.get():
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            if self.use_regex.get():
                matcher = RegexMatcher(self.keyword.get(), self.ignore_case.get())
            else:
                matcher = ExactMatcher(self.keyword.get(), self.ignore_case.get())

            processor = FileProcessor(Path(self.in_path.get()), Path(self.out_path.get()), matcher)
            total, found = processor.process()

            messagebox.showinfo("Success", f"Done!\nChecked: {total} lines\nFound: {found} matches")
        except re.error:
            messagebox.showerror("Regex Error", "Invalid Regular Expression.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
