from zipfile import ZipFile
import os
from google_api.google_api import GoogleSheets, GoogleDrive
from bot.config import ROOT_DIR

drive = GoogleDrive()
sheets = GoogleSheets()


def upload_and_delete_zip(file_to_load, email_address):
    link_to_file_on_drive = drive.load_file(file_to_load,
                                            filename=file_to_load)
    sheets.write_request_to_table(email_address,
                                  link_to_file_on_drive
                                  )


def build_usr_files(id, email_addr):
    os.chdir(ROOT_DIR + '/documents')
    with ZipFile(f'{id}.zip', 'w') as zip_:
        zip_.write(f'F{id}.sof')
        zip_.write(f'S{id}.txt')
    upload_and_delete_zip(f'{id}.zip', email_addr)
    os.chdir(ROOT_DIR + '/handlers/')
