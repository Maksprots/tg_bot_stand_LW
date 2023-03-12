import os
import datetime
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.auth.exceptions import MutualTLSChannelError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error

from google_api.config import ConfigDrive as cd
from google_api.config import ConfigSheets as cs
from google_api.exceptions import OpenCreds, BuildService, LoadHttp
from bot.create_bot import logger

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
    @logger.catch()
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
    @logger.catch()
    def __init__(self, credentials_path=cs.CREDENTIALS_PATH,
                 scopes=cs.SCOPES):
        if not os.path.exists(credentials_path):
            raise OpenCreds('File is not exist')
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path,
            scopes)
        creds = flow.run_local_server(port=0)
        try:
            service = build('sheets',
                            cs.SHEETS_VERSION,
                            credentials=creds)

            self.sheet = service.spreadsheets()
        except MutualTLSChannelError:
            raise BuildService("buil sheets api error")

    @logger.catch()
    def write_request_to_table(self, email_address, link_to_folder):
        """"Function write row to google table ( date, mail, link to zip)
        """

        today = datetime.datetime.today()
        values = [[
            today.strftime("%d.%m.%Y %H:%M:%S"),
            email_address,
            link_to_folder
        ], ]

        body = {
            'values': values
        }
        try:
            result = self.sheet.values().append(
                spreadsheetId=cs.SPREADSHEET_ID, range="A:C",
                valueInputOption="USER_ENTERED", body=body).execute()
        except HttpError:
            raise LoadHttp('Response is not 2XX')
        except HttpLib2Error:
            raise LoadHttp('Transport err')
        except:
            LoadHttp('unknown err')


if __name__ == "__main__":
    pass
    d = GoogleDrive()
