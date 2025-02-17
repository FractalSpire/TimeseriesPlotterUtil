import json
import logging
from datetime import datetime

from matplotlib import pyplot as plt

class Plotter:
    def __init__(self, filename, option, logger: logging.Logger):
        self.logger = logger
        self.logger.info(f"Initialized new Plotter with input file-type: {option}")

        self.filename = f"./data/{filename}"
        self.option = option

        self.title = ""
        self.xlabel = ""
        self.ylabel = ""

        self.data = None
        self.allow_plotting = False  # This is True after data has been loaded successfully

    def load_data(self):
        """
        Loads data from the specified file based on the type.
        """
        if self.option == "csv":
            self.logger.info(f"Loading CSV data from {self.filename}...")
            # TODO: Implement CSV reading logic
        elif self.option == "json":
            self.logger.info(f"Loading JSON data from {self.filename}...")
            self.load_json()
        else:
            self.logger.error(f"Unsupported file type: {self.option}")

    def plot(self):
        self.logger.info(f"Plotting data from {self.filename}...")

        if not self.allow_plotting or not self.data:
            self.logger.error("Plotting is not yet enabled. Please load data first."
                              "This can also happend if the data did not load correctly.")
            return

        # Extract plot attributes
        # Y-Values
        y_values = self.data['data']

        # X-Values
        if "steps" in self.data:
            x_values = self.data["steps"]
            self.logger.info("Using custom steps for x-values.")
        else:
            step_size = self.data["stepsize"]
            x_values = [i * step_size for i in range(len(y_values))]
            self.logger.info(f"Generated x-values with step size {step_size}: {x_values}")

        # Ensure consistent length between x and y lists
        if len(x_values) != len(y_values):
            self.logger.error("Masmatch between number of x- and y-values.")
            return

        # Create new plot
        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='tab:blue')

        # Set plot labels and title
        plt.title(self.data['title'])
        plt.xlabel(self.data['xlabel'])
        plt.ylabel(self.data['ylabel'])

        # Customize Axes
        ax = plt.gca()
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')

        ax.spines['left'].set_color('black')
        ax.spines['bottom'].set_color('black')

        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

        # Grid and layout
        plt.grid(True, linestyle='-', alpha=0.3)
        plt.tight_layout()

        # Show plot
        self.logger.info("Displaying plot.")
        current_date = datetime.now().strftime("%d%m%Y-%H%M%S")
        save_path = f"./output/Plot_{current_date}.png"
        plt.savefig(save_path)
        plt.show()

    def load_json(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # Required keys
            required_keys = {"title", "xlabel", "ylabel", "data", "stepsize"}
            if not required_keys.issubset(json_data.keys()):
                self.logger.error(f"Missing required keys in JSON file: {self.filename}.")
                return

            # Extract values
            self.data = {
                "title": json_data["title"],
                "xlabel": json_data["xlabel"],
                "ylabel": json_data["ylabel"],
                "data": json_data["data"],
                "stepsize": json_data["stepsize"],
            }

            # Validate data array
            if not isinstance(self.data["data"], list):
                self.logger.error(f"'data' must be an array in JSON file: {self.filename}.")
                return

            # Handle step size
            if self.data["stepsize"] == "custom":
                if "steps" not in json_data or not isinstance(json_data["steps"], list):
                    self.logger.error(f"Missing or invalid 'steps' key in JSON file: {self.filename}")
                    return
                self.data["steps"] = json_data["steps"]
                self.logger.info(f"Custom step value loaded: {self.data['steps']}")
            else:
                try:
                    self.data["stepsize"] = float(self.data["stepsize"])
                    self.logger.info(f"Step size identified: {self.data['stepsize']}")
                except ValueError:
                    self.logger.error(f"Invalid step size format in JSON file: {self.filename}.")
                    return

            # Log success
            self.logger.info(f"Successfully loaded JSON data from {self.filename}")
            self.allow_plotting = True

        except FileNotFoundError:
            self.logger.error(f"File not found: {self.filename}.")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON format in file: {self.filename}.")
        except Exception as e:
            self.logger.error(f"Unexpected error while reading JSON: {str(e)}")
