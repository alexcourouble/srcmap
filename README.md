# srcmap

Displaying linux source code information in a zoomable treemap

--------------------------------------------------------------------------------

## How to run the app

This directory contains the files to view the treemap on your own machine. This version of the app is setup to run on a local host on port 8000. 

To start your local server, run the follwing command from the *web_interface* directory.

```
python -m SimpleHTTPServer 8000
```

Now enter the following address in your browser:

```
http://localhost:8000
```

Note: The app will **not** work in Chrome! The script is not yet optimized, and takes a few moments to generate the whole treemap. Please use Safari or Firefox.

--------------------------------------------------------------------------------

## Web Interface

This directory contains the srcmap app.

### dataFiles:

* graftedData.csv

...Contains the data created by *db2csv.py*.

* authColorMapGrafted.csv

...Contains the colors of each authors to display in the list and the plot on the bottom right of the screen. 

### scripts

* scriptGrafted.js

...Contains the code necessary to generated all the elements of the visualization.

* papaparse.min.js 

...Csv reader package to read the author colors.


--------------------------------------------------------------------------------

## Mining

### db2csv.py

This file will read Daniel German's DB to create the data file necessary for the online tool.

The output data file is a CSV file containing the top 20 contributors of each file as well as the number of lines of code written by them in the coresponding version. 

The data is aggregated in the directory tree.


--------------------------------------------------------------------------------

## Color Map

Here are the html files and the scripts that I used to create the color map. The library used for the tool only takes a number as input for the color. The tool then chooses a color and there is not way to get a node's actual hex color after the tool is created. 

Since I assign each top-1 author a number between 1 and 10,000, I had to find out what those number meant in hex code. So I created a treemap with 10,000 diferent nodes with color codes ranging from 1 to 10,000. I was then able to create a map between each color number to its coresponding hex code.
