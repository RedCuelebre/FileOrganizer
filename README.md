# FileOrganizer

FileOrganizer is a Python desktop application that organizes files in a selected folder based on their extensions. It uses the `tkinter` library for the graphical user interface and supports multiple languages.

## Features

- Organizes files into subfolders based on their extensions.
- Supports multiple languages (currently: English, Spanish, and French).
- Intuitive graphical user interface.
- Displays progress of the file organization process.

## Requirements

- Python 3.x
- Python libraries: `tkinter`, `shutil`, `json`, `os`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/file-organizer.git
   cd file-organizer
   ```

2. Ensure you have the necessary libraries installed. If not, install them:
   ```bash
   pip install tk
   ```

3. Ensure the `translations.json` file is in the same directory as the main script (`file_organizer.py`). This file contains the necessary translations for the application.

## Usage

1. Run the script:
   ```bash
   python file_organizer.py
   ```

2. Select the desired language from the dropdown menu.

3. Enter the names of the subfolders for each file type.

4. Click the "Select Folder" button and choose the folder you want to organize.

5. The program will move the files to the corresponding subfolders and display a dialog with the progress of the process.

## Contribution

If you wish to contribute to this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-new-feature`).
3. Make the necessary changes and commit (`git commit -am 'Add new feature'`).
4. Push the changes to your branch (`git push origin feature-new-feature`).
5. Create a Pull Request.

## License

This project is licensed under the GPL-3.0 License. See the `LICENSE` file for details.

---

Thank you for using FileOrganizer! If you have any questions or suggestions, feel free to open an issue on GitHub.
