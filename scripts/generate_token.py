import os
import logging
from google_auth_oauthlib.flow import InstalledAppFlow

# Configuramos el logging para ver qué pasa
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Scopes necesarios
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

# Rutas de los archivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")

def generate_token():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"ERROR: No se encontró el archivo {CREDENTIALS_PATH}")
        print("Asegúrate de haber descargado el Client ID JSON desde GCP.")
        return

    print("--- Iniciando flujo de autenticación OAuth2 ---")
    print("Se abrirá una ventana en tu navegador...")
    
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    # Guardamos el token
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())
    
    print("-" * 50)
    print(f"¡ÉXITO! El token se ha guardado en: {TOKEN_PATH}")
    print("Ahora puedes iniciar el microservicio FastAPI.")
    print("-" * 50)

if __name__ == "__main__":
    generate_token()
