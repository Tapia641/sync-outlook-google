import win32com.client
import logging


class Outlook:
    __slots__ = ['appointments', 'begin', 'end']

    def __init__(self, begin, end) -> None:
        self.appointments = []
        cal = self.get_calendar(begin, end)
        self.get_appointments(cal)

    def get_calendar(self, begin, end):
        outlook = win32com.client.Dispatch(
            'Outlook.Application').GetNamespace('MAPI')
        calendar = outlook.getDefaultFolder(9).Items
        calendar.IncludeRecurrences = True
        calendar.Sort('[Start]')

        restriction = "[Start] >= '" + begin.strftime(
            '%m/%d/%Y') + "' AND [END] <= '" + end.strftime('%m/%d/%Y') + "'"
        calendar = calendar.Restrict(restriction)
        return calendar

    def get_appointments(self, calendar, subject_kw=None, exclude_subject_kw=None, body_kw=None):
        if subject_kw == None:
            appointments = [app for app in calendar]
        else:
            appointments = [
                app for app in calendar if subject_kw in app.subject]
        if exclude_subject_kw != None:
            appointments = [
                app for app in appointments if exclude_subject_kw not in app.subject]
        # cal_subject = [app.subject for app in appointments]
        # cal_start = [app.start for app in appointments]
        # cal_end = [app.end for app in appointments]
        # cal_body = [app.body for app in appointments]
        for app in appointments:
            if app:
                logging.info(f"{app.start}, {app.end}, {app.subject}")
                self.appointments.append([app.start, app.end, app.subject])
