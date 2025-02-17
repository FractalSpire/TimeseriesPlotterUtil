import os.path
import logging
import tkinter
from tkinter.filedialog import FileDialog

import ttkbootstrap as tb

from logging.handlers import RotatingFileHandler
from ttkbootstrap.dialogs import Messagebox

from logic.plotter import Plotter

LOG_FILE = "./logs/app.log"  # Main app log location
MAX_LOG_SIZE = 1 * 1024 * 1024  # Limit to 1 MB

# Color codes for logging:
LOG_COLORS = {
    "DEBUG": "\033[90m",    # Gray
    "INFO": "\033[94m",     # Light Blue
    "WARNING": "\033[93m",  # Orange
    "ERROR": "\033[91m",    # Red
    "RESET": "\033[0m"      # Reset to default
}


def setup_logger(log_file):
    """
    Sets up a logger for the application. Logs to console and a file (file rotation is enabled).
    Also checks for the existence of a './logs' directory and creates one if required.
    :param log_file: path to logfile
    :return: logger
    """
    # Check that the logs directory exists
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    # Create Logger
    logger = logging.getLogger("CustomLogger")
    logger.setLevel(logging.INFO)  # main logging level set to info and above

    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = RotatingFileHandler(log_file, maxBytes=MAX_LOG_SIZE, backupCount=2)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def get_file_type(file_name):
    _, ext = os.path.splitext(file_name)
    ext = ext.lower()

    if ext == ".csv":
        return "csv"
    elif ext == ".json":
        return "json"
    else:
        return None


class Main:
    def __init__(self):
        # set up application logger
        self.logger = setup_logger(LOG_FILE)
        self.logger.info("---- Started App, Logger init ----")
        self.logger.info("Checking existence of working directories...")
        self.check_folders()

        # Wait for the user to put the necessary files into the data folder
        files_moved = Messagebox.show_question(
            "Have you moved the necessary files into the data folder?",
            "Moved files?"
        )

        if files_moved == "No":
            self.logger.info("User did not yet move files to the appropriate directory.")
            Messagebox.show_warning("Please move the required files you want to fetch data from to the data directory."
                                    "Then restart the program.")
            quit(1)

        files = self.list_files()

        if files:
            selected_file = self.choose_file(files)
            self.logger.info(f"Selected file: {selected_file}")

            if not selected_file:
                Messagebox.show_warning("Invalid file or no file selected.")
                quit(0)

            plotter = Plotter(selected_file, get_file_type(selected_file), self.logger)
            plotter.load_data()
            plotter.plot()



    def check_folders(self):
        """Ensure all folders required by the program exist."""
        folders = [
            "data",
            "output"
        ]

        for folder in folders:
            self.ensure_folder_exists(folder)

    def ensure_folder_exists(self, folder_name):
        """Ensure that the folder with given name exists: 'folder_name'."""
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            self.logger.info(f"'{folder_name}' was created.")
        else:
            self.logger.debug(f"'{folder_name}' folder already exists.")

    def list_files(self, folder_name = "./data"):
        """
        List all CSV and JSON files in the specified directory.
        Writes all detected files to console as options.
        :param folder_name: name of the folder to search for files (default: './data')
        :return: list of all file-names or None
        """
        files = [f for f in os.listdir(folder_name) if f.endswith(('.csv', '.json'))]

        if not files:
            self.logger.warning(f"No CSV or JSON files found in the specified directory: '{folder_name}'.")
            Messagebox.show_warning(f"No CSV or JSON files found in the specified directory: '{folder_name}'.")
            return None

        return files

    def choose_file(self, files):
        if not files:
            return None

        file_path = tkinter.filedialog.askopenfilename(
            title="Select a CSV or JSON File",
            initialdir="data",  # Open the 'data' folder by default
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")],
        )

        if file_path:
            file_name = os.path.basename(file_path)  # Extract filename only
            self.logger.info(f"User selected file: {file_name}")
            return file_name
        else:
            self.logger.warning("No file was selected.")
            return None

class ColoredFormatter(logging.Formatter):
    """Custom formatter to colorize console logs."""

    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["RESET"])
        log_message = super().format(record)
        return f"{log_color}{log_message}{LOG_COLORS['RESET']}"


if __name__ == '__main__':
    app = Main()