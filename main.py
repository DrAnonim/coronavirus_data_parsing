import csv
from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def write_csv(data_list: List[Dict[str, str]]) -> None:
    """
    Writes data to a CSV file.
    If the file exists, the data is written to the end of the file,
    otherwise, a new file with the specified name is created and headers and data are written.
    """
    try:
        with open('coronavirus_data.csv', 'a') as out_file: # Open file for appending
            writer = csv.writer(out_file) # Create CSV writer
            writer.writerow(list(data_list[0].keys())) # Write headers
            for data in data_list: # Loop over data list
                writer.writerow(list(data.values())) # Write data rows

    except IOError:
        print('no file') # Error message if file can't be created or opened
        with open('coronavirus_data.csv', 'a') as out_file: # Open new file for appending
            writer = csv.writer(out_file) # Create CSV writer
            for data in data_list: # Loop over data list
                writer.writerow(list(data.values())) # Write data rows


def get_page_data(html: str) -> None:
    """
    Parses an HTML page with information about coronavirus and saves data in a dictionary.
    The keys of the dictionary are column headers of the table on the website.
    The data is written to a list of dictionaries, which is then passed to the write_csv() function for writing to a file.
    :param html: HTML content of a web page
    :return: None
    """
    # initialize variables
    n = -1
    data: Dict[str, str] = {}
    keys_data_raw: List[str] = []
    keys_data: List[List[str]] = [('today').split()] # add the 'today' key to the keys_data list
    data_list: List[Dict[str, str]] = []

    try:
        # parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')
        # extract the table rows from the HTML
        trs_raw = soup.find('table', id='main_table_countries_today').find_all('tr')
        # extract the table headers from the HTML
        ths = soup.find('table', id='main_table_countries_today').find('thead').find('tr').find_all('th')
        # iterate over the table headers to create keys for the dictionary
        for th in ths:
            n = n + 1
            keys_data_raw.append(th.text.split())
            if len(keys_data_raw[n]) > 1:
                keys_data.append(''.join(keys_data_raw[n]).split())
            else:
                keys_data.append(th.text.split())
        keys_data.append(('url').split()) # add the 'url' key to the keys_data list

        # create a dictionary with keys from the keys_data list
        for i in keys_data:
            data.update(dict.fromkeys(i))

        del data['#'] # delete the '#' key, which is not needed

        # extract the table rows, excluding the header and footer rows
        trs = trs_raw[9:-8]
        i_keys_raw = data.keys()
        i_key: List[str] = []
        for i_key_raw in i_keys_raw:
            i_key.append(i_key_raw)

        # iterate over the table rows to extract data for each country
        for tr in trs:
            today = datetime.today().strftime("%m/%d/%Y")
            data[i_key[0]] = today # add the current date as the value for the 'today' key
            for i in range(1, (len(i_key) - 1)):
                temp = tr.find_all('td')[i].text
                data[i_key[i]] = temp

            # extract the URL for each country's detailed information
            try:
                country_other_url_raw = tr.find_all('td')[1].find('a', class_='mt_a').get('href')
                country_other_url_full = 'https://www.worldometers.info/coronavirus/{}'.format(country_other_url_raw)
                url = country_other_url_full
                data[i_key[(len(i_key) - 1)]] = url
            except AttributeError:
                url = 'missing information'
                data[i_key[(len(i_key) - 1)]] = url

            data_list.append(data.copy()) # add the data for each country to the data_list

        write_csv(data_list) # write the data to a CSV file

    except AttributeError:
        print('no data')


def get_html(url: str) -> str:
    """
    Gets an HTML page by a given URL address and returns it as a string.
    """
    # Make a request to the given URL and get the response
    r = requests.get(url)
    # If the response is successful (status code 200), print a message and return the HTML page as a string
    if r.ok:
        print('Code 200, working')
        return r.text
    # If the response is not successful, print the status code and return an empty string
    print(r.status_code)


def main():
    url = 'https://www.worldometers.info/coronavirus/'
    html = get_html(url)
    get_page_data(html)


if __name__ == '__main__':
    main()
