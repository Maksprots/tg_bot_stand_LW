from dataclasses import dataclass

from bot.config import ROOT_DIR


@dataclass()
class ConfigDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CREDENTIALS_PATH = ROOT_DIR + '/bot/ul_cad_1.json'
    DRIVE_VERSION = 'v3'

    folder_id = '15_sFhZeHB_h1WfnuxiLCRj_DFXkZrJgIIOqrzYh6eh1OVg8BanYTFh3E1EIc8mXO_lzGjC6r'
    file_link = 'https://drive.google.com/open?id={}'


@dataclass()
class ConfigSheets:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    CREDENTIALS_PATH = ROOT_DIR + '/bot/client_secret_Petukhov.json'
    print(CREDENTIALS_PATH)
    SPREADSHEET_ID = '1hydoacEI1g9zjaLma-NTmLf1OhgeulSbyRSB53M6tXo'

    SHEETS_VERSION = 'v4'
    rnage_to_chek_len = 'A:A'
