"""
Author : Luis Enrique Hernández Tapia
Version: 1.0
"""

from configparser import ConfigParser
import os
from google_setup.cal_setup import get_calendar_service

class GoogleCalendar:

    # More info: https://developers.google.com/calendar/api/quickstart/python
    __slots__ = ['service', 'client_secret_file', 'api_name', 'scopes']

    def __init__(self) -> None:
        self.read_variables()

    def read_variables(self) -> None:
        configs = ConfigParser()
        configs.read('config.ini')
        self.client_secret_file = configs.get('google', 'CLIENT_SECRET_FILE')
        self.api_name = configs.get('google', 'API_NAME')
        self.scopes = configs.get('google', 'SCOPES')
        self.service = get_calendar_service(self.scopes,self.client_secret_file)


    def get_calendars(self):
        print('Getting list of calendars')

        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        if not calendars:
            print('No calendars found.')
        for calendar in calendars:
            summary = calendar['summary']
            id = calendar['id']
            primary = "Primary" if calendar.get('primary') else "No"
            print("Name:",summary, "ID", id, " Is primary: ", primary)
    
    def get_primary_calendar(self):
        calendar = self.service.calendars().get(calendarId='primary').execute()
        print (calendar['summary'])

    def get_all_events(self):
        page_token = None
        
        calendars_result = self.service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])

        for calendar in calendars:
            id = calendar['id']
            while True:
                events = self.service.events().list(calendarId=id, pageToken=page_token).execute()
                for event in events['items']:
                    print(event['summary'])
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
    def create_event(self)-> None:
        event = {
            'summary': 'Google I/O 2015',
            'location': '800 Howard St., San Francisco, CA 94103',
            'description': 'A chance to hear more about Google\'s developer products.',
            'start': {
                'dateTime': '2021-09-19T09:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': '2021-09-19T17:00:00-07:00',
                'timeZone': 'America/Los_Angeles',
            },
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            'attendees': [
                {'email': 'lpage@example.com'},
                {'email': 'sbrin@example.com'},
            ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #     {'method': 'email', 'minutes': 24 * 60},
            #     {'method': 'popup', 'minutes': 10},
            #     ],
            # },
            }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

