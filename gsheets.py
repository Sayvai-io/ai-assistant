#google sheets api
import os
import gspread
from typing import List, Tuple, Dict, Any
from oauth2client.service_account import ServiceAccountCredentials
from constants import SPREADSHEET_SCOPES, READ_ONLY_SPREADSHEET_SCOPES

SCOPES = SPREADSHEET_SCOPES
READ_ONLY_SPREADSHEET_SCOPES = READ_ONLY_SPREADSHEET_SCOPES

class GSheets:
    """Class for Google Sheets"""
    def __init__(self) -> None:
        self.creds = None
        self.sheet = None
        if os.path.exists('sheets_token.json'):
            self.creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            self.creds = self.get_credentials()
        self.sheet = gspread.authorize(self.creds)
        
    def get_credentials(self) -> str:
        """Gets the credentials for the user"""
        # if sheets_token.json exists, use that if not, create a new one
        if os.path.exists('sheets_token.json'):
            self.creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_token.json', SCOPES)
        else:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
        return "Credentials obtained"
    
    def get_sheet(self, sheet_name : str) -> str:
        """Gets the sheet for the user"""
        try:
            self.sheet = self.sheet.open(sheet_name)
            return "Sheet obtained"
        except Exception as e:
            print(e)
            return "Error occured"
    
    def get_worksheet(self, sheet_name : str, worksheet_name : str) -> str:
        """Gets the worksheet for the user"""
        try:
            self.sheet = self.sheet.open(sheet_name).worksheet(worksheet_name)
            return "Worksheet obtained"
        except Exception as e:
            print(e)
            return "Error occured"
        
    def get_all_values(self, sheet_name : str, worksheet_name : str) -> List[List[str]]:
        """Gets all the values from the worksheet"""
        try:
            self.get_worksheet(sheet_name, worksheet_name)
            return self.sheet.get_all_values()
        except Exception as e:
            print(e)
            return "Error occured"
        
    def get_all_records(self, sheet_name : str, worksheet_name : str) -> List[Dict[str, Any]]:
        """Gets all the records from the worksheet"""
        try:
            self.get_worksheet(sheet_name, worksheet_name)
            return self.sheet.get_all_records()
        except Exception as e:
            print(e)
            return "Error occured"
        
    def get_value(self, sheet_name : str, worksheet_name : str, cell : str) -> str:
        """Gets the value from the worksheet"""
        try:
            self.get_worksheet(sheet_name, worksheet_name)
            return self.sheet.acell(cell).value
        except Exception as e:
            print(e)
            return "Error occured"
        
    def search_value(self, sheet_name : str, worksheet_name : str, value : str) -> List[List[str]]:
        """Searches the value in the worksheet"""
        try:
            self.get_worksheet(sheet_name, worksheet_name)
            return self.sheet.findall(value)
        except Exception as e:
            print(e)
            return "Error occured"
        
    def update_value(self, sheet_name : str, worksheet_name : str, cell : str, value : str) -> str:
        """Updates the value in the worksheet"""
        try:
            self.get_worksheet(sheet_name, worksheet_name)
            self.sheet.update_acell(cell, value)
            return "Value updated"
        except Exception as e:
            print(e)
            return "Error occured"
        
    def create_sheet(self, sheet_name : str) -> str:
        """Creates a new sheet"""
        try:
            self.sheet.create(sheet_name)
            return "Sheet created"
        except Exception as e:
            print(e)
            return "Error occured"
        
    def create_worksheet(self, sheet_name : str, worksheet_name : str) -> str:
        """Creates a new worksheet"""
        try:
            self.get_sheet(sheet_name)
            self.sheet.add_worksheet(worksheet_name)
            return "Worksheet created"
        except Exception as e:
            print(e)
            return "Error occured"
        
    def delete_sheet(self, sheet_name : str) -> str:
        """Deletes the sheet"""
        try:
            self.sheet.del_worksheet(self.sheet.worksheet(sheet_name))
            return "Sheet deleted"
        except Exception as e:
            print(e)
            return "Error occured"
        
    def delete_worksheet(self, sheet_name : str, worksheet_name : str) -> str:
        """Deletes the worksheet"""
        try:
            self.get_sheet(sheet_name)
            self.sheet.del_worksheet(self.sheet.worksheet(worksheet_name))
            return "Worksheet deleted"
        except Exception as e:
            print(e)
            return "Error occured"
    
    def get_sheet_names(self, sheet_name : str) -> List[str]:
        """Gets the sheet names"""
        try:
            self.get_sheet(sheet_name)
            return self.sheet.worksheets()
        except Exception as e:
            print(e)
            return "Error occured"
        
# if __name__ == "__main__":
#     gsheets = GSheets()
#     print(gsheets.get_credentials())
#     print(gsheets.create_sheet("Test2"))
#     print(gsheets.create_worksheet("Test2", "Sheet2"))
#     print(gsheets.get_sheet("Test"))
#     print(gsheets.get_worksheet("Test", "Sheet1"))
#     print(gsheets.get_all_values("Test", "Sheet1"))
#     print(gsheets.get_all_records("Test", "Sheet1"))
#     print(gsheets.get_value("Test", "Sheet1", "A1"))
#     print(gsheets.search_value("Test", "Sheet1", "A1"))
#     print(gsheets.update_value("Test", "Sheet1", "A1", "Test"))
    
#     print(gsheets.delete_sheet("Test2"))
#     print(gsheets.delete_worksheet("Test2", "Sheet2"))
#     print(gsheets.get_sheet_names("Test"))