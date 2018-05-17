from time import sleep
from urllib.parse import urljoin
import csv
import requests
from lxml import html

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

proxies = {
    'http': 'http://209.50.53.21:3128',
    'https': 'https://165.227.104.78:3128',
}

links = []
url = 'https://www.amazon.com/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A1055398%2Cn%3A1063252%2Ck%3A-as&keywords=-as&ie=UTF8&qid=1520670994'

while True:
    try:
        print('Fetching url [%s]...' % url)
        response = requests.get(url, headers=headers, proxies=proxies, stream=True)
        if response.status_code == 200:
            source = html.fromstring(response.content)
            links.extend(source.xpath('//*[contains(@id,"result")]/div/div[3]/div[1]/a/@href'))
            try:
                next_url = source.xpath('//*[@id="pagnNextLink"]/@href')[0]
                url = urljoin('https://www.amazon.com', next_url)
            except IndexError:
                break
    except Exception:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        sleep(5)
        print("Was a nice sleep, now let me continue...")

csvfile = "csv/Bedding.csv"

# Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in links:
        writer.writerow([val])