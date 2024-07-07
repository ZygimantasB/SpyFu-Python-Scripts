from os import getenv
from dotenv import load_dotenv
from google_sheet_api import append_data_to_sheet
from spy_fu_api import SpyFuAPI
from data import data as spy_fu_data
from datetime import datetime


def prepare_data_for_sheets(spy_fu_api) -> list:
    """Transforms the data into a format suitable for Google Sheets."""
    sheet_data = []
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().strftime("%Y")
    current_day = datetime.now().strftime("%d")

    for url, results in spy_fu_api.items():
        if not results:
            print(f"No results for {url}")
            sheet_data.append(
                [url, current_year, current_month, current_day, "No data", "No data", "No data", "No data"])
            continue
        for item in results:

            search_month = item['searchMonth'] ##
            search_year = item['searchYear'] ##
            monthly_paid_clicks = item['monthlyPaidClicks'] ##
            monthly_organic_clicks = item['monthlyOrganicClicks'] ##

            sheet_data.append(
                [url, current_year, current_month, current_day, search_year, search_month,
                 monthly_paid_clicks, monthly_organic_clicks])

    return sheet_data


def main() -> None:
    """
    main function
    """
    load_dotenv()
    spyfu = SpyFuAPI(
        api_url=getenv("API_URL"),
        api_id=getenv("API_KEY"),
        secret_key=getenv("SECRET_KEY"),
        filename='config.json'
    )

    spy_fu_api = spyfu.get_spy_fu_data()

    if spy_fu_data:
        sheet_data = prepare_data_for_sheets(spy_fu_api)
        append_data_to_sheet(sheet_data)
    else:
        print("No data found.")


if __name__ == "__main__":
    main()
