from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml

# added from https://developers.google.com/identity/protocols/oauth2/service-account#python

from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


credentials= None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
# https://docs.google.com/spreadsheets/d/1EP5vIR5Im0UDW_0CrGONS6NxvV8jDN9JtbbXhWWE6sY/edit#gid=0
SAMPLE_SPREADSHEET_ID = '1EP5vIR5Im0UDW_0CrGONS6NxvV8jDN9JtbbXhWWE6sY'
#SAMPLE_RANGE_NAME = 'Class Data!A2:E'


service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sheet2!A1:D11").execute()
values = result.get('values', [])
print(values)


####### writing in sheet from csv

df=pd.read_csv('US_Interest_rate.csv',index_col=0)
df=df.reset_index()
df=round(df,2)
df=df.fillna(method="ffill")
lol = [df.columns.tolist()] + df.values.tolist()

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet2!A1", valueInputOption="USER_ENTERED", body={'values':lol}).execute()
#print(request)



####### writing in sheet from URL
def dfFromURL(url, tableNumber=1):
    soup = BeautifulSoup(requests.get(url).content, 'lxml') # Parse the HTML as a string
    tables = soup.find_all('table')
    # check table number is within number of tables on the page
    assert len(tables) >= tableNumber
    return pd.read_html(str(tables[tableNumber-1]))[0]

SP500=dfFromURL('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
SP500=SP500.fillna(method="ffill")
lol2 = [SP500.columns.tolist()] + SP500.values.tolist()
request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet3!A1", valueInputOption="USER_ENTERED", body={'values':lol2}).execute()