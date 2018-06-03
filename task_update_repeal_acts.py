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
    con, cur = pythonLib.database_connection()

    for row in data_rows:
        parsed_data = common_actions.legistation_parsing(row)
        category_id = pythonLib.handle_category(parsed_data[-1])
        legistation_id, legistation_type = pythonLib.handle_legistation(category_id, parsed_data)

        pythonLib.update_repeal_legistation(con, cur, legistation_id, parsed_data[7])

    con.commit()
    con.close()

def main(HOME_URL):
    try:
        soup = common_actions.make_get_request(HOME_URL)
        parse_results(soup)
    except Exception as err:
        print(str(err))
        pass


