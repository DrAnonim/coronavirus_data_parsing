Coronavirus data scraper

This Python script scrapes data from the Worldometer website on coronavirus cases around the world, 
and saves it to a CSV file called coronavirus_data.csv.

Installation

Clone the repository to your local machine using the command:

bash

    git clone https://github.com/DrAnonim/coronavirus_data_parsing.git


Install the required packages using the command:

bash

    pip install -r requirements.txt

This will install all necessary packages from the requirements.txt file. 
Make sure you have Python 3.x installed on your computer and have access to the command line.

Requirements

This script requires the following Python packages to be installed:

csv
datetime
typing
requests
bs4

These packages can be installed using pip.
How to use

Clone this repository or download the coronavirus_scraper.py file.

Open the terminal and navigate to the directory where the file is located.

Run the following command:

    python coronavirus_scraper.py

The script will then fetch the HTML content of the website and parse it using the BeautifulSoup library.

The data is then saved to a CSV file called coronavirus_data.csv.

If the file already exists, the data is appended to the end of the file.
If the file does not exist, a new file is created and the headers and data are written.

Functions

The script contains three functions:

get_html: This function takes a URL as input and returns the HTML content of the webpage as a string.

get_page_data: This function takes the HTML content of the webpage as input, parses it, 
and saves the data to a CSV file.

write_csv: This function writes data to a CSV file.
If the file exists, the data is written to the end of the file. If the file does not exist, 
a new file with the specified name is created and headers and data are written.

