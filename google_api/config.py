from dataclasses import dataclass


@dataclass()
class ConfigDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CREDENTIALS_PATH = 'ul_cad_1.json'
    DRIVE_VERSION = 'v3'

    folder_id = '15_sFhZeHB_h1WfnuxiLCRj_DFXkZrJgIIOqrzYh6eh1OVg8BanYTFh3E1EIc8mXO_lzGjC6r'
    file_link = "https://drive.google.com/file/d/{}/view?usp=sharing"
