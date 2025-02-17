import os.path
import logging
from logging.handlers import RotatingFileHandler


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


class Main:
    def __init__(self):
        # set up application logger
        self.logger = setup_logger(LOG_FILE)
        self.logger.info("---- Started App, Logger init ----")

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
            self.logger.info(f"'{folder_name}' folder already exists.")


class ColoredFormatter(logging.Formatter):
    """Custom formatter to colorize console logs."""

    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["RESET"])
        log_message = super().format(record)
        return f"{log_color}{log_message}{LOG_COLORS['RESET']}"


if __name__ == '__main__':
    app = Main()