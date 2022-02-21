"""
Module Docstring
"""

__author__ = "Vicky Wilson Jacob"
__version__ = "1.0.0"
__license__ = "DataHackr"

import argparse
import logging as log
import time
import requests
import json, locale
from bs4 import BeautifulSoup

base_url = "https://bgp.he.net"
asn_database = {}

'''
Crawl the root page
Input: URL
'''
def crawl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    html = requests.get(url, headers=headers).text
    # Open url and get data
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id":"table_countries"})
    
    for row in table.findAll("tr"):
        columns = row.findAll("td")
        if len(columns) > 0:
            country = columns[1].get_text().strip()
            page_url = columns[2].findNext('a')['href']
            country_url = base_url + page_url
            scrape_country(country_url, country)

'''
Crawl the country page
Input: URL
'''
def scrape_country(url, country):
    print ("Scraping country:" + country)
    html = requests.get(url, headers={ 'User-Agent': 'Mozilla/5.0' }).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id":"asns"})
    if(table != None):
        for row in table.findAll("tr"):
            columns = row.findAll("td")
            if len(columns) > 0:
                asn_record = {}
                asn = columns[0].get_text()[2:]         
                asn_record['Country'] = country
                asn_record['Name'] = columns[1].get_text()
                asn_record['Routes v4'] = locale.atoi(columns[3].get_text().replace(',',''))
                asn_record['Routes v6'] = locale.atoi(columns[5].get_text().replace(',',''))
                asn_database[asn] = asn_record

def main(args):
    """ Main entry point of the app """
    log.basicConfig(filename='crawler.log', format='%(asctime)s:%(funcName)s:Line %(lineno)d: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=log.INFO)
    log.info('Application started at: ' +
             time.asctime(time.localtime(time.time())))
    
    print(f"Crawling the URL: {args.URL}")
    crawl(args.URL)
    with open('ASNData.json', 'w') as f_out:
        json.dump(asn_database, f_out, ensure_ascii=True,indent=4, separators=(',', ': '))

    log.info('Application completed at: ' +
             time.asctime(time.localtime(time.time())))


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Required positional argument
    parser.add_argument("URL", action="store",
                        help="Web URL to scrape.")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
