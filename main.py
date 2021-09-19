from google_setup.google_calendar import GoogleCalendar

if __name__ == "__main__":
    
    # We call the service of Google with the API
    service = GoogleCalendar().service

    # Getting list of calendars
    calendars_result = service.calendarList().list().execute()

    print(calendars_result)

    # calendars = calendars_result.get('items', [])

    # if not calendars:
    #     print('No calendars found.')
    # for calendar in calendars:
    #     summary = calendar['summary']
    #     id = calendar['id']
    #     primary = "Primary" if calendar.get('primary') else ""
    #     print("%s\t%s\t%s" % (summary, id, primary))