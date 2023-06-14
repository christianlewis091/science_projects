"""
I'm trying to webscrape GLODAP website
https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/GLODAPv2_2021/cruise_table_v2021.html
So I don't have to click into every "Data Files" Page
The first and last "Data File" pages are:

https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0113894/
https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0115024/

and I think I can use that difference in final number for the scrape. The following website is helpful to me:
https://medium.com/@CodeYogi/bulk-downloading-files-from-websites-with-python-1caa011af0af

The FIRST instance of running this code errored out at line Cruise No. 268,
I'm going to start it again at 269 and invoke the TRY except clause to keep it from doing that again


"""

import requests
from bs4 import BeautifulSoup
import csv
import os

# Function to download a CSV file given a URL and save it in the specified directory
savings = "H:\Science\Datasets\Hydrographic\GLODAP_scrape2"

# def download_csv(url, filename, save_directory):
#     response = requests.get(url)
#     save_path = os.path.join(save_directory, filename)
#     with open(save_path, 'wb') as file:
#         file.write(response.content)

# URL of the main table page
main_url = 'https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/GLODAPv2_2021/cruise_table_v2021.html'

# Send a GET request to the main table page
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table on the page
table = soup.find('table')

# Specify the column index (starting from 0) containing the links you want to process
column_index = 19

# # Count the rows
# row_num = []
# x = 0
# for row in table.find_all('tr'):
#     x = x+1
#     row_num.append(x)
# print(x)

x = 0
# Rerunning it with try/except for all rows.
for row in table.find_all('tr'):
    x = x+1
    print(x)
  # see notes above
    try:
        print(x)
        # Find the cells in the specified column
        cells = row.find_all('td')
        if len(cells) > column_index:
            link = cells[column_index].find('a')
            if link is not None:
                url = link['href']
                print(url)

                response = requests.get(url)

                # Proceed if the response is successful
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Find all <a> tags with href attribute
                    links = soup.find_all("a", href=True)

                    for link in links:
                        href = link["href"]

                        # Check if the href ends with ".csv"
                        if href.endswith(".csv"):
                            file_url = f"{url}/{href}" if not href.startswith("http") else href

                            # Download the CSV file
                            response_csv = requests.get(file_url)

                            # Extract the filename from the URL
                            filename = os.path.join(savings, href.split("/")[-1])

                            # Save the file if the response is successful and the content is CSV
                            if response_csv.status_code == 200 and response_csv.headers.get("content-type") == "text/csv":
                                with open(filename, "wb") as file:
                                    file.write(response_csv.content)
                                    print(f"Downloaded: {filename}")
                            else:
                                print(f"Skipping: {filename}")

    except:
        x = 1
#
#


#
# import requests
# from bs4 import BeautifulSoup
# import csv
#
# # Function to download a CSV file given a URL
# def download_csv(url, filename):
#     response = requests.get(url)
#     with open(filename, 'wb') as file:
#         file.write(response.content)
#
# # URL of the main table page
# main_url = 'https://example.com/main-table-page'
#
# # Send a GET request to the main table page
# response = requests.get(main_url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# # Find the table on the page
# table = soup.find('table')
#
# # Specify the starting row
# starting_row = 269
#
# # Initialize a row counter
# row_counter = 0
#
# # Iterate through each row in the table
# for row in table.find_all('tr'):
#     # Increment the row counter
#     row_counter += 1
#
#     # Skip rows until reaching the desired starting row
#     if row_counter < starting_row:
#         continue
#
#     # Find the link in each row
#     link = row.find('a')
#     if link is not None:
#         link_url = link['href']
#
#         # Send a GET request to the link URL
#         link_response = requests.get(link_url)
#         link_soup = BeautifulSoup(link_response.text, 'html.parser')
#
#         # Find the CSV file on the link page
#         csv_link = link_soup.find('a', href=lambda href: href.endswith('.csv'))
#         if csv_link is not None:
#             csv_url = csv_link['href']
#
#             # Extract the filename from the URL
#             csv_filename = csv_url.split('/')[-1]
#
#             # Download the CSV file
#             download_csv(csv_url, csv_filename)
#             print(f"Downloaded CSV file: {csv_filename}")
