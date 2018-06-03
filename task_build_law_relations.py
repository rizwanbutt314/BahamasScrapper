import common_actions
import pythonLib
import string
import datetime


def __post_data(year, datetime):
    return {
        'submit4': year,
        'pointintime': datetime
    }


def parse_results(soup):
    form = soup.find("form", {"id": "adminForm"})
    data_rows = form.find("table").find("tbody").find_all("tr")

    for row in data_rows:
        parsed_data = common_actions.legistation_parsing(row)
        category_id = pythonLib.handle_category(parsed_data[-1])
        (legistation_id, legistation_type) = pythonLib.handle_legistation(category_id, parsed_data)

        pythonLib.handle_amendments(legistation_id, parsed_data[0], legistation_type)


def main(HOME_URL):
    alphabets = string.ascii_uppercase
    today_date = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
    for alphabet in list(alphabets):
        print("Alphabet: " + alphabet)
        post_data = __post_data(alphabet, today_date)
        try:
            soup = common_actions.make_request(HOME_URL, post_data)
            parse_results(soup)
        except Exception as err:
            print(str(err))
            pass


