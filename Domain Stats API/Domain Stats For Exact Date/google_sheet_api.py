import gspread
from dotenv import load_dotenv
from time import sleep

load_dotenv()

sa = gspread.service_account(filename='credentials.json')
sh = sa.open("SpyFu")
wks = sh.worksheet("Domain_Stats_For_Exact_Date")


def append_data_to_sheet(data) -> None:
    """Append data to Google Sheets"""
    for row in data:
        wks.append_row(row)
        sleep(1.1)
    if len(data) > 0:
        print(f"Appended {len(data)} rows to Google Sheets.")
    else:
        print("No data to append.")
