import common_actions
import pythonLib
import datetime


def __post_data(year):
    return {
        'year': year
    }


def parse_results(soup):
    form = soup.find("form", {"id": "adminForm"})
    data_rows = form.find("table").find("tbody").find_all("tr")
    results = list()

    for row in data_rows:
        parsed_data = common_actions.legistation_parsing(row)
        results.append(tuple(parsed_data))

    pythonLib.insert_data(results, bulk_insert=True)


def main(HOME_URL):
    now = datetime.datetime.now()
    years = range(1920, now.year)
    years.append(now.year)
    for year in years:
        year = str(year)
        print("Year: " + year)
        post_data = __post_data(year)
        try:
            soup = common_actions.make_request(HOME_URL, post_data)
            parse_results(soup)
        except Exception as err:
            print(str(err))
            pass

