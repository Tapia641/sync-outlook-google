"""
Author : Luis Enrique Hernández Tapia
Version: 1.0
"""

from configparser import ConfigParser
import logging
from time import time
from google_setup.cal_setup import get_calendar_service
import logging


class GoogleCalendar:

    # More info: https://developers.google.com/calendar/api/quickstart/python
    __slots__ = ['service', 'client_secret_file',
                 'api_name', 'scopes', 'timezone']

    def __init__(self) -> None:
        self.read_variables()

    def read_variables(self) -> None:
        configs = ConfigParser()
        configs.read('config.ini')
        self.client_secret_file = configs.get('google', 'CLIENT_SECRET_FILE')
        self.api_name = configs.get('google', 'API_NAME')
        self.scopes = configs.get('google', 'SCOPES')
        self.service = get_calendar_service(
            self.scopes, self.client_secret_file)

    def get_calendars(self):
        logging.info(f'Getting list of calendars')

        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            logging.info(f'No calendars found.')
        for calendar in calendars:
            summary = calendar['summary']
            id = calendar['id']
            primary = "Primary" if calendar.get('primary') else "No"
            logging.info(f"Name:{summary}, ID {id}, Is primary: {primary}")

    def get_primary_calendar(self):
        calendar = self.service.calendars().get(calendarId='primary').execute()
        logging.info(f"{calendar['summary']}, {calendar['timeZone']}")
        self.timezone = calendar['timeZone']

    def get_all_events(self):
        page_token = None

        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        for calendar in calendars:
            id = calendar['id']
            while True:
                events = self.service.events().list(calendarId=id, pageToken=page_token).execute()
                for event in events['items']:
                    logging.info(f"{event['summary']}")
                page_token = events.get('nextPageToken')
                if not page_token:
                    break

    def get_primary_events(self):
        page_token = None

        while True:
            events = self.service.events().list(
                calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                logging.info(f"{event['summary']}, {event['id']}")
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def create_event(self, start, end, subject, timezone) -> None:
        event = {
            'summary': subject,
            'location': 'Nokia',
            'description': '',
            'start': {
                'dateTime': start.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 5}
                ]
            }
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f'Event created: %s' % (event.get('htmlLink')))

    def delete_primary_events(self):
        page_token = None

        while True:
            events = self.service.events().list(
                calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                self.service.events().delete(calendarId='primary',
                                             eventId=event['id']).execute()
                logging.info(f"{event['summary']} has been deleted.")
            page_token = events.get('nextPageToken')
            if not page_token:
                break
