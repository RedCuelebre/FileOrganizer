import sys
import os
import shutil
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileOrganizer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Organizador")
        self.resizable(False, False)  # Hacer la ventana no redimensionable

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load translations from the same directory as the script
        translations_path = os.path.join(script_dir, "translations.json")
        with open(translations_path, "r", encoding="utf-8") as file:
            self.translations = json.load(file)

        self.current_language = "en"

        # Main layout
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Language selection
        self.language_label = ttk.Label(self.main_frame, text=self.translations[self.current_language]["language"] + ":")
        self.language_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.language_combo = ttk.Combobox(self.main_frame, state="readonly")
        self.language_combo['values'] = ("English", "Español", "Français")
        self.language_combo.current(0)
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.language_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # Folder names input
        self.folder_labels = {}
        self.folder_inputs = {}

        row = 1
        for key in ['image_extensions', 'video_extensions', 'audio_extensions', 'office_extensions', 'executable_extensions', 'other_extensions']:
            label = ttk.Label(self.main_frame, text=self.translations[self.current_language][key] + ":")
            label.grid(row=row, column=0, sticky=tk.W, pady=5)
            self.folder_labels[key] = label

            line_edit = ttk.Entry(self.main_frame)
            line_edit.insert(0, self.translations[self.current_language][key])
            line_edit.grid(row=row, column=1, sticky=tk.EW, pady=5)
            self.folder_inputs[key] = line_edit

            row += 1

        # Select folder button
        self.button = ttk.Button(self.main_frame, text=self.translations[self.current_language]["select_folder"], command=self.select_folder)
        self.button.grid(row=row, column=0, columnspan=2, pady=20)

        # Set layout
        self.columnconfigure(1, weight=1)
        self.update_idletasks()
        width = self.main_frame.winfo_reqwidth() + 20
        height = self.main_frame.winfo_reqheight() + 20
        self.geometry(f"{width}x{height}")  # Ajusta el tamaño de la ventana

    def change_language(self, event=None):
        self.current_language = self.language_combo.get()[:2].lower()
        self.button.config(text=self.translations[self.current_language]["select_folder"])

        for key, label in self.folder_labels.items():
            label.config(text=self.translations[self.current_language][key] + ":")
        
        for key, line_edit in self.folder_inputs.items():
            line_edit.delete(0, tk.END)
            line_edit.insert(0, self.translations[self.current_language][key])

    def select_folder(self):
        folder = filedialog.askdirectory(title=self.translations[self.current_language]["select_folder"])
        if folder:
            self.organize_files(folder)

    def organize_files(self, folder):
        # Define the extensions for different file types
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        audio_extensions = ['.mp3', '.wav', '.aac', '.flac']
        office_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp', '.pdf']
        executable_extensions = ['.exe', '.bat', '.sh', '.bin', '.apk']

        # Define the folders to move the files to based on user input
        subfolders = {
            self.folder_inputs['image_extensions'].get(): image_extensions,
            self.folder_inputs['video_extensions'].get(): video_extensions,
            self.folder_inputs['audio_extensions'].get(): audio_extensions,
            self.folder_inputs['office_extensions'].get(): office_extensions,
            self.folder_inputs['executable_extensions'].get(): executable_extensions,
            self.folder_inputs['other_extensions'].get(): []
        }

        # Create the subfolders if they do not exist
        for subfolder in subfolders.keys():
            path = os.path.join(folder, subfolder)
            if not os.path.exists(path):
                os.makedirs(path)

        files = []
        for root, _, file_names in os.walk(folder):
            for file in file_names:
                files.append(os.path.join(root, file))

        total_files = len(files)

        if total_files == 0:
            messagebox.showinfo(self.translations[self.current_language]["done"], self.translations[self.current_language]["no_files"])
            return

        progress_dialog = ProgressDialog(self, self.translations[self.current_language]["organizing"])
        progress_dialog.update_progress(0)

        for i, file_path in enumerate(files):
            if not os.path.isfile(file_path):
                continue

            file_ext = os.path.splitext(file_path)[1].lower()

            moved = False
            for subfolder, extensions in subfolders.items():
                if file_ext in extensions:
                    shutil.move(file_path, os.path.join(folder, subfolder, os.path.basename(file_path)))
                    moved = True
                    break

            if not moved:
                shutil.move(file_path, os.path.join(folder, self.folder_inputs['other_extensions'].get(), os.path.basename(file_path)))

            progress = int((i + 1) / total_files * 100)
            progress_dialog.update_progress(progress)

        progress_dialog.destroy()
        messagebox.showinfo(self.translations[self.current_language]["done"], self.translations[self.current_language]["success_message"])

class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x100")
        self.resizable(False, False)
        self.grab_set()
        self.transient(parent)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.update()

    def update_progress(self, value):
        self.progress_var.set(value)
        self.update_idletasks()

if __name__ == "__main__":
    app = FileOrganizer()
    app.mainloop()
