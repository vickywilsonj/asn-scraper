'''
Scraping Autonomous System Numbers from http://bgp.he.net/report/world

Created on Sep 6, 2017
@author: vickywilsonj
Website: https://github.com/vickywilsonj
'''
import datetime
import json, locale
import urllib2
import bs4


base_url = "https://bgp.he.net"
asn_database = {}

'''
Crawl the root page
Input: URL
'''
def crawl(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    # Open url and get data
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id":"table_countries"})
    
    for row in table.findAll("tr"):
        columns = row.findAll("td")
        if len(columns) > 0:
            country = columns[1].get_text().strip()
            page_url = columns[2].findNext('a')['href']
            country_url = base_url + page_url
            scrape_country(country_url, country)
    
    return soup

'''
Crawl the country page
Input: URL
'''
def scrape_country(url, country):
    print ("Scraping country:" + country)
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    # Open url and get data
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id":"asns"})
    if(table != None):
        for row in table.findAll("tr"):
            columns = row.findAll("td")
            if len(columns) > 0:
                asn_record = {}
                asn = columns[0].get_text()[2:]         
                asn_record['Country'] = country
                asn_record['Name'] = columns[1].get_text()
                asn_record['Routes v4'] = locale.atoi(columns[3].get_text())
                asn_record['Routes v6'] = locale.atoi(columns[5].get_text())
                asn_database[asn] = asn_record

if __name__ == '__main__':
    print "Program started at: " + str(datetime.datetime.now())
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    soup = crawl('http://bgp.he.net/report/world')
    with open('ASNData.json', 'w') as f_out:
        json.dump(asn_database, f_out, ensure_ascii=True, encoding='utf-8',indent=4, separators=(',', ': '))
    print "Program ended at: " + str(datetime.datetime.now())
