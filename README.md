# TimeseriesPlotterUtil
Small Python Tool for plotting a timeseries from a file. Intended for the creation of preconfigured plots from data for visualization only.

The tool is currently run from your IDE or through a console and uses ttkbootstrap GUI 

# Prerequisites
This tool requires the following setup to work:
- A data folder (gets created on first start if not already there). This folder should contain your data either in csv or json format.
- An output folder for saving the plots created by the program to png files.

Both folders are created automatically on first start of the program.

The program always prompts the user to confirm whether the files they want to analyse are placed in the data folder.
On confirmation the program then prompt the user to select either a CSV or JSON file. Currently only JSON is supported.

Look [here](#json-file-structure) for a guide on how to structure your data JSON files.

# Output
The program automatically stores every plot created as a png file in the `/output` directory.
The files created are automatically named to avoid any overrides of plots created earlier.

## File naming scheme
Output png files are named using the following scheme:
`Plot_<Date>-<Time>.png`
The date and time are derived from the local system time and added automatically.
Later versions will include more customizable output options.

# Input
## JSON file structure
JSON files that are to be used for plotting data using this tool need adhere to a specific structure. This structure is as follows:

The following keys are to be included in the JSON file:
- `title`
- `xlabel`
- `ylabel`
- `data`
- `stepsize`
- `steps`¹

¹*steps is not a mandatory key if stepsize is set to a numeric value, 
if stepssize is set to "custom" steps is used to define the actual steps (x-values) for each y-value.*

➡️`title`:
Text to print as title of the plot.

➡️`xlabel`:
Label for the x-Axis of the plot.

➡️`ylabel`:
Label for the y-Axis of the Plot

➡️`data`:
list of numerical (float) values, represented by the y-values of the resulting plot.

➡️`stepsize`:
Size of steps on the x-axis. Numerical value creates an array of x-values the size of the data array starting at 0
with values spaced apart by this value. If this is set to "custom" a "steps"-list needs to be defined.

➡️`steps`¹:
Optional. List of x-values that correspond to the y-values defined in "data". Only active if stepsize is set to "custom".

### Example JSON
A JSON-file that can be used with this tool looks something like this:
```json
{
  "title": "JSON example file result",
  "xlabel": "X-Label",
  "ylabel": "Y-Label",
  "data": [
    1,
    2,
    3,
    4,
    5
  ],
  "stepsize": "custom",
  "steps": [
    0.5,
    1,
    1.5,
    2,
    2.5
  ]
}
```

The output of this file looks like this:
![example image of plot resulting from example JSON file.](/documentation/Plot_17022025-115947.png "Example Plot result")

The example JSON file is located in the `/documentation` directory in this repository (`example.json`).
