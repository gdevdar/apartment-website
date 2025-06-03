import cloudscraper
from bs4 import BeautifulSoup
import json


def read_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def scrape(link,scraper):
    response = scraper.get(link)
    page = response.text
    del response
    return page

def extract_data(page):
    soup = BeautifulSoup(page, 'html.parser')
    script_tag = soup.find('script', type='application/json')
    string = script_tag.string
    json_data = json.loads(string)
    queries = json_data['props']['pageProps']['dehydratedState']['queries']
    return queries

def trim_data(data):
    main_data = data[0]['state']['data']['data']['statement']
    data_update_count = data[0]['state']['dataUpdateCount']
    full_data = {"main_data":main_data, "data_update_count":data_update_count}
    return full_data

def full_process(link,scraper):
    try_count = 0
    full_data = {}
    failed = False
    except_count = 0
    while True:
        try:
            page = scrape(link,scraper)
            try_count += 1
            data = extract_data(page)
            is_empty = data == []
            if is_empty:
                if try_count > 10:
                    #print(f"Didn't have the needed data: {link}")
                    failed = True
                    break
                else:
                    #time.sleep(5)
                    continue
            else:
                full_data = trim_data(data)
                #if try_count > 1:
                    #print(f"success for {link}")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            except_count += 1
            if except_count > 10:
                failed = True
                print(f"Errored too many times: {link}")
                break
            #time.sleep(2)
    return full_data, failed

def data_collector(url):
    #batch_identifier = url_batch[0][22:33]
    scraper = cloudscraper.create_scraper(delay=10, interpreter='nodejs')
    #print(f"processing {i}/{batch_size} of batch {batch_identifier} \n {url}")
    json_data, failed = full_process(url,scraper)
    json_data
    return json_data