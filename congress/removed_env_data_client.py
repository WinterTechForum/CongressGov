import csv
import requests
import logging


fh = logging.FileHandler('congress_api.log')
fh.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

API_KEY = ""
RANGE_NAME = 'Sheet1'
CSV_FILE_PATH = "cache/Enviro Fed Web Tracker - 2025-.csv"

url = "https://docs.google.com/spreadsheets/d/1eqZA-LDMRyoRLSRh_S_4MQuX6YXhDeOLqKMEzMLP-2Y/edit?gid=1720528264#gid=1720528264"

class RemovedEnvDataClient:
    # Untested
    def download_sheet_as_csv():
        """Downloads the Google Sheet as a CSV and saves it to the local file system."""
        # url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE_NAME}?key={API_KEY}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Check if there's any data in the sheet
            if 'values' in data and data['values']:
                # Write the CSV file to the local file system
                with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(data['values'])

                print(f"Data downloaded and saved as {CSV_FILE_PATH}")
            else:
                print('No data found.')
        else:
            print(f"Error fetching data: {response.status_code}")

    @staticmethod
    def read_and_parse_csv():
        """Reads the downloaded CSV file and parses the data."""
        try:
            with open(CSV_FILE_PATH) as file:
                reader = csv.DictReader(file)
                parsed_data = [row for row in reader]
                return parsed_data
        except FileNotFoundError:
            print(f"File {CSV_FILE_PATH} not found.")
            return None