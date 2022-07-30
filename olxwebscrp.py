import requests
import bs4
import json
from tqdm import tqdm
import pandas as pd
import datetime


# List of functions to scrape data from OLX

def get_links(npages=3):
    '''
    Returns a list of links to OLX listings and Otodom as second element
    '''

    pages = []

    print("Scraping links from OLX...")
    for i in tqdm(range(npages)):
        r = requests.get(
            "https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/lublin/?page={}".format(i+1))

        if r.status_code == 200:
            pages.append(bs4.BeautifulSoup(r.text, "html.parser"))

    links = []

    for p in pages:
        for a in p.find_all("a", {"class": "css-1bbgabe"}):
            links.append(a["href"])

    olx_links = []
    otodom_links = []

    for link in links:
        if "otodom" in link:
            otodom_links.append(link)
        else:
            olx_links.append("http://www.olx.pl" + link)

    return olx_links, otodom_links


# Extracting flat data from olx.pl

def extract_data_olx(link):

    r1 = bs4.BeautifulSoup(requests.get(link).text, "html.parser")
    # .find("window.__PRERENDERED_STATE__")
    script_w_data_json = str(r1.find_all(
        "script", {"id": "olx-init-config"})[0])

    start = script_w_data_json.find("window.__PRERENDERED_STATE__")
    stop = script_w_data_json.find("window.__TAURUS__")

    json_extracted = script_w_data_json[start+30:stop-10]
    j = json.loads(json.loads(json_extracted))

    try:

        id = j['ad']['ad']['id']
        createdTime = j['ad']['ad']['createdTime']
        lastRefresh = j['ad']['ad']['lastRefreshTime']
        params = j['ad']['ad']['params']
        price = j['ad']['ad']['price']['regularPrice']['value']
        location = j['ad']['ad']['location']['cityName']

        params_dic = {param['key']: param['normalizedValue']
                      for param in params}

        collected_data = {
            "id": id,
            "createdTime": createdTime,
            "lastRefresh": lastRefresh,
            "price": price,
            "location": location,
            "url": link,
            **params_dic
        }

    except:
        collected_data = {
            "id": "",
            "createdTime": "",
            "lastRefresh": "",
            "price": "",
            "location": ""
        }

    return collected_data


def extract_data_otodom(link):
    r1 = bs4.BeautifulSoup(requests.get(link).text, "html.parser")

    try:

        j = json.loads(r1.find("script", {"id": "__NEXT_DATA__"}).text)

        data = j['props']['pageProps']['ad']['target']

        area = data['Area']
        build_year = data['Build_year']
        city = data['City']
        floor = data['Floor_no']
        id = data['Id']
        markettype = data['MarketType']
        price = data['Price']
        price_per_m2 = data['Price_per_m']
        date_created = j['props']['pageProps']['ad']['dateCreated']
        date_lastmod = j['props']['pageProps']['ad']['dateModified']
        rooms = data['Rooms_num'][0]
        builttype = data['Building_type'][0]

        collected_data = {
            "m": area,
            "build_year": build_year,
            "location": city,
            "floor": floor[0],
            "id": id,
            "market": markettype,
            "price": price,
            "price_per_m2": price_per_m2,
            "date_created": date_created,
            "date_lastmod": date_lastmod,
            "rooms": rooms,
            "builttype": builttype,
            "url": link
        }

    except:
        print("Error in reading data from JSON")
        collected_data = {
            "m": "",
            "build_year": "",
            "location": "",
            "floor": "",
            "id": "",
            "market": "",
            "price": "",
            "price_per_m2": "",
            "date_created": "",
            "date_lastmod": "",
            "rooms": "",
            "builttype": ""
        }

    return collected_data


def collect_data_save_table(npages=10):

    # Grabbing links from olx.pl and otodom.pl
    olx_links, otodom_links = get_links(npages)

    # Save to csv both data from olx.pl and otodom.pl with month name in file name
    now = datetime.datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")

    # Extracting data from olx.pl
    print("Extracting data from olx.pl...")
    olx_data = []
    for link in tqdm(olx_links):
        olx_data.append(extract_data_olx(link))

    pd.DataFrame(olx_data).to_csv("olx_data_{}_{}.csv".format(month, year))

    # Extracting data from otodom.pl
    print("Extracting data from otodom.pl...")
    otodom_data = []
    for link in tqdm(otodom_links):
        otodom_data.append(extract_data_otodom(link))

    pd.DataFrame(otodom_data).to_csv(
        "otodom_data_{}_{}.csv".format(month, year))


#### MAIN ####
if __name__ == "__main__":

    collect_data_save_table(20)
    # extract_data_olx("https://www.olx.pl/oferta/mieszkanie-w-krakowie-lublin-IDgZQQACX
