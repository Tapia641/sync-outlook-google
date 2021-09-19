"""
Author : Luis Enrique Hernández Tapia
Version: 1.0
"""

from configparser import ConfigParser
import os
from google_setup.cal_setup import get_calendar_service

class GoogleCalendar:
    # More info: https://developers.google.com/calendar/api/quickstart/python

    __slots__ = ['service', 'client_secret_file', 'api_name', 'api_version', 'scopes']

    def __init__(self) -> None:
        self.read_variables()
        # self.do_connection()

    def read_variables(self) -> None:
        configs = ConfigParser()
        configs.read(f'{os.path.dirname(os.path.abspath(__file__))}\\config.ini')
        print(f'{os.path.dirname(os.path.abspath(__file__))}\\config.ini')
        self.client_secret_file = configs.get('google', 'CLIENT_SECRET_FILE')
        self.api_name = configs.get('google', 'API_NAME')
        # self.api_version = configs.get('google', 'API_VERSION')
        self.scopes = configs.get('google', 'SCOPES')
        self.service = get_calendar_service(self.scopes,self.client_secret_file)

# def main():

    # def do_connection(self) -> None:
    #     service = Create_Service(self.client_secret_file,self.api_name,self.api_version,self.scopes)
    #     colors = service.colors().get().execute()
    #     print(colors)

        