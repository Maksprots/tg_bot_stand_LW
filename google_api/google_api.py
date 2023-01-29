import os
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.auth.exceptions import MutualTLSChannelError

from googleapiclient.errors import HttpError
from httplib2 import HttpLib2Error

from config import ConfigDrive as cd
from exceptions import OpenCreds, BuildService, LoadHttp


class GoogleDrive:
    def __init__(self,
                 credentials_path=cd.CREDENTIALS_PATH,
                 scopes=cd.SCOPES):
        if not os.path.exists(credentials_path):
            print('file isnt exist')
            raise OpenCreds

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
            print('build is not successful')
            raise BuildService

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

            file_id = response.get('id')
            return cd.file_link.format(file_id)
        except HttpError:
            print('response is not 2XX')
            raise LoadHttp
        except HttpLib2Error:
            print("transport err")
            raise LoadHttp


if __name__ == "__main__":
    d = GoogleDrive()
    print(d.load_file(file_path='test_load.html', filename="test2_maks.html"))
