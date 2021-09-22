from google_setup.google_calendar import GoogleCalendar
from outlook_setup.outlook import Outlook
from datetime import datetime, timedelta
import logging
import argparse


if __name__ == "__main__":

    # CHECK IF THE ARGUMENTS ARE PRESENT
    parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--sync', action='store_true', required=False)

    # GET ALL ARGUMENTS
    # args = parser.parse_args()

    # Do not touch this is for logs and outputs during the execution
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # We call the service of Google with the API
    google = GoogleCalendar()
    google.get_primary_calendar()
    google.delete_primary_events()

    begin = datetime.now()
    end = begin + timedelta(days=7)

    outlook = Outlook(begin, end)
    appointments = outlook.appointments

    for app in appointments:
        if "Canceled" not in app[2]:
            google.create_event(app[0], app[1], app[2], google.timezone)
