from dataclasses import dataclass


@dataclass()
class ConfigDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CREDENTIALS_PATH = 'ul_cad_1.json'
    DRIVE_VERSION = 'v3'

    folder_id = '15_sFhZeHB_h1WfnuxiLCRj_DFXkZrJgIIOqrzYh6eh1OVg8BanYTFh3E1EIc8mXO_lzGjC6r'
    file_link = "https://drive.google.com/file/d/{}/view?usp=sharing"


dataclass()


class ConfigSheets:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    CREDENTIALS_PATH = 'client_secret_Petukhov.json'
    SPREADSHEET_ID = '1hydoacEI1g9zjaLma-NTmLf1OhgeulSbyRSB53M6tXo'

    SHEETS_VERSION = 'v4'
    rnage_to_chek_len = 'A:A'
