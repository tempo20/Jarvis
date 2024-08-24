# %%
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os.path
import datetime
import sys
import os
import configparser
config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file_path)
credentials_file_path = config.get('file_paths', 'file_path_credentials')
email = config.get('emails', 'email')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCOPES = ["https://www.googleapis.com/auth/calendar"]
# %%


def get_creds():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds
# %%


def get_events():
    creds = get_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        event_result = service.events().list(calendarId='primary', timeMin=now,
                                             maxResults=5, singleEvents=True, orderBy='startTime').execute()
        events = event_result.get('items', [])
        if not events:
            print('No upcoming events found!')
            return
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except HttpError as error:
        print('an error has occured:', error)

# %%


def create_event(summary, location, description, colorId, dateTime, timeZone, end, attendees):
    creds = get_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': summary,
            'locaton': location,
            'description': description,
            'colorId': colorId,
            'start': {
                'dateTime': dateTime,
                'timeZone': timeZone
            },
            'end': {
                'dateTime': dateTime,
                'timeZone': timeZone
            },
            'recurrence': ['RRULE:FREQ=DAILY;COUNT=3'],
            'attendees': [
                {'email': email}
            ]
        }
        event = service.events().insert(calendarID='primary', body=event).execute()
        print(f"event created: {event.get('htmllink')}")
    except HttpError as error:
        print('an error has occured:', error)

# %%


def delete_event(event_id):
    creds = get_creds()
    try:
        service = build('calendar', 'v3', credentials=creds)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event with ID {event_id} deleted successfully.")
    except HttpError as error:
        print('An error occurred:', error)
