#!/usr/bin/env python

import urllib2
# Get beautifulsoup4 with: pip install beautifulsoup4
import bs4
import json


# To help get you started, here is a function to fetch and parse a page.
# Given url, return soup.
def url_to_soup(url):
    # bgp.he.net filters based on user-agent.
    req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html)

    # Finding the table body on the page
    tbody = soup.find("tbody")
    countries = []

    # Taking all country codes in a list
    for row in tbody.findAll('tr'):
        col = row.findAll('td')
        countryCode = col[1].string
        countryCode = countryCode.strip().encode('utf-8')
        countries.append(countryCode)

    # Initialising an empty dictionary to store the info in an object notation format.
    mapping = {}
    with open("outputASN.json", "w") as file:
        for code in countries:
            # Going to each report page by providing country code in the url since the structures is same
            req = urllib2.Request("http://bgp.he.net/country/" + code, headers={'User-Agent': 'Mozilla/5.0'})
            reportPage = bs4.BeautifulSoup(urllib2.urlopen(req).read())
            report = reportPage.find("tbody")

            try:
                for row in report.findAll('tr'):
                    col = row.findAll('td')

                    # Stripping out AS from the ASN to get the ASN number
                    asn = col[0].string.strip("AS")

                    # Initialising a nested dictionary for each ASN number and storing info for that ASN
                    mapping[asn] = {}
                    mapping[asn]['Country'] = code
                    mapping = col[1].strwing
                    mapping[asn]['Name'] = name
                    rv4 = col[3].string
                    mapping[asn]['Routes v4'] = rv4
                    rv6 = col[5].string
                    mapping[asn]['Routes v6'] = rv6

            # Checking if report is Null like in case of country code Mayotte(YT)
            except AttributeError:
                continue
        # Saving file to a json format
        json.dump(mapping, file, indent=4)
    file.close()


# Passing the main url to the function
url_to_soup("http://bgp.he.net/report/world")
