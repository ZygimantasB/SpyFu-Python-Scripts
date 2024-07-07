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
                [url, "No data", "No data", current_year, current_month, current_day, 'No Data', 'No Data',
                 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data',
                 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data', 'No Data'])
            continue
        for item in results:
            keyword = item['keyword']
            search_volume = item['searchVolume']
            top_ranked_url = item['topRankedUrl']
            rank_change = item['rankChange']
            keyword_difficulty = item['keywordDifficulty']
            broad_cost_per_click = item['broadCostPerClick']
            phrase_cost_per_click = item['phraseCostPerClick']
            exact_cost_per_click = item['exactCostPerClick']
            seo_clicks = item['seoClicks']
            seo_clicks_change = item['seoClicksChange']
            total_monthly_clicks = item['totalMonthlyClicks']
            percent_mobile_searches = item['percentMobileSearches']
            percent_desktop_searches = item['percentDesktopSearches']
            percent_not_clicked = item['percentNotClicked']
            percent_paid_clicks = item['percentPaidClicks']
            percen_organic_clicks = item['percentOrganicClicks']
            broad_monthly_cost = item['broadMonthlyCost']
            phrase_monthly_cost = item['phraseMonthlyCost']
            exact_monthly_cost = item['exactMonthlyCost']
            paid_competitors = item['paidCompetitors']
            ranking_homepages = item['rankingHomepages']
            sheet_data.append(
                [url, keyword, search_volume, current_year, current_month, current_day, top_ranked_url, rank_change,
                 keyword_difficulty, broad_cost_per_click, phrase_cost_per_click, exact_cost_per_click, seo_clicks,
                 seo_clicks_change, total_monthly_clicks, percent_mobile_searches, percent_desktop_searches,
                 percent_not_clicked, percent_paid_clicks, percen_organic_clicks, broad_monthly_cost,
                 phrase_monthly_cost, exact_monthly_cost, paid_competitors, ranking_homepages])

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
