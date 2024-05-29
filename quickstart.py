import datetime
import os.path
from dateutil import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import numpy as np
load_dotenv(verbose=True, override=True)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = os.getenv('RANGE_NAME')


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        today = datetime.date.today()
        month = today.month
        nextMonth = month + 1
        year = today.year
        nextYear = year
        day = today.day
        dateString = f"{year}-{month}-{day}"

        # reset the next month and update the year if we are in december
        if (nextMonth > 12):
            nextMonth = 1
            nextYear += 1

        if (month < 10):
            month = '0' + str(month)

        if (nextMonth < 10):
            nextMonth = '0' + str(nextMonth)

        weekDays = np.busday_count(
            f"{year}-{month}", f"{nextYear}-{nextMonth}")

        if not values:
            updateValues = [[dateString, str(weekDays)]]
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                  valueInputOption="USER_ENTERED", body={"values": updateValues}).execute()
            print("No data found. The current month has been added!")
            return

        isMonthAdded = False

        for row in values:
            # Print the rows
            monthFromRow = datetime.datetime.strptime(
                row[0], "%Y-%m-%d").date().month

            if int(month) == monthFromRow:
                isMonthAdded = True

        if not isMonthAdded:
            updateValues = [[dateString, str(weekDays)]]
            sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                                  valueInputOption="USER_ENTERED", body={"values": updateValues}).execute()
            print(f"{dateString} appended!")
            return

        print("Nothing to add!")
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
