# asn-scraper
Scraping Autonomous System Numbers by crawling http://bgp.he.net/report/world

ASNs (Autonomous System Numbers) are one of the building blocks of the
Internet. This project is to create a mapping from each ASN in use to the
company that owns it. For example, ASN 36375 is used by the University of
Michigan - http://bgp.he.net/AS36375

The site http://bgp.he.net/ has lots of useful information about ASNs. 
Starting at http://bgp.he.net/report/world crawl and scrape the linked country reports to make a json structure mapping each ASN to info about that ASN.

Sample Json mapping:
```
{
    "6939": {
        "Country": "US",
        "Name": "Hurricane Electric LLC",
        "Routes v4": 140569,
        "Routes v6": 50836
    },
    "174": {
        "Country": "US",
        "Name": "Cogent Communications",
        "Routes v4": 185309,
        "Routes v6": 15362
    }
}
```
