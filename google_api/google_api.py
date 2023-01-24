from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
'''
Пытаюсь собрать что-из основного кода
читается плохо, уходят часы 
извините что коммичу это в репу 
но иначе я совсем заблужусь)
'''
SCOPES = ['https://www.googleapis.com/auth/drive']

# Проверяем наличие файла токена
token_name = 'ul_cad_1.json'
token_path = root_path + '/' + token_name
if not (os.path.exists(token_path)):
    for root, dirs, files in os.walk('C:/'):
        if files.find(token) != -1:
            token_path = root + '/' + files
elif os.path.exists(token_path):
    SERVICE_ACCOUNT_FILE = token_path

    # Подключаемся к соответствующему сервису с помощью сервисного аккаунта Google
credentials = service_account.Credentials.from_service_account_file(
SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials, static_discovery=False)

def Get_main_folder_id(service):
    # Производим поиск среди папок по названию
    results = service.files().list(
        pageSize=1,
        fields=" files(id, name, mimeType, parents, createdTime)",
        q="name contains 'Remote_Stand_930' and mimeType='application/vnd.google-apps.folder'").execute()
    #pp.pprint(results['files'])
    file_info = results['files']
    # Получаем id главной папки
    main_folder_id = [item['id'] for item in file_info]
    #print(main_folder_id)
    # Переводим id из списка в строку
    str1 = ''.join(main_folder_id)
    main_folder_id = str1
    return main_folder_id

# Функия по созданию папки пользователя по названию почты
def Folder_create(service, Users_drive, main_folder_id):


    # Создание папки пользователя внутри главной папки
    folder_id = main_folder_id
    name = Users_drive
    # Задаем основные данные папки пользователя
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    # Создание папки с необходимыми метаданными
    r = service.files().create(body=file_metadata,
                               fields='id').execute()
    #pp.pprint(r)
    Folder_id = r['id']
    #print(Folder_id)
    return Folder_id

# Функция загрузки файлов пользователя
def File_upload(service, folder_id, file_path):
    # folder_id = '1PSD7Dutt6TIJqFmlM902oW70mFPy6pPH'
    # Задаем метаданные архива файлов пользователя
    name = 'rezult.zip'
    file_metadata = {
        'name': name,
        'mimeType': 'application/octet-stream',
        'parents': [folder_id]
    }
    # Задаем путь до загружаемых файлов, и необходимый mimetype
    media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)
    # Загрузка файлов
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    # Тело запроса назначения прав
    file_permission = {"role": "reader", "type": "anyone"}

    # Назначение прав
    service.permissions().create(
        body=file_permission, fileId=r.get("id")
    ).execute()

    #pp.pprint(r)
    # Создаем ссылку на файлы пользователя
    file_id = r['id']
    file_link = r"https://drive.google.com/file/d/" + file_id + r"/view?usp=sharing"
    #print(file_link)
    return file_link


