from googleapiclient.discovery import build
from google.oauth2 import service_account

# AIzaSyD9SHYhSOBonWLG7YV1wZyvaAdZh1XuXH0

# The ID and range of a sample spreadsheet.
spreadsheet_id = '112QAhW9TLX2O_tElYZFgSNEfRy-OVD0HhaH77EToGiw'

credentials = service_account.Credentials.from_service_account_file('credentials.json')
service = build('sheets', 'v4', credentials=credentials, cache_discovery='.google_cache')
sheet = service.spreadsheets()


def main():
    values = [[i*j for j in range(10)] for i in range(5)]
    body = {
        'values': values
    }
    range_name = 'A1:J10'
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED',
        body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':
    main()