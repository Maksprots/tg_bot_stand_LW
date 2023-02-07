import os
import datetime
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.auth.exceptions import MutualTLSChannelError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error

from config import ConfigDrive as cd
from config import ConfigSheets as cs
from exceptions import OpenCreds, BuildService, LoadHttp


class GoogleDrive:
    def __init__(self,
                 credentials_path=cd.CREDENTIALS_PATH,
                 scopes=cd.SCOPES):
        if not os.path.exists(credentials_path):
            raise OpenCreds('File is not exist')

        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )
        try:
            self.service = build(serviceName='drive',
                                 version=cd.DRIVE_VERSION,
                                 credentials=creds,
                                 static_discovery=False)
        except MutualTLSChannelError:
            raise BuildService('Build is not successful')

    def load_file(self, file_path: str, filename: str) -> str:
        """Function load your file to drive folder (config).
        return link to your file in web.
        """
        file_metadata = {
            'name': filename,
            'parents': [cd.folder_id]
        }
        media = MediaFileUpload(file_path,
                                mimetype='application/octet-stream',
                                resumable=True)
        try:
            response = self.service.files() \
                .create(body=file_metadata,
                        media_body=media,
                        fields='id').execute()
        except HttpError:
            raise LoadHttp('Response is not 2XX')
        except HttpLib2Error:
            raise LoadHttp('Transport err')

        file_id = response.get('id')
        return cd.file_link.format(file_id)


class GoogleSheets:
    def __init__(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            cs.CREDENTIALS_PATH,
            cs.SCOPES)
        creds = flow.run_local_server(port=0)
        service = build('sheets',
                        cs.SHEETS_VERSION,
                        credentials=creds)

        self.sheet = service.spreadsheets()

    def write_requaest_to_table(self, email_address, link_to_folder):
        """"Function write row to google table ( date, mail, link to zip)
        """
        number_of_current_string = len(self.sheet.values()
                                       .get(spreadsheetId=cs.SPREADSHEET_ID,
                                            range=cs.rnage_to_chek_len).execute()
                                       .get('values'))

        today = datetime.datetime.today()
        values = [[
            today.strftime("%d.%m.%Y %H:%M:%S"),
            email_address,
            link_to_folder
        ], ]

        body = {
            'values': values
        }
        result = self.sheet.values().append(
            spreadsheetId=cs.SPREADSHEET_ID, range="A:C",
            valueInputOption="USER_ENTERED", body=body).execute()
        print(f"{(result.get('updates').get('updatedCells'))} ")


if __name__ == "__main__":
    # d = GoogleDrive()
    # print(d.load_file(file_path='test_load.html', filename="test2_maks.html"))
    d = GoogleSheets()
    d.write_requaest_to_table('aafd', 'afd')
