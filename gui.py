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
