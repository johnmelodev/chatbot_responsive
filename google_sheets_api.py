import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime


class GoogleSheets():
    def __init__(self, service=None):
        self.service = service

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        SAMPLE_SPREADSHEET_ID = "1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU"
        SAMPLE_RANGE_NAME = "Incomes!A2:D4"

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            self.service = build("sheets", "v4", credentials=creds)
        except HttpError as err:
            print(err)

    def insert_incomes(self, value, category, comments):
        try:
            body = {"values": [[value, category, comments,
                                datetime.now().strftime('%d/%m/%Y')]]}
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                    range='Incomes!A2:D2',
                    valueInputOption='USER_ENTERED',
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def insert_outcomes(self, value, classification, type, comments):
        try:
            body = {"values": [[value, classification, type, comments,
                                datetime.now().strftime('%d/%m/%Y')]]}
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                    range='Outcomes!A2:E2',
                    valueInputOption='USER_ENTERED',
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def insert_transfers(self, value, from_account, to_account, comments):
        try:
            body = {"values": [[value, from_account, to_account, comments,
                                datetime.now().strftime('%d/%m/%Y')]]}
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                    range='Transfers!A2:E2',
                    valueInputOption='USER_ENTERED',
                    body=body,
                )
                .execute()
            )
            print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
            return result

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def show_report(self, column):
        try:
            sheet = self.service.spreadsheets()
            if column == 'Total Incomes':
                results = sheet.values().get(spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                                             range='Report!A2:A').execute()
                values = results.get('values', [])
                # if you want more values change the way you access the table in the code below:
                print(values)
                print(values[0][0])
                return values[0][0]
            elif column == 'Total Outcomes':
                results = sheet.values().get(spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                                             range='Report!B2:B').execute()
                values = results.get('values', [])
                # if you want more values change the way you access the table in the code below:
                print(values)
                print(values[0][0])
                return values[0][0]
            elif column == 'Total Transfers':
                results = sheet.values().get(spreadsheetId='1H8fLpCXezIMDmuqI_uk36B95fgDF9LT2CoubJ8liMAU',
                                             range='Report!C2:C').execute()
                values = results.get('values', [])
                # if you want more values change the way you access the table in the code below:
                print(values)
                print(values[0][0])
                return values[0][0]
        except Exception as error:
            print(error)


# google_sheets_api = GoogleSheets()
# google_sheets_api.insert_incomes(1500, 'Salary', 'First salary')
# google_sheets_api.insert_outcomes(500, 'fix', 'pix', 'car repair')
# google_sheets_api.insert_transfers(500, 'fix', 'pix', 'car repair')
# google_sheets_api.show_report('Total Incomes')
# google_sheets_api.show_report('Total Outcomes')
# google_sheets_api.show_report('Total Transfers')
