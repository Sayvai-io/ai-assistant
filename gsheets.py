#google sheets api
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from constants import SPREADSHEET_SCOPES, READ_ONLY_SPREADSHEET_SCOPES

SCOPES = SPREADSHEET_SCOPES
READ_ONLY_SPREADSHEET_SCOPES = READ_ONLY_SPREADSHEET_SCOPES

class GSheets:
    """Class for Google Sheets"""
    def __init__(self) -> None:
        pass    