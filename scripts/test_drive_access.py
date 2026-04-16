import os
import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

def test_access():
    if not os.path.exists(TOKEN_PATH):
        print(f"Error: No se encontró {TOKEN_PATH}")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    drive = build('drive', 'v3', credentials=creds)

    print("\n--- Información del Usuario Autenticado ---")
    try:
        about = drive.about().get(fields="user").execute()
        print(f"Usuario: {about['user']['displayName']} ({about['user']['emailAddress']})")
    except Exception as e:
        print(f"No se pudo obtener info del usuario: {e}")

    print("\n--- Listando carpetas en la raíz (Top 10) ---")
    try:
        results = drive.files().list(
            q="mimeType = 'application/vnd.google-apps.folder'",
            pageSize=10, 
            fields="files(id, name)"
        ).execute()
        items = results.get('files', [])
        if not items:
            print('No se encontraron carpetas.')
        else:
            for item in items:
                print(f"{item['name']} ({item['id']})")
    except Exception as e:
        print(f"Error listando carpetas: {e}")

    target_folder = "1bnr_83zw1MAm8oHWewrrPNGvytkRAJsn"
    print(f"\n--- Probando acceso directo a: {target_folder} ---")
    try:
        folder = drive.files().get(fileId=target_folder, fields="id, name, permissions").execute()
        print(f"¡ÉXITO! Carpeta encontrada: {folder['name']}")
    except Exception as e:
        print(f"FALLÓ el acceso directo: {e}")
        print("\nTIP: Si la carpeta está en una 'Shared Drive' (Unidad Compartida), necesitamos activar soportes especiales en la API.")

if __name__ == "__main__":
    test_access()
