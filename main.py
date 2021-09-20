from google_setup.google_calendar import GoogleCalendar
from outlook_setup.outlook import Outlook
from datetime import datetime, timedelta

if __name__ == "__main__":
    
    # We call the service of Google with the API
    google = GoogleCalendar()
    google.get_primary_calendar()
    # google.delete_primary_events()

    begin = datetime.now()
    end = begin + timedelta(days=7)

    outlook = Outlook(begin, end)
    appointments = outlook.appointments

    for app in appointments:
        google.create_event(app[0], app[1], app[2], google.timezone)
  

