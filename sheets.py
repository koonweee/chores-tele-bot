import httplib2
from apiclient import discovery
import pytz
from pytz import timezone
import datetime
import pygsheets
tz = pytz.utc

sheets_api_key = 'AIzaSyBeh_CnQNh8-_041kUcKUbPBTgBSgMcYVs' # hide as secret'
spreadsheet_id = '1tiYLMKpJFCfbTie_yqzmJYoE9IWWd4545BW9Wviyt_U' # hide as secret
discovery_url = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
service = discovery.build(
        'sheets',
        'v4',
        http=httplib2.Http(),
        discoveryServiceUrl=discovery_url,
        developerKey=sheets_api_key)
gc = pygsheets.authorize(service_file='/Users/jtkw/Desktop/tele-bot.json')
sh = gc.open('Chores')
wks = sh[0]



def getRow(queryDate): # return row of interest
    # get the first column
    firstColumRange = 'Schedule!A1:A50'
    firstColumnResult = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=firstColumRange).execute()
    firstColumnValues = firstColumnResult.get('values', [])
    date_row = {}
    for index, row in enumerate(firstColumnValues):
        split = row[0].split(", ")
        dateStr = split[1] if len(split) > 1 else split[0]
        date_row[dateStr] = index + 1
    return date_row[queryDate]



def getChores(queryDate):
    row = getRow(queryDate)
    choresRange = 'Schedule!B{}:F{}'.format(row, row)
    choresResult = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=choresRange).execute()
    choresValues = choresResult.get('values', [])[0]
    return choresValues

def updateDoneChore(date, choreIndex):
    row = getRow(dateToQuery(date))
    column = chr(ord('`')+choreIndex+1)
    updateRange = '{}{}'.format(column, row)
    curName = wks.cell(updateRange).value
    wks.update_value(updateRange, '{} - DONE'.format(curName))

def getWeekChores(date):
    # convert date to nearest-previous monday
    
    print('Looking for: {}'.format(dateToQuery(date)))
    return getChores(dateToQuery(date))

def dateToQuery(date):
    queryDay = int(datetime.datetime.strftime(date, '%w')) # 0 = sun, 1 = mon etc
    offsetDays = 6 if queryDay == 0 else queryDay - 1 if queryDay != 1 else 7
    mondayDate = date - datetime.timedelta(offsetDays)
    return mondayDate.strftime('%-d %B %Y')

