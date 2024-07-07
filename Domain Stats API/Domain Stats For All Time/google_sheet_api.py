import gspread
from dotenv import load_dotenv
from time import sleep

load_dotenv()

service_account = gspread.service_account(filename='expanded-guide-392113-3d87472fc006.json')
sheet_name = service_account.open("SpyFu")
work_sheet_name = sheet_name.worksheet("Domain stats for all time")


def append_data_to_sheet(data) -> None:
    """Append data to Google Sheets"""
    for row in data:
        work_sheet_name.append_row(row)
        sleep(1.1)
    if len(data) > 0:
        print(f"Appended {len(data)} rows to Google Sheets.")
    else:
        print("No data to append.")
