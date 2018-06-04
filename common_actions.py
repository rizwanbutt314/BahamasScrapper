import requests
import urllib
import re
import os
import datetime
import dateparser
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder


def make_request(HOME_URL, post_data):
    m = MultipartEncoder(post_data, boundary='my_super_custom_header')
    r = requests.post(HOME_URL, headers={'Content-Type': m.content_type}, data=m.to_string())
    soup = BeautifulSoup(r.text, 'html5lib')
    return soup


def make_get_request(HOME_URL):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    }
    r = requests.get(HOME_URL, headers=header)
    soup = BeautifulSoup(r.text, 'html5lib')
    return soup


def parse_pdf_url(pdf_url):
    pdf_url = pdf_url.replace("/cms/images/", "")
    slash_split = pdf_url.split("/")
    title_slug = slash_split[-1].rsplit(".pdf", 1)[0]
    _type = slash_split[1]
    return (title_slug, _type)


def pdf_local_url(_type, year, item_num, title_slug):
    local_url = "/".join([_type, str(year), item_num, title_slug]) + ".pdf"
    return local_url


def legistation_parsing(row):
    total_tds = len(row.find_all("td"))
    created_at = datetime.datetime.now()
    migrated = 1
    item_num = row.find_all("td")[0].get_text().strip()
    year = int(item_num.split('-')[0])
    number = int(item_num.split('-')[1])
    category = ""

    try:
        notes = row.find_all("td")[0]["rel"]
        notes = re.sub('\s+', ' ', notes)
    except:
        notes = ""

    try:
        short_title = row.find_all("td")[1].find("a").get_text().strip()
        short_title = re.sub('\s+', ' ', short_title)
    except:
        short_title = ""

    pdf_url = row.find_all("td")[1].find("a")["href"]
    pdf_full_url = "http://laws.bahamas.gov.bs" + pdf_url
    (title_slug, _type) = parse_pdf_url(pdf_url)

    pdf_url_local = pdf_local_url(_type, year, item_num, title_slug)

    date_index = 2
    if total_tds == 4:
        date_index = 3
        category = row.find_all("td")[2].get_text().strip()
    else:
        date_index = 2

    date_commenced = row.find_all("td")[date_index].get_text().strip()
    status = "Not Enforced"

    if date_commenced in ["NOT IN FORCE"]:
        status = "Active"

    if date_commenced in ["NOT IN FORCE", "Repealed Legislation"]:
        date_commenced = ""
    else:
        date_commenced = dateparser.parse(date_commenced)

    # Download PDF file in pdfs/ folder
    pdf_download_path = "pdfs/"+ pdf_url_local.split(title_slug)[0]
    if not os.path.exists(os.path.dirname(pdf_download_path)):
        try:
            os.makedirs(os.path.dirname(pdf_download_path))
        except OSError as exc: # Guard against race condition
                print(str(exc))
    try:
        urllib.urlretrieve (pdf_full_url, pdf_download_path+title_slug+".pdf")
    except:
        print("pdf downloading failed")

    if total_tds == 4:
        return [short_title, title_slug, _type, year, number, notes, pdf_url_local, date_commenced, status, migrated, created_at, category]
    else:
        return [short_title, title_slug, _type, year, number, notes, pdf_url_local, date_commenced, status, migrated, created_at]
