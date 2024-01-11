from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread

# Google Cloud Function entry point
def main(request):
    # Setup the Calendar API
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 
              'https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'path/to/service/account.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    calendar_service = build('calendar', 'v3', credentials=credentials)
    sheet_service = gspread.authorize(credentials)

    # Extract events from Calendar
    events_result = calendar_service.events().list(
        calendarId='primary', 
        timeMin='2024-01-01T00:00:00Z',  # Modify as needed
        timeMax='2024-01-31T23:59:59Z',  # Modify as needed
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    # Write to Google Sheet
    # Open the sheet and write data
    sheet = sheet_service.open("Your Google Sheet Name").sheet1
    for event in events:
        # Event data extraction
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')

        # Write to sheet
        sheet.append_row([start, summary])

    return "Events Exported Successfully"

# Trigger this function from Google Cloud Scheduler
