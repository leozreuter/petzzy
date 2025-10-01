import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Se modificar esses escopos, delete o arquivo token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # O arquivo token.json armazena os tokens do usuário.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Se não houver credenciais válidas, deixa o usuário fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Lembre-se de ter o client_secrets.json na raiz do projeto
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)
    return service